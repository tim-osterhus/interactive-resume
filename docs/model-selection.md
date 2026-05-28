# Model Selection

The best model for this project is not necessarily the largest model. Choose
for local reliability, citation discipline, latency, licensing, and hardware
fit.

## Decision Criteria

Evaluate every candidate on:

- License compatibility.
- Runtime support.
- VRAM/RAM fit with the embedding model loaded.
- Context length.
- Citation-following behavior.
- Missing-evidence behavior.
- Average and tail latency.
- Quantization quality.
- Fine-tuning support.
- Ease of export to the serving runtime.

## Hardware Tiers

### CPU Only

Use:

- small embedding model;
- 1B to 3B generation model;
- aggressive response limits;
- conservative public concurrency.

Expect slower public answers. Consider hosted GPU inference if latency matters.

### 8 GB VRAM

Use:

- 2B to 4B instruction model for fast profile;
- quantized 4-bit or 5-bit GGUF for inference;
- one embedding model resident if possible;
- max concurrent generations of 1.

This is the practical minimum for a pleasant local public demo.

### 12-16 GB VRAM

Use:

- 3B to 8B instruction models;
- larger context windows;
- optional deeper profile;
- local QLoRA experimentation.

### 24 GB+ VRAM

Use:

- 7B to 14B models;
- broader profile comparisons;
- local fine-tuning with more comfortable batch sizes;
- stronger reranking or source packing experiments.

## Candidate Shortlist Process

1. Pick 3 to 5 models that fit the hardware.
2. Confirm licenses.
3. Confirm each model runs in the target runtime.
4. Run manual smoke prompts.
5. Run the smoke eval.
6. Run the full eval for the top candidates.
7. Choose the smallest/fastest model that passes the quality bar.

## Embedding Model Selection

Embedding quality controls source recall. Choose embeddings before blaming the
generator.

Evaluate:

- top-k expected source recall;
- multilingual needs;
- embedding latency;
- index size;
- runtime simplicity.

Keep the embedding model stable while comparing generation models. Change one
major variable at a time.

## Reranker Selection

Add a reranker only if source recall or source ordering is the bottleneck.

Measure:

- final source recall before and after reranking;
- latency added per request;
- CPU/GPU requirements;
- whether grouped source packing solves the same problem more cheaply.

For small public resume corpora, wider retrieval plus grouped source packing is
often simpler than live CPU reranking.

## Quantization

For GGUF inference:

- Start with Q4_K_M or equivalent for memory-constrained systems.
- Try Q5_K_M or Q6_K when quality matters and VRAM allows.
- Benchmark latency and answer quality, not just perplexity.

Do not assume a larger quantization is better if it causes CPU offload and
slower public responses.

## Live Model Change Checklist

Before changing the live model, record:

- old model eval score and latency;
- new model eval score and latency;
- citation failures;
- privacy failures;
- VRAM/RAM behavior;
- max observed latency;
- rollback command.

Keep the previous model available until the new one survives real traffic.
