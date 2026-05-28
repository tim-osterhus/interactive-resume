# Minimal Resume Mode

Not every owner needs RAG. If the owner only has a single high-quality Markdown
resume or profile document, build a simpler evidence console first.

## When To Use

Use minimal mode when:

- there is one resume/profile document;
- there are few or no project artifacts;
- the owner wants a quick public site;
- hardware is limited;
- fine-tuning is not needed.

## Source Format

Use:

```text
private/resume.md
```

or a gitignored:

```text
raw-corpus/00-profile/resume.md
```

Recommended sections:

- Summary.
- Work history.
- Projects.
- Skills.
- Public links.
- Contact.
- Limitations or currently unproven claims.

## No Vector Index Required

For one document, parse sections and pack the relevant sections into the model
prompt. A simple section router is enough:

```text
question -> classify topic -> select resume sections -> generate cited answer
```

Citation IDs can refer to sections:

```json
[
  {
    "id": "S1",
    "title": "Resume: Projects",
    "excerpt": "..."
  }
]
```

## Upgrade Path To RAG

Move to full RAG when:

- answers need multiple documents;
- source popups should show artifact-specific evidence;
- job-fit needs deeper proof;
- evals show section routing misses important context.

The single resume can become `raw-corpus/00-profile/resume.md`.

## Fine-Tuning

Do not fine-tune for minimal mode unless:

- the owner already has evals;
- the same answer-format failure repeats;
- prompt changes are not enough.

Most minimal-mode systems should use a base instruction model with strict
prompting.
