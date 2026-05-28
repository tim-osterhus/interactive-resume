from __future__ import annotations

import hashlib
import re
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
HEADING_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER_RE.sub("", text).strip()


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text.strip()
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"')
    return meta, text[match.end() :].strip()


def source_slug(path: Path) -> str:
    return path.stem.lower().replace(" ", "-")


def source_id(path: Path) -> str:
    return hashlib.sha1(path.as_posix().encode("utf-8")).hexdigest()[:10]


def excerpt(body: str, limit: int = 520) -> str:
    compact = re.sub(r"\s+", " ", body).strip()
    if len(compact) <= limit:
        return compact
    if limit <= 3:
        return "." * max(limit, 0)
    return compact[: limit - 3].rstrip() + "..."


def parse_markdown_file(path: Path, corpus_root: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(raw)
    title = meta.get("title")
    if not title:
        heading = HEADING_RE.search(body)
        title = heading.group(1).strip() if heading else path.stem.replace("-", " ").title()
    rel_path = path.relative_to(corpus_root).as_posix()
    return {
        "stable_id": source_id(path.relative_to(corpus_root)),
        "slug": meta.get("slug", source_slug(path)),
        "title": title,
        "url": meta.get("url", ""),
        "tags": [item.strip() for item in meta.get("tags", "").split(",") if item.strip()],
        "path": rel_path,
        "body_text": strip_frontmatter(raw),
        "excerpt": excerpt(body),
    }
