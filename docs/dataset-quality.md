# Dataset Quality

Dataset quality determines whether fine-tuning improves the system or just
makes it more confident.

## Golden Rules

- Every answer must be supported by the provided sources.
- Every factual claim should be cited.
- Missing evidence should be explicitly acknowledged.
- Private facts should not appear in public-facing training rows.
- Role changes should alter emphasis, not truth.
- Training rows should reflect the deployed API contract.

## Deduplication

Remove or reduce:

- exact duplicate questions;
- near-duplicate answers;
- repeated boilerplate intros;
- source packs with identical ordering for too many rows;
- examples that only differ by role label but have identical answer needs.

Keep deliberate paraphrases, but make sure they vary wording and source
combinations.

## Split Strategy

Do not rely only on random split.

Hold out:

- entire question families;
- exact public suggested-question paraphrase families;
- some projects or source groups;
- limitation and red-team prompts.

This tests generalization instead of memorization.

## Review Labels

Add review metadata when useful:

```json
{
  "review": {
    "privacy_checked": true,
    "citation_checked": true,
    "source_support": "strong",
    "generated_by": "human|model-name",
    "approved_by_owner": true
  }
}
```

## Common Bad Rows

Reject rows that:

- cite sources that do not support the answer;
- answer from general knowledge instead of source snippets;
- include hidden private context;
- overstate employment, revenue, traction, or impact;
- use vague praise without evidence;
- turn limitations into strengths without proof;
- contain local paths or private URLs;
- teach the model to reveal raw source dumps.

## Mechanical Validation

Before training, run checks for:

- JSONL parse validity.
- Schema validity.
- unique IDs.
- allowed roles/modes.
- citation IDs present in `sources`.
- local path patterns.
- secret-like strings.
- empty fields.
- excessive answer length.
- train/test leakage by question family.

Mechanical validation does not replace human review.
