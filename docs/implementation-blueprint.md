# Implementation Blueprint

This is the generic version of the interactive resume stack. An agent should be
able to start here, gather owner inputs, choose the right complexity level, and
build a personalized version.

## Choose The Complexity Level

### Level 0: Static Resume Only

Use when the owner only wants a static resume site.

Build:

- static homepage;
- contact page;
- downloadable resume;
- project/proof links.

No backend, no RAG, no fine-tuning.

### Level 1: Single-Document Evidence Console

Use when the owner only has one high-quality Markdown resume or profile doc.

Build:

- static site;
- small backend or browser-side answer helper;
- source-grounded answers from the single document;
- no vector index required.

This can use deterministic section lookup and prompt packing instead of RAG.
See [minimal-resume-mode.md](minimal-resume-mode.md).

### Level 2: Local RAG Evidence Console

Use when the owner has multiple evidence documents.

Build:

- private `raw-corpus/`;
- ingestion and local vector index;
- `/health` and `/chat` API;
- role prompt routing;
- citation source popups;
- eval suite.

This is the default full stack.

### Level 3: Fine-Tuned Local Model

Use when evals show answer-behavior failures after retrieval and prompts are
working.

Add:

- synthesized SFT dataset;
- dataset validator;
- LoRA/QLoRA training;
- candidate bakeoff;
- optional fast/deeper model profiles.

### Level 4: Job-Fit And Specialized Workflows

Use when the owner wants visitors to compare a job posting, investment thesis,
customer problem, or collaboration idea against the evidence corpus.

Add:

- job-fit input flow;
- structured fit analysis;
- evidence-backed match/gap/risk sections;
- stricter privacy and overclaiming rules.

See [job-fit-feature.md](job-fit-feature.md).

## Implementation Order

1. Run the intake in [personalization-intake.md](personalization-intake.md).
2. Choose Level 0, 1, 2, 3, or 4.
3. Create the frontend first if Level 0.
4. Create corpus or single-resume source if Level 1+.
5. Build backend API if Level 1+.
6. Add role routing from [role-prompt-routing.md](role-prompt-routing.md).
7. Add evals before model changes.
8. Add fine-tuning only after baseline evals justify it.
9. Add public deployment with [public-safety.md](public-safety.md).

## Non-Negotiables

- The public site must work when the backend is offline.
- The API must never expose raw model/runtime/database ports.
- The answerer must cite evidence or admit missing evidence.
- The corpus must not contain secrets, local paths, or private third-party data.
- Fine-tuning must not be used as a substitute for missing evidence.

## Suggested Repository After Implementation

```text
backend/
  app/
  data/index/              # gitignored
  data/evals/              # generated run outputs gitignored
frontend/
  src/
  dist/                    # gitignored
raw-corpus/                # gitignored or outside repo
generated/
  datasets/                # gitignored
  training-runs/           # gitignored
docs/
templates/
.codex/skills/
```

## Agent Completion Report

At the end of implementation, report:

- chosen level;
- local run commands;
- public deploy commands;
- corpus source and corpus version;
- model/runtime choices;
- eval baseline;
- safety limits;
- known limitations;
- what documents the owner still needs to provide.
