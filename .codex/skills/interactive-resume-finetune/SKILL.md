---
name: interactive-resume-finetune
description: Plan, prepare, run, or review fine-tuning for an evidence-backed interactive resume model. Use when synthesizing SFT datasets, validating training rows, choosing LoRA/QLoRA settings, comparing checkpoints, exporting local models, or deciding whether fine-tuning is appropriate.
---

# Interactive Resume Fine-Tuning

## Workflow

1. Read `docs/fine-tuning-local-models.md`,
   `docs/fine-tuning-best-practices.md`, `docs/dataset-synthesis.md`, and
   `docs/dataset-quality.md`.
2. Confirm a baseline RAG eval exists.
3. Confirm failures are answer-behavior failures, not corpus/retrieval gaps.
4. Validate training data before launching training.
5. Start with a smoke run.
6. Compare the candidate against the baseline before adoption.

## Good Training Targets

- Citation discipline.
- Concise source-grounded answers.
- Missing-evidence admissions.
- Limitation-aware phrasing.
- Role emphasis without hallucinated fit.
- Refusal of private/source-dump requests.

## Bad Training Targets

- Memorizing the owner’s resume.
- Fixing missing evidence.
- Fixing bad retrieval.
- Adding unsupported claims.
- Teaching private facts that should not be public.

## Starting QLoRA Settings

Use as initial ranges, then evaluate:

```text
sequence_length: 1024 or 2048
lora_rank: 8 or 16 for smoke; 32 or 64 for serious runs
lora_alpha: 2x lora_rank
lora_dropout: 0.0 to 0.05
learning_rate: 1e-4 to 2e-4
epochs: 1 to 3
packing: true for short examples
```

## Dataset Validation

Require:

- unique row IDs;
- schema-valid JSONL;
- allowed roles/modes;
- citations in `answer` exist in `sources`;
- no local paths or secret-like strings;
- train/test separation by question family;
- human review for privacy and claim support.

## Adoption Rule

Do not adopt a fine-tuned model unless it improves held-out evals without
regressing citation reliability, privacy behavior, missing-evidence questions,
or latency.
