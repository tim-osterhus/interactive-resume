#!/usr/bin/env python3
"""Lint a small local RAG evidence corpus before ingestion.

The checks are intentionally conservative: they surface likely evidence-quality,
retrieval, privacy, and prompt-injection hygiene issues without rewriting source
documents.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SUPPORTED_SUFFIXES = {".md", ".markdown", ".txt", ".json"}
DEFAULT_IGNORE_DIRS = {".git", ".hg", ".svn", "__pycache__", "node_modules"}

BROAD_DOC_PATTERNS = {
    "corpus overview",
    "identity and positioning",
    "earlier professional background",
    "answer bank",
    "public answering guardrails",
}

BROAD_HOOK_PATTERNS = {
    "current overview",
    "strongest proof points",
    "who is this person",
    "public identity",
    "what should i know",
    "tell me about this person",
    "summarize this person",
    "overview of this person",
    "general summary",
}

PROMPT_INJECTION_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\bignore (all )?(previous|prior|above) instructions\b",
        r"\bdisregard (all )?(previous|prior|above) instructions\b",
        r"\breveal (the )?(system|developer) prompt\b",
        r"\bshow (the )?(system|developer) prompt\b",
        r"\byou are (chatgpt|an ai assistant|a language model)\b",
        r"\bact as (system|developer|admin|root)\b",
        r"\bdo not follow (the )?(system|developer) instructions\b",
        r"\bexfiltrate\b",
        r"<script\b",
    ]
]

SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bghp_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\b(cf|cloudflare)[-_ ]?(api[-_ ]?)?(token|key)\b.{0,30}[:=]\s*[A-Za-z0-9_-]{20,}", re.I),
    re.compile(r"\b(api[_-]?key|secret|password|passwd|token)\b\s*[:=]\s*['\"]?[^'\"\s]{12,}", re.I),
]

WINDOWS_PATH_RE = re.compile(r"\b[A-Za-z]:[\\/][^\s`'\"<>]+")
MAC_LINUX_PRIVATE_PATH_RE = re.compile(r"(?<!\w)/(Users|home)/[^\s`'\"<>]+")
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PHONE_RE = re.compile(r"(?<!\d)(?:\+?1[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}(?!\d)")
ADDRESS_HINT_RE = re.compile(
    r"\b\d{2,6}\s+[A-Za-z0-9.' -]{2,40}\s+"
    r"(Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Drive|Dr|Court|Ct|Way|Boulevard|Blvd)\b",
    re.I,
)


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    line: int
    message: str


@dataclass
class Document:
    path: Path
    rel_path: str
    text: str
    frontmatter: dict[str, object]
    body: str
    body_start_line: int
    title: str


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint a local RAG evidence corpus.")
    parser.add_argument("--corpus", default="raw-corpus", help="Corpus directory to lint.")
    parser.add_argument("--repo-root", default=None, help="Repo/workspace root for relative paths.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--fail-on", choices=["error", "warn", "never"], default="error")
    parser.add_argument("--include-archived", action="store_true", help="Include directories whose names start with underscore.")
    parser.add_argument("--chunk-chars", type=int, default=1200)
    parser.add_argument("--chunk-overlap", type=int, default=150)
    parser.add_argument(
        "--allow-email",
        action="append",
        default=["name@example.com"],
        help="Email address allowed in public corpus. Repeatable.",
    )
    args = parser.parse_args()

    corpus_dir = Path(args.corpus).resolve()
    repo_root = Path(args.repo_root).resolve() if args.repo_root else corpus_dir.parent
    allowed_emails = {email.lower() for email in args.allow_email}

    findings: list[Finding] = []

    if not corpus_dir.exists():
        findings.append(Finding("error", "corpus_missing", str(corpus_dir), 0, "Corpus directory does not exist."))
        return emit(findings, [], args)
    if not corpus_dir.is_dir():
        findings.append(Finding("error", "corpus_not_directory", str(corpus_dir), 0, "Corpus path is not a directory."))
        return emit(findings, [], args)

    documents = load_documents(corpus_dir, repo_root, include_archived=args.include_archived, findings=findings)
    lint_documents(documents, findings, allowed_emails, args.chunk_chars)
    lint_collection(documents, findings)

    return emit(findings, documents, args)


def load_documents(corpus_dir: Path, repo_root: Path, include_archived: bool, findings: list[Finding]) -> list[Document]:
    documents: list[Document] = []
    for path in sorted(corpus_dir.rglob("*")):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(corpus_dir).parts
        if not include_archived and any(part.startswith("_") for part in rel_parts[:-1]):
            continue
        if any(part in DEFAULT_IGNORE_DIRS for part in rel_parts):
            continue
        if path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue

        rel_path = display_path(path, repo_root)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(Finding("error", "decode_error", rel_path, 0, "File is not valid UTF-8."))
            continue
        except OSError as exc:
            findings.append(Finding("error", "read_error", rel_path, 0, f"Could not read file: {exc}"))
            continue

        frontmatter, body, body_start_line = split_frontmatter(text)
        title = infer_title(body) or string_value(frontmatter.get("title")) or path.stem.replace("-", " ").title()
        documents.append(Document(path, rel_path, text, frontmatter, body, body_start_line, title))

    if not documents:
        findings.append(Finding("error", "no_supported_docs", display_path(corpus_dir, repo_root), 0, "No supported corpus files found."))
    return documents


def lint_documents(documents: list[Document], findings: list[Finding], allowed_emails: set[str], chunk_chars: int) -> None:
    for doc in documents:
        lint_frontmatter(doc, findings)
        lint_body_shape(doc, findings, chunk_chars)
        lint_retrieval_hygiene(doc, findings)
        lint_sensitive_text(doc, findings, allowed_emails)
        lint_prompt_injection_text(doc, findings)


def lint_frontmatter(doc: Document, findings: list[Finding]) -> None:
    suffix = doc.path.suffix.lower()
    if suffix in {".md", ".markdown"} and not doc.frontmatter:
        findings.append(Finding("error", "missing_frontmatter", doc.rel_path, 1, "Markdown corpus doc has no ingestion frontmatter."))
        return

    if suffix in {".md", ".markdown"}:
        if not (string_value(doc.frontmatter.get("title")) or string_value(doc.frontmatter.get("doc_id"))):
            findings.append(Finding("warn", "missing_title_metadata", doc.rel_path, 1, "Frontmatter has neither title nor doc_id."))
        if not string_value(doc.frontmatter.get("source_file")):
            findings.append(Finding("warn", "missing_source_file", doc.rel_path, 1, "Frontmatter lacks source_file provenance."))
        if "source_sections" not in doc.frontmatter:
            findings.append(Finding("warn", "missing_source_sections", doc.rel_path, 1, "Frontmatter lacks source_sections provenance."))
        if "visibility" not in doc.frontmatter and "public_citation" not in doc.frontmatter:
            findings.append(Finding("warn", "missing_visibility", doc.rel_path, 1, "Frontmatter lacks visibility/public_citation metadata."))
        if not (
            "retrieval_topics" in doc.frontmatter
            or string_value(doc.frontmatter.get("answer_intent"))
            or string_value(doc.frontmatter.get("corpus_scope"))
        ):
            findings.append(Finding("warn", "missing_retrieval_metadata", doc.rel_path, 1, "Frontmatter lacks retrieval_topics, answer_intent, or corpus_scope."))

        source_file = string_value(doc.frontmatter.get("source_file"))
        if source_file and (WINDOWS_PATH_RE.search(source_file) or MAC_LINUX_PRIVATE_PATH_RE.search(source_file)):
            findings.append(Finding("error", "absolute_source_file", doc.rel_path, 1, "source_file contains an absolute local path."))


def lint_body_shape(doc: Document, findings: list[Finding], chunk_chars: int) -> None:
    body = doc.body.strip()
    if not body:
        findings.append(Finding("error", "empty_body", doc.rel_path, doc.body_start_line, "Corpus document body is empty."))
        return

    if not infer_title(doc.body):
        findings.append(Finding("warn", "missing_h1", doc.rel_path, doc.body_start_line, "Document body has no H1 heading."))

    if len(body) < 300:
        findings.append(Finding("warn", "very_short_body", doc.rel_path, doc.body_start_line, "Document body is very short; confirm it is useful evidence."))

    paragraphs = [paragraph for paragraph in re.split(r"\n\s*\n", body) if paragraph.strip()]
    for line_no, paragraph in paragraph_locations(doc.body, doc.body_start_line):
        if len(paragraph) > chunk_chars * 2:
            findings.append(Finding("warn", "oversized_paragraph", doc.rel_path, line_no, f"Paragraph is {len(paragraph)} characters and will be split bluntly by the backend chunker."))

    approximate_chunks = estimate_chunks(paragraphs, chunk_chars)
    if approximate_chunks > 10:
        findings.append(Finding("warn", "large_document", doc.rel_path, doc.body_start_line, f"Document will produce about {approximate_chunks} chunks; consider narrower source docs if retrieval quality suffers."))


def lint_retrieval_hygiene(doc: Document, findings: list[Finding]) -> None:
    title_norm = normalize_label(doc.title)
    path_norm = normalize_label(doc.path.stem)
    for pattern in BROAD_DOC_PATTERNS:
        if pattern in title_norm or pattern.replace(" ", "-") in path_norm:
            findings.append(Finding("error", "broad_doc_reintroduced", doc.rel_path, doc.body_start_line, f"Broad retrieval-magnet document appears to be reintroduced: {pattern}."))

    hooks = extract_retrieval_hooks(doc.body, doc.body_start_line)
    if len(hooks) > 14:
        findings.append(Finding("warn", "too_many_retrieval_hooks", doc.rel_path, doc.body_start_line, f"Document has {len(hooks)} retrieval hooks; overly broad hooks can make it a retrieval magnet."))

    for hook, line_no in hooks:
        hook_norm = normalize_label(hook)
        if len(hook_norm.split()) <= 2 and hook_norm in {"overview", "summary", "proof", "evidence", "background"}:
            findings.append(Finding("warn", "broad_retrieval_hook", doc.rel_path, line_no, f"Retrieval hook is very broad: {hook!r}."))
        for pattern in BROAD_HOOK_PATTERNS:
            if pattern in hook_norm:
                findings.append(Finding("warn", "retrieval_magnet_hook", doc.rel_path, line_no, f"Retrieval hook may attract unrelated broad queries: {hook!r}."))
                break


def lint_sensitive_text(doc: Document, findings: list[Finding], allowed_emails: set[str]) -> None:
    for line_no, line in enumerate(doc.text.splitlines(), start=1):
        for match in WINDOWS_PATH_RE.finditer(line):
            findings.append(Finding("error", "absolute_local_path", doc.rel_path, line_no, f"Absolute local path should be replaced with a placeholder: {match.group(0)}"))
        for match in MAC_LINUX_PRIVATE_PATH_RE.finditer(line):
            findings.append(Finding("error", "absolute_local_path", doc.rel_path, line_no, f"Absolute local path should be replaced with a placeholder: {match.group(0)}"))
        for pattern in SECRET_PATTERNS:
            if pattern.search(line):
                findings.append(Finding("error", "possible_secret", doc.rel_path, line_no, "Line resembles a secret, token, password, or API key."))
                break
        for match in EMAIL_RE.finditer(line):
            email = match.group(0).lower()
            if email not in allowed_emails:
                findings.append(Finding("warn", "non_allowlisted_email", doc.rel_path, line_no, f"Email is not on the public allowlist: {match.group(0)}"))
        if any(is_probable_phone_match(line, match) for match in PHONE_RE.finditer(line)):
            findings.append(Finding("warn", "phone_like_value", doc.rel_path, line_no, "Line contains a phone-number-like value; confirm it is intentionally public."))
        if ADDRESS_HINT_RE.search(line):
            findings.append(Finding("warn", "address_like_value", doc.rel_path, line_no, "Line contains a street-address-like value; confirm it is intentionally public."))


def lint_prompt_injection_text(doc: Document, findings: list[Finding]) -> None:
    for line_no, line in enumerate(doc.body.splitlines(), start=doc.body_start_line):
        for pattern in PROMPT_INJECTION_PATTERNS:
            if pattern.search(line):
                findings.append(Finding("warn", "prompt_injection_like_text", doc.rel_path, line_no, "Corpus text resembles an instruction to the model; verify it is evidence, not injected instructions."))
                break


def lint_collection(documents: list[Document], findings: list[Finding]) -> None:
    titles: dict[str, list[Document]] = {}
    hashes: dict[str, list[Document]] = {}
    hook_index: dict[str, list[tuple[Document, int]]] = {}

    for doc in documents:
        title_key = normalize_label(doc.title)
        titles.setdefault(title_key, []).append(doc)
        body_hash = hashlib.sha256(normalize_body(doc.body).encode("utf-8")).hexdigest()
        hashes.setdefault(body_hash, []).append(doc)
        for hook, line_no in extract_retrieval_hooks(doc.body, doc.body_start_line):
            hook_index.setdefault(normalize_label(hook), []).append((doc, line_no))

    for title_key, docs in titles.items():
        if title_key and len(docs) > 1:
            paths = ", ".join(doc.rel_path for doc in docs)
            findings.append(Finding("warn", "duplicate_title", docs[0].rel_path, docs[0].body_start_line, f"Duplicate title across corpus: {paths}"))

    for docs in hashes.values():
        if len(docs) > 1:
            paths = ", ".join(doc.rel_path for doc in docs)
            findings.append(Finding("warn", "duplicate_body", docs[0].rel_path, docs[0].body_start_line, f"Exact duplicate body text across corpus: {paths}"))

    for hook_key, locations in hook_index.items():
        if hook_key and len(locations) >= 4:
            first_doc, first_line = locations[0]
            paths = ", ".join(sorted({doc.rel_path for doc, _line in locations})[:6])
            findings.append(Finding("warn", "overused_retrieval_hook", first_doc.rel_path, first_line, f"Retrieval hook appears in {len(locations)} documents and may be too generic: {hook_key!r}. Examples: {paths}"))


def split_frontmatter(text: str) -> tuple[dict[str, object], str, int]:
    if not text.startswith("---"):
        return {}, text, 1
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, flags=re.DOTALL)
    if not match:
        return {}, text, 1
    frontmatter_text = match.group(1)
    body = match.group(2)
    return parse_simple_yaml(frontmatter_text), body, frontmatter_text.count("\n") + 3


def parse_simple_yaml(text: str) -> dict[str, object]:
    data: dict[str, object] = {}
    current_key: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- ") and current_key:
            data.setdefault(current_key, [])
            value = stripped[2:].strip().strip('"').strip("'")
            if isinstance(data[current_key], list):
                data[current_key].append(value)
            continue
        if ":" not in line:
            current_key = None
            continue
        key, value = line.split(":", 1)
        current_key = key.strip().lower()
        value = value.strip()
        if value == "":
            data[current_key] = []
        else:
            data[current_key] = value.strip('"').strip("'")
    return data


def infer_title(body: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return ""


def extract_retrieval_hooks(body: str, body_start_line: int) -> list[tuple[str, int]]:
    hooks: list[tuple[str, int]] = []
    in_section = False
    for line_no, line in enumerate(body.splitlines(), start=body_start_line):
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip().lower()
            in_section = heading == "retrieval hooks"
            continue
        if not in_section:
            continue
        if stripped.startswith("- "):
            hooks.append((stripped[2:].strip(), line_no))
    return hooks


def paragraph_locations(body: str, body_start_line: int) -> Iterable[tuple[int, str]]:
    current: list[str] = []
    start_line = body_start_line
    for offset, line in enumerate(body.splitlines(), start=0):
        if line.strip():
            if not current:
                start_line = body_start_line + offset
            current.append(line)
            continue
        if current:
            yield start_line, "\n".join(current)
            current = []
    if current:
        yield start_line, "\n".join(current)


def estimate_chunks(paragraphs: list[str], chunk_chars: int) -> int:
    if not paragraphs:
        return 0
    chunks = 0
    current = ""
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not current:
            current = paragraph
            continue
        if len(current) + len(paragraph) + 2 <= chunk_chars:
            current = f"{current}\n\n{paragraph}"
            continue
        chunks += max(1, (len(current) + chunk_chars - 1) // chunk_chars)
        current = paragraph
    if current:
        chunks += max(1, (len(current) + chunk_chars - 1) // chunk_chars)
    return chunks


def normalize_label(value: str) -> str:
    value = value.replace("-", " ").replace("_", " ").lower()
    value = re.sub(r"[^a-z0-9 ]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def is_probable_phone_match(line: str, match: re.Match[str]) -> bool:
    before = line[match.start() - 1] if match.start() > 0 else ""
    after = line[match.end()] if match.end() < len(line) else ""
    if before.isalnum() or after.isalnum():
        return False
    digits = re.sub(r"\D", "", match.group(0))
    return len(digits) == 10 or (len(digits) == 11 and digits.startswith("1"))


def normalize_body(value: str) -> str:
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"\s+", " ", value).strip().lower()
    return value


def string_value(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value).strip()


def display_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path)


def emit(findings: list[Finding], documents: list[Document], args: argparse.Namespace) -> int:
    severity_rank = {"info": 0, "warn": 1, "error": 2}
    counts = {
        "error": sum(1 for finding in findings if finding.severity == "error"),
        "warn": sum(1 for finding in findings if finding.severity == "warn"),
        "info": sum(1 for finding in findings if finding.severity == "info"),
    }

    if args.format == "json":
        payload = {
            "summary": {
                "documents": len(documents),
                "findings": counts,
            },
            "findings": [asdict(finding) for finding in findings],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"Corpus documents checked: {len(documents)}")
        print(f"Findings: {counts['error']} error, {counts['warn']} warn, {counts['info']} info")
        if findings:
            print()
        for finding in sorted(findings, key=lambda item: (-severity_rank[item.severity], item.path, item.line, item.code)):
            location = finding.path if finding.line <= 0 else f"{finding.path}:{finding.line}"
            print(f"[{finding.severity.upper()}] {finding.code} {location}")
            print(f"  {finding.message}")

    if args.fail_on == "never":
        return 0
    threshold = severity_rank[args.fail_on]
    return 1 if any(severity_rank[finding.severity] >= threshold for finding in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
