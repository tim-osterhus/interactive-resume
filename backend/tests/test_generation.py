from __future__ import annotations

from types import SimpleNamespace

from app.generation import generate_answer, ollama_answer, placeholder_answer


def test_placeholder_answer_admits_missing_evidence_without_sources():
    answer = placeholder_answer("What is the revenue?", [])

    assert "not have enough retrieved evidence" in answer
    assert "[S1]" not in answer


def test_placeholder_answer_bounds_revenue_claims():
    sources = [{"id": "S1", "title": "Sample Limits"}]

    answer = placeholder_answer("What revenue or traffic proof exists?", sources)

    assert "does not prove revenue" in answer
    assert "[S1]" in answer


def test_generate_answer_uses_placeholder_provider():
    settings = SimpleNamespace(
        generation_provider="placeholder",
        fast_model_name="fast-model",
        thinking_model_name="thinking-model",
    )

    answer, model = generate_answer(
        settings,
        "What shipped?",
        "builder",
        [{"id": "S1", "title": "Sample Project"}],
        None,
        "fast",
    )

    assert model == "fast-model"
    assert "Sample Project" in answer


def test_ollama_answer_posts_expected_payload(monkeypatch):
    seen = {}

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"response": "ok"}

    def fake_post(url, *, json, timeout):
        seen["url"] = url
        seen["json"] = json
        seen["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr("app.generation.requests.post", fake_post)

    answer = ollama_answer("http://localhost:11434/", "model-a", "Prompt", think=True, max_tokens=123, timeout=7)

    assert answer == "ok"
    assert seen["url"] == "http://localhost:11434/api/generate"
    assert seen["json"]["model"] == "model-a"
    assert seen["json"]["prompt"] == "Prompt"
    assert seen["json"]["think"] is True
    assert seen["json"]["options"]["num_predict"] == 123
    assert seen["timeout"] == 7
