from __future__ import annotations

import json
from pathlib import Path

import pytest


@pytest.fixture()
def sample_index(tmp_path: Path) -> Path:
    index_path = tmp_path / "sources.json"
    index_path.write_text(
        json.dumps(
            {
                "sources": [
                    {
                        "stable_id": "sample-1",
                        "slug": "sample-project",
                        "title": "Sample Project",
                        "url": "https://example.com/sample",
                        "excerpt": "A fictional project that shipped citation popups and public proof notes.",
                        "body_text": "# Sample Project\nA fictional project that shipped citation popups and public proof notes.",
                    },
                    {
                        "stable_id": "sample-2",
                        "slug": "sample-limits",
                        "title": "Sample Limits",
                        "url": "",
                        "excerpt": "A fictional evidence boundary about missing revenue and traffic proof.",
                        "body_text": "# Sample Limits\nRevenue, fundraising, and production traffic are not proven in the sample.",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    return index_path


@pytest.fixture()
def configured_env(monkeypatch: pytest.MonkeyPatch, sample_index: Path) -> None:
    monkeypatch.setenv("RAG_INDEX_PATH", str(sample_index))
    monkeypatch.setenv("RAG_GENERATION_PROVIDER", "placeholder")
    monkeypatch.setenv("RAG_MESSAGE_COOLDOWN_SECONDS", "0")
    monkeypatch.setenv("RAG_MAX_ACTIVE_SESSIONS", "3")
    monkeypatch.setenv("RAG_ALLOWED_ORIGINS", "https://resume.example")
