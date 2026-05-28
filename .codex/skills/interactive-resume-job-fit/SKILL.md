---
name: interactive-resume-job-fit
description: Implement, evaluate, or review the job-fit/opportunity-fit feature for an evidence-backed interactive resume. Use when adding a pasted job description flow, structured match/gap/risk output, requirement extraction, fit evals, or privacy rules for job-fit analysis.
---

# Interactive Resume Job Fit

## Workflow

1. Read `docs/job-fit-feature.md`, `docs/role-prompt-routing.md`, and
   `docs/public-safety.md`.
2. Decide whether to add a separate `/job-fit` endpoint or a `/chat` mode.
3. Do not log pasted job descriptions by default.
4. Extract requirements before retrieving evidence.
5. Cite matches and state gaps as missing evidence.
6. Add evals for supported, partial, missing, and adversarial requirements.

## Output Sections

Return:

- summary;
- matches;
- gaps;
- risks;
- suggested follow-up questions;
- sources.

## Safety Rules

- Do not claim perfect fit.
- Do not fabricate experience.
- Do not infer protected-class information.
- Do not treat missing evidence as proof of absence.
- Do not store job descriptions unless the owner explicitly enables it.

## Evals

Test:

- relevant job with strong evidence;
- job with partial evidence;
- job with missing key requirements;
- adversarial job asking for unsupported claims;
- private-data or prompt-injection text inside the pasted job post.
