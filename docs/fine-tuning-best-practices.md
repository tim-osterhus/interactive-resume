# Fine-Tuning Best Practices

Fine-tuning is a behavior tool, not an evidence source. For an interactive
resume, the best model is the one that answers from retrieved sources
faithfully, cites reliably, admits uncertainty, and runs fast enough for the
owner's hardware.

## Recommended Order Of Operations

1. Build the corpus.
2. Build ingestion and retrieval.
3. Build the prompt and citation contract.
4. Create evals.
5. Measure the base RAG system.
6. Fix retrieval and corpus gaps.
7. Fine-tune only the remaining answer-behavior failures.

Do not fine-tune before you have a baseline eval. Without a baseline, training
usually hides retrieval and corpus problems.

## What To Fine-Tune For

Good targets:

- Citation format discipline.
- Concise source-grounded answers.
- Missing-evidence admissions.
- Role-specific emphasis without hallucinated role fit.
- Refusal of private/source-dump requests.
- Limitation-aware phrasing.
- Consistent answer shape across common resume questions.

Poor targets:

- Memorizing the owner's resume.
- Compensating for missing corpus documents.
- Fixing bad retrieval.
- Teaching private facts that should not be public.
- Making unsupported claims sound confident.

## SFT First

Start with supervised fine-tuning.

Use SFT when you can write or synthesize high-quality examples of the desired
answer behavior. For this project, SFT examples should include:

- User question.
- Role/mode/profile context.
- Retrieved source snippets.
- Cited answer.
- Explicit missing-proof language when relevant.

Avoid training examples where the answer depends on facts not present in the
provided sources.

## Preference And RL Methods

Use preference or reward-based methods only after SFT works.

Preference tuning can help when you have pairs such as:

- cited answer vs uncited answer.
- cautious answer vs overclaiming answer.
- concise answer vs source dump.
- privacy-safe answer vs private-detail leak.

Reward-based methods can help citation and safety behavior, but they add
complexity. Do not use them for the first implementation unless the owner
already has training infrastructure.

## LoRA And QLoRA Defaults

For constrained hardware, use LoRA or QLoRA.

Starting points:

```text
method: QLoRA SFT
sequence_length: 1024 or 2048
lora_rank: 8 or 16 for smoke tests
lora_rank: 32 or 64 for stronger runs
lora_alpha: 2x lora_rank
lora_dropout: 0.0 to 0.05
learning_rate: 1e-4 to 2e-4
epochs: 1 to 3
packing: true when examples are short
```

Run a tiny smoke job before any long job. The smoke job should prove that the
dataset loads, loss decreases, checkpoints save, and inference still works.

## Dataset Size Guidance

Quality matters more than scale.

```text
smoke: 50-100 rows
first useful run: 500-1000 rows
strong first pass: 1000-2000 rows
larger run: only after evals show more data helps
```

Keep a held-out set that is not just random rows from the same prompt families.
Hold out entire question families and project/source combinations.

## Training Hygiene

Always record:

- Base model and revision.
- Dataset path and hash.
- Train/test split method.
- Corpus version used to retrieve sources.
- Hyperparameters.
- Hardware.
- Runtime and package versions.
- Checkpoint path.
- Eval results.

Keep generated datasets and model artifacts out of Git unless they are
sanitized examples.

## Overfitting Signs

Watch for:

- Better exact suggested-question performance but worse paraphrases.
- More confident answers with weaker source support.
- Repeating boilerplate regardless of question.
- Citation IDs that look valid but do not support the claim.
- Loss improving while held-out eval quality stagnates.

If these appear, reduce epochs, improve dataset variety, remove duplicates, or
return to retrieval/prompt fixes.

## Adoption Rule

Do not adopt a fine-tuned model unless it beats the current live baseline on:

- held-out eval score;
- citation-format reliability;
- privacy/safety tests;
- limitation questions;
- acceptable latency on target hardware.

If quality improves but latency fails, keep it as an optional deeper profile or
reject it.
