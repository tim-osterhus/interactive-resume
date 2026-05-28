# Personalization Intake

Before building, the agent should ask for only the information needed to choose
the implementation level and protect privacy.

## Required Questions

Ask:

1. What public name, headline, and contact links should appear?
2. What domain or subdomain should host the static site?
3. What domain or subdomain should host the API, if any?
4. What hardware is available for local inference and training?
5. Do you already have a resume or evidence corpus?
6. Are cloud model APIs approved for dataset synthesis or only local models?
7. Should the site include a job-fit feature?

## Document Request Decision Tree

### If The Owner Has Only One Resume

Ask for:

- one Markdown resume or profile document;
- optional public links;
- optional contact info;
- optional known limitations.

Recommend Level 1. Tell the owner they do not need a RAG corpus yet.

### If The Owner Has Multiple Projects Or Artifacts

Ask for:

- resume;
- project notes;
- public repository links;
- shipped-product notes;
- work-history notes;
- public writing/talks;
- limitation notes;
- testimonials only if they have rights to use them.

Recommend Level 2.

### If The Owner Wants Fine-Tuning

Ask for:

- baseline eval results if they exist;
- approved base models;
- GPU details;
- whether Hugging Face Jobs or another cloud GPU provider is approved;
- whether generated datasets can be uploaded to a private Hub dataset.

If there is no baseline eval, build evals first.

### If The Owner Wants Job-Fit

Ask for:

- target role types;
- whether users may paste job descriptions;
- whether pasted job descriptions may be logged;
- desired output sections;
- risk tolerance for fit claims.

Default: do not log pasted job descriptions.

## Hardware Intake

Ask for:

```text
OS:
CPU:
RAM:
GPU model:
VRAM:
Disk free:
Can Docker run with GPU access:
Can Ollama run:
Can Hugging Face Jobs or cloud GPU be used:
```

Map this to [model-selection.md](model-selection.md).

## Privacy Intake

Ask:

- Are there employers, clients, or projects that must not be named?
- Are private documents allowed for local retrieval if excerpts are not shown?
- Are public source popups allowed to show full source text?
- Should the backend keep logs? If yes, what fields?
- Are pasted job descriptions allowed to leave the browser/backend?

Default to conservative public display.

## Owner Deliverables Checklist

Minimum for Level 1:

- `resume.md` using `templates/owner-inputs/resume.md`
- public contact links
- deployment domain decision

Minimum for Level 2:

- `resume.md`
- `raw-corpus/20-projects/*.md`
- `raw-corpus/10-work-history/*.md`
- `raw-corpus/30-public-links/*.md`
- `raw-corpus/40-limitations/*.md`

Minimum for Level 3:

- Level 2 corpus
- eval suite
- approved synthesis/training path
- candidate model list

Minimum for Level 4:

- Level 2 corpus
- fit output policy
- target audience roles
- example job descriptions for evals

## Intake Template

The owner can fill out
`templates/owner-inputs/intake-answers.md` before the agent starts. If it is
incomplete, ask only for the missing fields needed for the selected level.
