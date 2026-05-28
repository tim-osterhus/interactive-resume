from __future__ import annotations

from app.main import create_app


def test_health_exposes_public_runtime_contract(configured_env):
    client = create_app().test_client()

    response = client.get("/health")

    assert response.status_code == 200
    data = response.get_json()
    assert data["ok"] is True
    assert data["default_model_profile"] == "fast"
    assert set(data["model_profiles"]) == {"fast", "thinking"}
    assert data["max_message_chars"] > 0
    assert data["max_queue_depth"] >= 0
    assert data["max_active_sessions"] == 3
    assert data["max_concurrent_generations"] >= 1


def test_chat_rejects_invalid_payloads(configured_env, monkeypatch):
    monkeypatch.setenv("RAG_MAX_MESSAGE_CHARS", "12")
    client = create_app().test_client()

    cases = [
        ({}, "empty_message"),
        ({"message": "hello", "role": "intruder"}, "invalid_role"),
        ({"message": "hello", "role": "builder", "model_profile": "slow"}, "invalid_model_profile"),
        ({"message": "hello", "role": "builder", "mode": "raw_dump"}, "invalid_mode"),
        ({"message": "this message is much too long", "role": "builder"}, "message_too_long"),
    ]

    for payload, code in cases:
        response = client.post("/chat", json=payload)
        assert response.status_code == 400
        assert response.get_json()["error"]["code"] == code


def test_chat_returns_cited_answer_without_leaking_source_path(configured_env):
    client = create_app().test_client()

    response = client.post(
        "/chat",
        json={
            "message": "What shipped citation popups?",
            "role": "builder",
            "model_profile": "fast",
            "session_id": "session-a",
        },
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["placeholder_generation"] is True
    assert data["role"] == "builder"
    assert data["model_profile"] == "fast"
    assert "[S1]" in data["answer"]
    assert data["sources"][0]["id"] == "S1"
    assert data["sources"][0]["static_source_path"] == "/evidence/sample-project/"
    assert "source_path" not in data["sources"][0]


def test_cooldown_rate_limits_repeated_session(configured_env, monkeypatch):
    monkeypatch.setenv("RAG_MESSAGE_COOLDOWN_SECONDS", "15")
    client = create_app().test_client()
    payload = {"message": "What shipped citation popups?", "role": "builder", "session_id": "same-session"}

    assert client.post("/chat", json=payload).status_code == 200
    response = client.post("/chat", json=payload)

    assert response.status_code == 429
    assert response.get_json()["error"]["code"] == "rate_limited"


def test_active_session_cap_rejects_new_sessions(configured_env, monkeypatch):
    monkeypatch.setenv("RAG_MAX_ACTIVE_SESSIONS", "1")
    client = create_app().test_client()

    assert client.post(
        "/chat",
        json={"message": "What shipped citation popups?", "role": "builder", "session_id": "session-a"},
    ).status_code == 200
    response = client.post(
        "/chat",
        json={"message": "What shipped citation popups?", "role": "builder", "session_id": "session-b"},
    )

    assert response.status_code == 429
    assert response.get_json()["error"]["code"] == "at_capacity"


def test_cors_allows_only_configured_origins(configured_env):
    client = create_app().test_client()

    allowed = client.get("/health", headers={"Origin": "https://resume.example"})
    disallowed = client.get("/health", headers={"Origin": "https://attacker.example"})

    assert allowed.headers["Access-Control-Allow-Origin"] == "https://resume.example"
    assert "Access-Control-Allow-Origin" not in disallowed.headers
