---
name: interactive-resume-model-selection
description: Select or compare generation models, embedding models, rerankers, quantization levels, runtimes, and hardware profiles for an evidence-backed interactive resume. Use when planning candidate bakeoffs, changing live models, choosing fast/thinking profiles, or diagnosing latency/VRAM tradeoffs.
---

# Interactive Resume Model Selection

## Workflow

1. Read `docs/model-selection.md` and
   `docs/model-candidate-evaluation.md`.
2. Keep one baseline fixed while testing one major variable.
3. Confirm license and runtime support before evaluation.
4. Run smoke evals before full evals.
5. Record score, latency, citation failures, privacy failures, and memory fit.

## Selection Priorities

Prefer the smallest model that:

- answers from evidence;
- cites reliably;
- admits missing evidence;
- fits with the embedding model loaded;
- has acceptable tail latency;
- can be served and rolled back cleanly.

## Hardware Guidance

- CPU-only: expect slower answers; use very small models.
- 8 GB VRAM: target 2B-4B quantized generation models.
- 12-16 GB VRAM: test 3B-8B models and optional deeper profiles.
- 24 GB+ VRAM: consider larger models, local QLoRA, and rerankers.

## Change Checklist

Before changing live config, record:

- current baseline;
- candidate settings;
- corpus version;
- embedding model;
- generation model;
- runtime;
- quantization;
- eval score;
- average/max latency;
- citation/privacy failures;
- rollback command.
