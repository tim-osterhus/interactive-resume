# Agent Skills

This template includes repo-local skills under `.codex/skills/`. They are
designed for future agents implementing the template.

## Included Skills

Template-specific skills:

- `interactive-resume-stack`: end-to-end template implementation and
  personalization workflow.
- `interactive-resume-rag`: backend, retrieval, citations, public API limits.
- `interactive-resume-corpus`: corpus curation, privacy, visibility labels.
- `interactive-resume-evals`: eval authoring, run analysis, failure classes.
- `interactive-resume-finetune`: SFT/LoRA/QLoRA dataset and training workflow.
- `interactive-resume-model-selection`: model, embedding, reranker, runtime,
  quantization, and hardware bakeoffs.
- `interactive-resume-job-fit`: job-fit/opportunity-fit feature.

Vendored installed skills:

- `vendor/fine-tuning`: detailed SFT, KTO, GRPO, LoRA, experiment-loop,
  checkpoint-evaluation, and cloud/local training workflow references.
- `vendor/golden-dataset`: golden dataset curation, versioning, validation,
  quality metrics, and backup/restore patterns.
- `vendor/huggingface-llm-trainer`: Hugging Face Jobs, TRL, Unsloth, GGUF
  conversion, hardware planning, and Hub persistence guidance.
- `vendor/evaluate-rag`: retrieval/generation evaluation, chunking evaluation,
  synthetic retrieval QA, and RAG trace dataset checks.
- `vendor/eval-audit`: evaluator and eval-result auditing.
- `vendor/generate-synthetic-data`: synthetic dataset generation workflows.
- `vendor/rag-corpus-hygiene`: corpus linting and pre-ingestion hygiene.
- `vendor/train-sentence-transformers`: embedding/reranker training.
- `vendor/validate-evaluator`: evaluator validation and calibration.

The vendored skills were copied from the local agent installation and sanitized
to replace local paths, personal handles, and secret-shaped examples with
placeholders.

## How To Use

If the agent runtime discovers repo-local skills, ask for them by name:

```text
Use $interactive-resume-stack to implement this template for me.
Use $interactive-resume-rag to implement the backend.
Use $interactive-resume-corpus to curate the corpus.
Use $interactive-resume-evals to create the eval suite.
Use $interactive-resume-finetune to plan fine-tuning.
Use $interactive-resume-model-selection to compare model candidates.
Use $interactive-resume-job-fit to add the job-fit feature.
```

If repo-local skills are not auto-discovered, copy the skill folders from
`.codex/skills/` into the agent's configured skills directory.

For deeper training workflows, copy or reference the relevant vendored skill
from `.codex/skills/vendor/`.

## Recommended Sequence

1. `interactive-resume-stack`
2. `interactive-resume-corpus`
3. `interactive-resume-rag`
4. `interactive-resume-evals`
5. `interactive-resume-model-selection`
6. `interactive-resume-finetune`
7. `interactive-resume-job-fit`
8. vendored skills when detailed training, data generation, corpus hygiene,
   embedding, or evaluator work is needed.

Fine-tuning should come after corpus, retrieval, and evals.
