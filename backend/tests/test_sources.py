from __future__ import annotations

from pathlib import Path

from app.sources import excerpt, parse_markdown_file, source_slug, strip_frontmatter


def test_strip_frontmatter_removes_metadata_block():
    assert strip_frontmatter("---\ntitle: Hidden\n---\n# Public\nBody") == "# Public\nBody"


def test_parse_markdown_file_uses_frontmatter_without_exposing_it(tmp_path: Path):
    corpus = tmp_path / "corpus"
    nested = corpus / "projects"
    nested.mkdir(parents=True)
    source = nested / "Sample Project.md"
    source.write_text(
        "---\n"
        "title: Sample Project\n"
        "slug: sample-project\n"
        "url: https://example.com/sample\n"
        "tags: ai, proof\n"
        "---\n"
        "# Ignored Heading\n"
        "This public body should be shown.",
        encoding="utf-8",
    )

    parsed = parse_markdown_file(source, corpus)

    assert parsed["title"] == "Sample Project"
    assert parsed["slug"] == "sample-project"
    assert parsed["url"] == "https://example.com/sample"
    assert parsed["tags"] == ["ai", "proof"]
    assert parsed["path"] == "projects/Sample Project.md"
    assert parsed["body_text"] == "# Ignored Heading\nThis public body should be shown."
    assert "title:" not in parsed["body_text"]
    assert len(parsed["stable_id"]) == 10


def test_parse_markdown_file_falls_back_to_heading_and_filename(tmp_path: Path):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    with_heading = corpus / "with-heading.md"
    without_heading = corpus / "without-heading.md"
    with_heading.write_text("# Heading Title\nBody", encoding="utf-8")
    without_heading.write_text("Body only", encoding="utf-8")

    assert parse_markdown_file(with_heading, corpus)["title"] == "Heading Title"
    assert parse_markdown_file(without_heading, corpus)["title"] == "Without Heading"


def test_source_slug_and_excerpt_are_public_safe():
    assert source_slug(Path("My Project.md")) == "my-project"
    text = " ".join(["word"] * 200)
    short = excerpt(text, limit=40)

    assert len(short) <= 40
    assert short.endswith("...")
