from __future__ import annotations

import json
import math
import re
from pathlib import Path


TOKEN_RE = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_-]+")


def tokenize(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(text)}


def load_sources(index_path: Path) -> list[dict]:
    if not index_path.exists():
        return []
    data = json.loads(index_path.read_text(encoding="utf-8"))
    return list(data.get("sources", []))


def retrieve(message: str, sources: list[dict], limit: int = 4) -> list[dict]:
    query_tokens = tokenize(message)
    scored = []
    for source in sources:
        haystack = " ".join(
            [source.get("title", ""), source.get("excerpt", ""), source.get("body_text", "")]
        )
        source_tokens = tokenize(haystack)
        overlap = query_tokens & source_tokens
        if not overlap:
            continue
        score = len(overlap) / math.sqrt(max(len(source_tokens), 1))
        scored.append((score, source))
    scored.sort(key=lambda item: item[0], reverse=True)
    selected = [source for _, source in scored[:limit]]
    return [
        {
            "id": f"S{idx}",
            "title": source["title"],
            "url": source.get("url", ""),
            "excerpt": source.get("excerpt", ""),
            "body_text": source.get("body_text", ""),
            "source_slug": source.get("slug", ""),
            "static_source_path": f"/evidence/{source.get('slug', '')}/",
            "static_source_anchor": source.get("slug", ""),
        }
        for idx, source in enumerate(selected, start=1)
    ]
