---
name: interactive-resume-evals
description: Create, expand, run, or analyze evals for an evidence-backed interactive resume. Use when designing smoke/full/red-team eval questions, measuring retrieval recall, checking citations, classifying failures, comparing model/profile changes, or deciding whether a candidate model should replace the baseline.
---

# Interactive Resume Evals

## Workflow

1. Read `docs/evaluation.md` and `docs/eval-creation-cookbook.md`.
2. Create smoke, full, and red-team eval sets.
3. Track corpus version, embedding model, generation model, runtime, profile,
   score, latency, and failure classes for every run.
4. Classify failures before proposing fixes.

## Eval Set Targets

- Smoke: 10-20 questions.
- Full: 75-150 questions.
- Red-team: 20-50 questions.

Cover broad intro, project proof, work history, technical architecture, public
links, contact, limitations, missing evidence, prompt injection, and private
data requests.

## Metrics

Track:

- pass count;
- average latency;
- max or p95 latency;
- citation-format failures;
- expected source recall;
- privacy failures;
- timeout/error rate.

## Failure Classes

Use these labels:

- `corpus_missing`
- `chunking`
- `embedding_recall`
- `source_selection`
- `context_packing`
- `prompt`
- `model_synthesis`
- `citation_format`
- `privacy_safety`
- `frontend_display`

Fix the cheapest true cause first. Do not fine-tune a missing source or a bad
chunking strategy.

## Candidate Adoption Rule

Adopt a model/profile/retrieval change only if it improves the objective while
preserving:

- citation reliability;
- privacy behavior;
- missing-evidence behavior;
- acceptable latency;
- rollback ability.
