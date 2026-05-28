from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import load_settings
from .sources import parse_markdown_file


def ingest_corpus(corpus: Path, index_path: Path) -> list[dict]:
    corpus = corpus.resolve()
    if not corpus.exists():
        raise FileNotFoundError(f"Corpus folder does not exist: {corpus}")
    sources = [
        parse_markdown_file(path, corpus)
        for path in sorted(corpus.rglob("*.md"))
        if path.is_file()
    ]
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps({"sources": sources}, indent=2), encoding="utf-8")
    return sources


def main() -> None:
    settings = load_settings()
    parser = argparse.ArgumentParser(description="Ingest Markdown evidence sources.")
    parser.add_argument("--corpus", "--corpus-dir", dest="corpus", type=Path, default=settings.corpus_path)
    parser.add_argument("--index", "--index-db", dest="index", type=Path, default=settings.index_path)
    args = parser.parse_args()
    sources = ingest_corpus(args.corpus, args.index)
    print(f"Ingested {len(sources)} Markdown source(s) into {args.index}")


if __name__ == "__main__":
    main()
