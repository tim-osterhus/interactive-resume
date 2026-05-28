---
name: interactive-resume-stack
description: End-to-end implementation workflow for this generic interactive resume stack. Use when a user says "implement this for me", wants to personalize the template, choose between single-resume and RAG mode, wire frontend/backend/model runtime, add job-fit, or rebuild the stack from the template.
---

# Interactive Resume Stack

## Workflow

1. Read `README.md`, `AGENTS.md`, `docs/implementation-blueprint.md`, and
   `docs/personalization-intake.md`.
2. Determine the implementation level: static, single-document, RAG,
   fine-tuned, or job-fit.
3. Ask only for missing owner inputs required for that level.
4. Keep private corpus, generated datasets, indexes, secrets, and model
   artifacts out of Git.
5. Build in this order: corpus/source -> backend -> frontend -> evals ->
   model selection -> optional fine-tuning -> deployment.

## Required Decisions

- Is there one resume document or a multi-document corpus?
- Will the backend run locally, on a home server, or on a private GPU host?
- Is cloud dataset synthesis/training allowed?
- Is job-fit enabled?
- What public origins may call the API?

## Skill Routing

Use:

- `interactive-resume-corpus` for evidence collection and sanitization.
- `interactive-resume-rag` for backend and retrieval.
- `interactive-resume-evals` for evals.
- `interactive-resume-model-selection` for model/runtime choices.
- `interactive-resume-finetune` for training decisions.
- vendored `evaluate-rag`, `rag-corpus-hygiene`, `generate-synthetic-data`,
  `golden-dataset`, `fine-tuning`, `huggingface-llm-trainer`,
  `train-sentence-transformers`, `eval-audit`, and `validate-evaluator` when
  deeper workflow detail is needed.

## Completion Criteria

Report:

- chosen implementation level;
- documents still needed from the owner;
- local run commands;
- deployment commands;
- public URLs;
- runtime/model choices;
- corpus version;
- eval score and latency;
- known limitations and safety settings.
