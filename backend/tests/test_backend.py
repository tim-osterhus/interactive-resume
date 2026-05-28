from __future__ import annotations

from pathlib import Path

from app.ingest import ingest_corpus
from app.main import create_app
from app.sources import strip_frontmatter


def test_strip_frontmatter():
    assert strip_frontmatter("---\ntitle: Hidden\n---\n# Public\nBody") == "# Public\nBody"


def test_ingest_and_chat(tmp_path, monkeypatch):
    corpus = tmp_path / "corpus"
    index = tmp_path / "sources.json"
    corpus.mkdir()
    (corpus / "sample.md").write_text(
        "---\ntitle: Sample Project\nslug: sample-project\nurl: https://example.com/sample\n---\n"
        "# Sample Project\nA fictional project that shipped citation popups.",
        encoding="utf-8",
    )
    ingest_corpus(corpus, index)
    monkeypatch.setenv("RAG_INDEX_PATH", str(index))
    monkeypatch.setenv("RAG_MESSAGE_COOLDOWN_SECONDS", "0")
    app = create_app()
    client = app.test_client()

    health = client.get("/health")
    assert health.status_code == 200
    health_data = health.get_json()
    assert health_data["ok"] is True
    assert health_data["queue_depth"] == 0
    assert health_data["max_queue_depth"] >= 0
    assert health_data["active_sessions"] >= 0
    assert health_data["max_active_sessions"] >= 1
    assert health_data["active_generations"] == 0
    assert health_data["max_concurrent_generations"] >= 1

    response = client.post(
        "/chat",
        json={"message": "What shipped citation popups?", "role": "builder", "model_profile": "fast"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "[S1]" in data["answer"]
    assert data["sources"][0]["title"] == "Sample Project"
    assert data["sources"][0]["static_source_path"] == "/evidence/sample-project/"
    assert "source_path" not in data["sources"][0]
