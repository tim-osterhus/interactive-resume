# Job-Fit Feature

The job-fit feature compares a pasted job description or opportunity brief
against the evidence corpus. It should be evidence-backed and limitation-aware,
not a hype generator.

## Product Framing

Recommended UI label:

```text
Compare a role against the evidence
```

Avoid labels that imply the system can decide hiring fit by itself.

## Inputs

Request:

```json
{
  "job_description": "Pasted job post or opportunity brief",
  "role": "recruiter",
  "session_id": "browser-generated-session-id",
  "model_profile": "thinking"
}
```

Do not log job descriptions by default. If logging is needed for debugging, ask
the owner and disclose it in the UI.

## Backend Endpoint

Recommended endpoint:

```text
POST /job-fit
```

Alternative: use `/chat` with `mode: "job_fit"`, but a separate endpoint is
cleaner because input validation and output shape differ.

## Output Shape

```json
{
  "summary": "Short evidence-backed fit summary.",
  "matches": [
    {
      "claim": "Relevant strength.",
      "evidence": ["S1", "S2"],
      "strength": "strong"
    }
  ],
  "gaps": [
    {
      "claim": "Requirement not proven by the corpus.",
      "evidence": [],
      "severity": "medium"
    }
  ],
  "risks": [
    {
      "claim": "Potential mismatch or unknown.",
      "evidence": ["S3"],
      "severity": "low"
    }
  ],
  "suggested_questions": [
    "Ask about ..."
  ],
  "sources": []
}
```

## Analysis Steps

1. Extract job requirements into skills, responsibilities, seniority, domain,
   constraints, and nice-to-haves.
2. Retrieve evidence for each major requirement.
3. Classify each requirement as `supported`, `partially_supported`, `missing`,
   or `contradicted`.
4. Generate a concise summary with citations.
5. Surface gaps clearly.
6. Suggest follow-up questions.

## Safety Rules

- Do not claim the person is a perfect fit.
- Do not infer private demographic or protected-class information.
- Do not fabricate experience for requirements.
- Do not treat missing corpus evidence as proof of absence.
- Do not store pasted job descriptions unless explicitly enabled.
- Cite matches; state gaps as missing evidence.

## Evals

Create job-fit evals with:

- job post text;
- expected supported requirements;
- expected missing requirements;
- forbidden overclaims;
- expected source tags.

Include adversarial jobs asking for skills that are not in the corpus. Correct
behavior is to identify gaps.

Use `templates/dataset/job-fit-eval-row.schema.json` for structured eval rows.
