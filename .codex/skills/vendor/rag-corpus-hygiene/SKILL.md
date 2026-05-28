---
name: rag-corpus-hygiene
description: Lint and review local RAG evidence corpora before ingestion, especially small evidence-first resume or portfolio RAG systems. Use when Codex needs to check markdown corpus docs for metadata quality, retrieval magnets, prompt-injection-like text, absolute local paths, duplicate sources, chunk-shape problems, privacy leaks, stale broad docs, or source-display readiness.
---

# RAG Corpus Hygiene

Use this skill before ingesting or re-ingesting a local evidence corpus. It is
designed for small, evidence-bound RAG systems where source quality matters more
than scale.

## Quick Start

Run the linter against the current corpus:

```powershell
python .codex\skills\vendor\rag-corpus-hygiene\scripts\lint_corpus.py --corpus raw-corpus --repo-root .
```

For machine-readable output:

```powershell
python .codex\skills\vendor\rag-corpus-hygiene\scripts\lint_corpus.py --corpus raw-corpus --format json
```

Use `--fail-on warn` in CI or before a final ingestion pass. Use `--include-archived`
only when intentionally inspecting archived/source-original files.

## Workflow

1. Run `scripts/lint_corpus.py`.
2. Fix `error` findings before ingestion.
3. Review `warn` findings and decide whether each is real cleanup or acceptable
   corpus intent.
4. Manually review the corpus for retrieval quality, not just lint cleanliness.
   Small evidence corpora should read like source documentation, not hidden
   system prompts, evaluator notes, or marketing summaries.
5. Re-run the linter.
6. Re-ingest the corpus only after the remaining findings are understood.

## What The Linter Checks

- Required corpus shape: readable files, markdown frontmatter, title/H1, body
  content, source metadata, public visibility metadata, and retrieval hooks.
- Local/privacy leakage: absolute Windows/macOS/Linux paths, suspicious secrets,
  non-allowlisted emails, private phone-like values, and private address-like
  fragments.
- Retrieval quality: broad rollup docs, retrieval-magnet titles/hooks, duplicate
  titles, exact duplicate bodies, overly large docs, and long paragraphs that
  split poorly under the backend's chunker.
- Prompt-injection hygiene: instruction-like text in corpus content such as
  "ignore previous instructions" or "reveal the system prompt".
- Public source display readiness: frontmatter stripping assumptions, source
  titles, and body text availability.

The linter flags suspicious material; it does not rewrite evidence docs. Treat
findings as review prompts, not automatic truth.

## Manual Review Checks

After linting, read the documents that are likely to affect retrieval most:
broad summaries, role/identity docs, source maps, heavily cited docs, and any
newly added evidence. Check for:

- Agent-facing structure such as `Retrieval Summary`, `Key Claim Summary`,
  `Evidence Boundaries`, answer instructions, or prompt-like labels.
- Prompt residue and evaluator scaffolding that should not be embedded as public
  evidence.
- Retrieval magnets: broad semantic language, overloaded summaries, or headings
  that could attract unrelated queries.
- Overly flowery prose where a precise fact, date, artifact, source, role, or
  limitation would retrieve more cleanly.
- Source-map prose that should be quarantined, narrowed, or converted into
  direct source-facing evidence wording.

Prefer concise, concrete documentation over broad positioning. Facts should live
in the narrowest appropriate source document, with broad overview docs excluded
from normal indexed evidence unless their retrieval hooks are intentionally
narrow.

## Interactive Resume Defaults

For a generic evidence-backed interactive resume:

- Corpus root: `raw-corpus`.
- Backend chunking defaults: `1200` characters with `150` overlap.
- Broad docs such as corpus overviews, answer banks, public answering
  guardrails, and positioning summaries should not return as normal indexed
  evidence unless intentionally scoped.
- Publicly allowed identity details should be configured by the owner, for
  example public name, public email, and public location.
- Absolute local paths should be replaced with placeholders before indexing or
  public source display.

## Interpreting Results

- `error`: fix before ingestion unless the user explicitly accepts the risk.
- `warn`: inspect before ingestion; many warnings are quality risks rather than
  hard failures.
- `info`: useful cleanup context.

Prefer corpus edits that move facts into narrower source-specific documents over
adding broad overview docs. If a broad document is necessary, keep it out of the
normal indexed evidence path or make its retrieval hooks narrow and explicit.
