# Corpus Curation

The corpus is the product. Fine-tuning and prompts can improve style, but the
system is only as trustworthy as the evidence it retrieves.

## What Belongs In The Corpus

Include documents about things the owner has actually done, built, shipped,
operated, evaluated, written, taught, or documented.

Good sources:

- Resume and work-history notes.
- Project READMEs.
- Public GitHub repository summaries.
- Launch notes.
- Case studies.
- Architecture notes.
- Blog posts and talks.
- Product screenshots with descriptions.
- Public links to artifacts.
- Sanitized performance reviews or testimonials if the owner has rights to use
  them.
- Sanitized internal project narratives that remove employer secrets.
- Known limitations, failed attempts, and lessons learned.

Avoid:

- Speculative future positioning not supported by work.
- Private customer data.
- Credentials, addresses, phone numbers, government IDs, compensation details,
  medical details, or family details.
- Confidential employer information.
- Raw chat exports unless carefully sanitized.
- Absolute local machine paths.
- Documents the owner cannot explain or defend.

## Recommended Directory Shape

```text
raw-corpus/
  00-profile/
  10-work-history/
  20-projects/
  30-public-links/
  40-limitations/
  50-testimonials/
  90-red-team-notes/
```

Use Markdown for most files. One file should represent one coherent evidence
unit.

## Document Template

Start from [templates/corpus/evidence-document.md](../templates/corpus/evidence-document.md).

Required frontmatter:

- `title`
- `source_type`
- `status`
- `visibility`
- `date`
- `summary`
- `public_url`
- `tags`

The backend may strip frontmatter before returning public source bodies, but
frontmatter is useful for ingestion and evals.

## Source Types

Use a controlled vocabulary:

- `resume`
- `project`
- `repository`
- `case_study`
- `blog_post`
- `talk`
- `testimonial`
- `architecture_note`
- `limitation`
- `evaluation`
- `contact`

## Visibility Labels

- `public`: safe to show directly.
- `public_summary_only`: source can support claims, but only summary/excerpts
  should be shown.
- `private`: use only locally; do not expose body text publicly.
- `exclude`: keep in folder for operator reference, but do not ingest.

## Sanitization Checklist

Before ingestion:

- Replace local paths with placeholders such as `[LOCAL_PROJECT_PATH]`.
- Replace private names with role labels when needed.
- Remove credentials and tokens.
- Remove private emails unless they are public contact addresses.
- Remove third-party confidential details.
- Mark documents that should not expose `body_text`.
- Confirm public URLs still resolve.
- Add limitations where proof is weak or absent.

## Coverage Checklist

The corpus should answer:

- What has this person built?
- What roles have they held?
- What artifacts prove the claims?
- What is public versus private?
- What technologies and workflows are evidenced?
- What is still unproven?
- What should a recruiter, investor, customer, collaborator, or peer know?
- How can someone contact them?

## Versioning

Compute a corpus version after each ingest. A simple version is a hash of the
sorted file paths plus file contents:

```text
local-<12-character-hash>
```

Expose that version through `/health` and `/chat` responses so eval results can
be tied to a specific corpus state.
