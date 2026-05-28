from __future__ import annotations

from app.retrieval import retrieve, tokenize


def test_tokenize_normalizes_words_and_ids():
    assert tokenize("Citation popups, RAG-backed UI!") == {"citation", "popups", "rag-backed", "ui"}


def test_retrieve_ranks_limits_and_remaps_sources():
    sources = [
        {
            "slug": "alpha",
            "title": "Alpha Project",
            "excerpt": "React dashboard",
            "body_text": "React dashboard with charts.",
        },
        {
            "slug": "beta",
            "title": "Beta Proof",
            "url": "https://example.com/beta",
            "excerpt": "citation popups",
            "body_text": "citation popups citation popups public evidence",
        },
        {
            "slug": "gamma",
            "title": "Gamma Proof",
            "excerpt": "citation",
            "body_text": "citation",
        },
    ]

    results = retrieve("citation popups evidence", sources, limit=2)

    assert [item["id"] for item in results] == ["S1", "S2"]
    assert results[0]["title"] == "Beta Proof"
    assert results[0]["url"] == "https://example.com/beta"
    assert results[0]["static_source_path"] == "/evidence/beta/"
    assert "path" not in results[0]


def test_retrieve_returns_empty_when_nothing_matches():
    assert retrieve("unrelated", [{"title": "Sample", "body_text": "Different words"}]) == []
