# Fine-Tuning Local Models

Start with RAG before fine-tuning. Fine-tuning is useful when the model has
consistent answer-style failures, citation-format failures, or role-framing
problems that prompts alone do not solve.

For the practical checklist, use
[fine-tuning-best-practices.md](fine-tuning-best-practices.md) alongside this
file.

## Model Selection

Choose small instruction models that fit the hardware.

Good first candidates:

- 2B to 4B parameter instruction models for 8 GB VRAM.
- 7B to 8B parameter instruction models for 12 GB to 16 GB VRAM.
- Quantized GGUF models for inference.
- LoRA or QLoRA for training.

Selection criteria:

- License allows your use.
- Context length supports your source packing.
- Inference latency is acceptable.
- The model follows citation formatting reliably.
- The model can be served by your runtime.

## Baseline Before Training

Record:

- Corpus version.
- Embedding model.
- Retrieval settings.
- Generation model.
- Quantization.
- Runtime.
- Hardware.
- Eval score.
- Average latency.
- Max latency.
- Citation-format failures.
- Qualitative failure notes.

Do not replace the live model unless the candidate improves quality without
breaking operational latency.

## Training Data

Use the dataset process in [dataset-synthesis.md](dataset-synthesis.md).

A practical starting point:

- 500 to 1,000 train rows for a smoke fine-tune.
- 100 to 200 held-out validation rows.
- 1,000 to 2,000 train rows for a serious first model.

Keep examples source-grounded. The model should learn how to answer from
provided snippets, not memorize the entire corpus.

## Training Method

Recommended first method: QLoRA supervised fine-tuning.

Typical settings to sweep:

- Sequence length: 1024, 1536, 2048.
- LoRA rank: 8, 16, 32.
- Learning rate: 1e-4 to 2e-4 for small models.
- Epochs: 1 to 3.
- Batch size: as large as fits, with gradient accumulation.

Use short smoke runs first. Run evals after each candidate.

## Export And Serve

Common path:

1. Train LoRA adapter.
2. Merge adapter into base model if desired.
3. Quantize to GGUF for local inference.
4. Import into Ollama or serve with llama.cpp.
5. Run the same eval suite used by the baseline.

Keep model artifacts out of Git. Store exact commands in a private operations
note or local run log.

## Evaluation Gates

A candidate must pass:

- No increase in citation-format failures.
- Better or equal held-out eval score.
- Acceptable average and max latency.
- No new privacy leaks.
- No regression on limitation questions.
- No unsupported role-fit claims.

## When Not To Fine-Tune

Prefer retrieval, prompts, or source formatting when:

- The right source is not retrieved.
- The source is retrieved but truncated.
- The prompt gives unclear citation instructions.
- The corpus lacks the answer.
- The model is too slow before training.

Fine-tuning cannot create evidence.
