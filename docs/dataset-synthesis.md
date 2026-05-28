# Dataset Synthesis

Fine-tuning data should teach source-grounded answering behavior. It should not
teach the model to memorize private facts without retrieval.

For dataset validation and review rules, use
[dataset-quality.md](dataset-quality.md).

## Recommended Dataset Types

Build three datasets:

- `eval_questions.jsonl`: held-out questions for regression testing.
- `sft_train.jsonl`: supervised fine-tuning rows.
- `sft_test.jsonl`: held-out fine-tuning validation rows.

Keep generated datasets private until they have been reviewed and sanitized.

## Row Shape

Use the schema in
[templates/dataset/training-row.schema.json](../templates/dataset/training-row.schema.json).

Example:

```json
{
  "id": "project_alpha_recruiter_001",
  "role": "recruiter",
  "messages": [
    {
      "role": "system",
      "content": "Answer from the provided sources. Cite factual claims with [S1]-style citations."
    },
    {
      "role": "user",
      "content": "What has this person shipped?"
    }
  ],
  "sources": [
    {
      "id": "S1",
      "title": "Project Alpha launch note",
      "excerpt": "Project Alpha launched with ..."
    }
  ],
  "answer": "They shipped Project Alpha, which ... [S1]"
}
```

## Synthesis Workflow

1. Start with hand-authored seed questions for each audience role.
2. Retrieve top sources for each question using the current index.
3. Draft answers that cite only the provided sources.
4. Generate paraphrases of the questions.
5. Generate adversarial and limitation-seeking questions.
6. Validate citations and source IDs mechanically.
7. Human-review privacy and claim accuracy.
8. Split train/test by question family, not by random row only.

## Suggested Role Distribution

For a small first fine-tune:

- `recruiter`: 25 percent.
- `builder`: 25 percent.
- `investor` or `customer`: 20 percent.
- `friend`: 15 percent.
- `limits`: 15 percent across roles or as a mode.

For a larger dataset, target 1,000 to 2,000 high-quality rows before chasing
scale.

## Answer Format Mix

Train the model on the production answer-shape policy, not a single rigid
format.

- Use cited bullets by default for proof, resume-scan, comparison, limitation,
  and diligence questions.
- Use short cited prose when explicitly requested, when the visitor asks a broad
  conversational question, or when a technical `builder` explanation reads more
  clearly as prose.
- Give the `friend` role wider format variety and a warmer, more casual tone,
  while keeping factual claims evidence-backed.
- Keep a small hybrid slice for "short synthesis plus receipts" answers.

For v3-style datasets, a practical target is roughly `65-75%` bullets,
`20-30%` prose, and `5-10%` hybrid answers. The row's format should serve the
question and role.

## Question Families

Cover:

- Broad intro questions.
- Project-specific questions.
- Work-history questions.
- Technical architecture questions.
- Evidence and citation questions.
- Contact questions.
- Negative-evidence questions.
- Limitation and critique questions.
- Ambiguous questions.
- Questions that should be refused or redirected.

## Quality Rules

Every training answer must:

- Use citations that exist in `sources`.
- Avoid uncited factual paragraphs.
- Say when proof is missing.
- Avoid claiming private or inferred facts.
- Preserve source boundaries.
- Use direct, public-safe language.
- Keep role tone as framing, not a separate personality.

## Provider-Terms Safety

If using a cloud model to synthesize rows:

- Confirm the corpus is sanitized for that provider.
- Confirm provider terms allow the intended data use.
- Do not use provider output to train a competing model when prohibited.
- Keep a note of which provider/model generated which rows.
- Human-review all generated rows before fine-tuning.

## Validation Script Requirements

Before training, implement a validator that checks:

- Unique row IDs.
- Allowed roles and modes.
- Required fields.
- Citation IDs in `answer` exist in `sources`.
- No local paths.
- No obvious secrets.
- No empty answers.
- Train/test split separation by question family.
- Reasonable role distribution.

Do not train on a dataset that fails validation.
