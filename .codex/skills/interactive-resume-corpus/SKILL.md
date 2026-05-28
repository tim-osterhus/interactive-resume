---
name: interactive-resume-corpus
description: Curate, sanitize, structure, or review the private raw evidence corpus for an evidence-backed interactive resume. Use when collecting resume/project artifacts, writing evidence documents, labeling visibility, removing PII/secrets/local paths, or preparing corpus files for ingestion.
---

# Interactive Resume Corpus

## Workflow

1. Read `docs/corpus-curation.md` and
   `templates/corpus/evidence-document.md`.
2. Create one coherent evidence document per artifact, project, role, or
   limitation.
3. Use frontmatter fields consistently.
4. Label visibility before ingestion.
5. Sanitize before indexing.
6. Add limitation documents for weak or absent proof.

## Include

- Public resume facts.
- Project summaries and READMEs.
- Public repositories and launch notes.
- Architecture notes.
- Case studies.
- Public links.
- Sanitized testimonials.
- Evaluations and lessons learned.
- Known limitations.

## Exclude Or Redact

- Secrets, tokens, credentials.
- Local absolute paths.
- Home address, IDs, private phone numbers.
- Confidential employer/customer details.
- Private third-party names unless approved.
- Raw source dumps not safe for public summarization.
- Speculative claims the owner cannot support.

## Visibility Labels

- `public`: can be shown directly.
- `public_summary_only`: supports answers, but public display should use
  summary/excerpts.
- `private`: can support local answers only if policy allows; do not expose
  body text.
- `exclude`: do not ingest.

## Review Checklist

Before ingestion, verify:

- every file has title, source type, status, visibility, date, summary, tags;
- all public URLs are intentional;
- no local paths remain;
- no secret-like strings remain;
- limitations are explicit;
- the corpus can answer broad, project, role, proof, contact, and limitation
  questions.
