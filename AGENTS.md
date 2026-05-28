# AGENTS.md

## Project Role

This repository is a generic template for a public, evidence-backed interactive
resume.

The intended product shape is:

```text
static public website
  -> small public RAG API
  -> private local or self-hosted inference node
  -> private evidence corpus
  -> local vector index
```

This is not a generic resume chatbot. It is a trust-building evidence surface.
Answers should guide visitors back to artifacts, documents, public links,
source excerpts, and explicit limitations.

## Privacy And Portability Rules

- Do not commit private resumes, source documents, raw transcripts, IDs,
  addresses, secrets, tokens, API keys, private URLs, or local machine paths.
- Replace machine-specific details with placeholders and implementation notes.
- Keep raw corpus files outside the public template repository, or under a
  gitignored `raw-corpus/` directory.
- Keep generated indexes, eval outputs, fine-tuning datasets, checkpoints, and
  local model files out of Git unless they are deliberately sanitized examples.
- Do not expose raw model runtime ports publicly. Only expose the narrow API
  service, protected with CORS, rate limits, input limits, and queue limits.
- Treat all source-grounded claims as evidence-bound. If evidence is missing,
  say so.

## Expected Repository Shape

- `docs/`: implementation runbooks for agents and humans.
- `templates/`: copyable config, corpus, dataset, and frontend templates.
- `raw-corpus/`: optional local-only evidence documents. This path is ignored.
- `generated/`: local-only synthesized datasets, eval outputs, and indexes.
  This path is ignored.
- `backend/`: created by the implementing agent if this repo is used as the
  live backend repo.
- `frontend/`: created by the implementing agent if this repo is used as the
  live static-site repo.

## Implementation Priorities

1. Start with `docs/implementation-blueprint.md` and decide the right
   complexity level.
2. If one Markdown resume is enough, use `docs/minimal-resume-mode.md` instead
   of forcing a RAG corpus.
3. Curate and sanitize the evidence corpus before building model behavior.
4. Build retrieval and citation behavior before fine-tuning.
5. Add multi-role routing with explicit allowlists and prompt addendums.
6. Add a small static frontend with offline/degraded behavior.
7. Add evals before changing models or prompts.
8. Fine-tune only after the baseline RAG loop has measurable failures.
9. Add job-fit only with explicit privacy and logging decisions.
10. Deploy safely: static site public, API tunneled/proxied, model ports
    private.

## Agent Workflow

When asked to implement this for a specific person:

1. Read `README.md` and `docs/agent-implementation-playbook.md`.
2. Read `docs/implementation-blueprint.md` and
   `docs/personalization-intake.md`.
3. Ask the user for the minimum required identity, domain, hardware, and
   evidence-source decisions.
4. Tell the user exactly which documents are needed. If a single Markdown
   resume is enough, say so.
5. Create a private/local corpus using `docs/corpus-curation.md`, or use
   `docs/minimal-resume-mode.md`.
6. Build a backend that satisfies `docs/api-contract.md`.
7. Add role routing from `docs/role-prompt-routing.md`.
8. Build a static frontend that consumes that contract.
9. Add job-fit from `docs/job-fit-feature.md` if requested.
10. Run evals from `docs/evaluation.md` before and after changes.
11. If fine-tuning is requested, follow `docs/dataset-synthesis.md` and
   `docs/fine-tuning-local-models.md`.
12. Before deployment, check `docs/public-safety.md`.

Prefer simple, inspectable systems over clever abstractions. The first working
version should be easy for the owner to run, debug, and explain.
