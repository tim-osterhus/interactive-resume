# Evaluation

Evaluation keeps the console honest as the corpus, prompts, retrieval settings,
and models change.

For concrete eval authoring patterns, use
[eval-creation-cookbook.md](eval-creation-cookbook.md).

## Eval File Shape

Use [templates/dataset/eval-question.schema.json](../templates/dataset/eval-question.schema.json).

Example:

```json
{
  "id": "project_alpha_public_proof",
  "role": "recruiter",
  "mode": "proof",
  "question": "What public proof exists for Project Alpha?",
  "expected_source_tags": ["project_alpha", "public_link"],
  "required_phrases": ["Project Alpha"],
  "forbidden_phrases": ["guaranteed", "confidential"],
  "must_admit_missing_evidence": false
}
```

## Eval Categories

Include:

- Broad intro.
- Project proof.
- Technical architecture.
- Work history.
- Public links.
- Contact.
- Limitations.
- Missing-evidence questions.
- Prompt-injection attempts.
- Role-specific framing.
- Citation formatting.

## Metrics

Track:

- Pass count.
- Average latency.
- Max latency.
- Citation-format failures.
- Expected-source recall.
- Missing-evidence behavior.
- Privacy failures.
- Timeout/error rate.

## Regression Rule

Record every eval run with:

- timestamp.
- corpus version.
- embedding model.
- generation model.
- runtime.
- profile.
- settings.
- score summary.

Do not switch live models or retrieval settings without comparing against the
current baseline.

## Manual Review

Automated evals are not enough. Spot-check:

- Whether citations actually support claims.
- Whether answers overstate weak evidence.
- Whether role framing is natural.
- Whether limitations are visible.
- Whether public source popups are readable.
