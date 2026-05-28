# Model Candidate Evaluation

Use this process before changing the live generation or embedding model.

## Candidate Log

For every candidate, record:

```text
candidate_name:
runtime:
quantization:
hardware:
embedding_model:
corpus_version:
retrieval_settings:
average_latency:
max_latency:
eval_score:
citation_failures:
privacy_failures:
notes:
decision:
```

## Evaluation Order

1. Confirm the model license.
2. Confirm it loads on the target runtime.
3. Run one manual smoke question.
4. Run the small smoke eval set.
5. Run the full held-out eval set.
6. Compare against the current live baseline.
7. Adopt only if it improves the actual objective.

## Objective

The objective is not benchmark score in isolation. The live model must:

- Answer from evidence.
- Cite consistently.
- Admit missing evidence.
- Stay within acceptable latency.
- Fit in available memory with the embedding model loaded.
- Avoid private leakage.
- Preserve a trustworthy public tone.

## Common Failure Modes

- Good answer quality but unacceptable latency.
- Strong general prose but weak citation discipline.
- Correct source retrieval but bad synthesis.
- Good model but context too small for source packing.
- Runtime supports model poorly.
- Model produces hidden reasoning but little visible answer.
- Training improves exact prompts but hurts held-out questions.
