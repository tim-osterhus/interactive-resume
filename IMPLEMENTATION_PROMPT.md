# Implementation Prompt For A Coding Agent

Use this prompt when asking an agent to instantiate the template for a specific
person.

```text
You are implementing this interactive-resume evidence console for me.

First, read AGENTS.md, README.md, docs/implementation-blueprint.md,
docs/personalization-intake.md, and docs/agent-implementation-playbook.md.
Then inspect the docs/ and templates/ directories.
Use the repo-local skills in .codex/skills/ when relevant:
interactive-resume-corpus, interactive-resume-rag, interactive-resume-evals,
interactive-resume-model-selection, interactive-resume-finetune,
interactive-resume-stack, and interactive-resume-job-fit.
For detailed dataset or training work, also consult the sanitized vendored
skills under .codex/skills/vendor/.

My public identity inputs are:

- Display name: <NAME>
- Headline: <HEADLINE>
- Public contact links: <LINKS>
- Target static site domain: <DOMAIN>
- Target API domain: <API_DOMAIN>
- Runtime host: <LOCAL_DESKTOP | HOME_SERVER | PRIVATE_GPU_HOST>
- Available hardware: <CPU/RAM/GPU/VRAM>
- Approved model runtime: <OLLAMA | LLAMA_CPP | VLLM | OTHER>
- Approved dataset-synthesis providers: <NONE | PROVIDER LIST>
- Private raw corpus path: <PATH>
- Existing input documents: <SINGLE_MARKDOWN_RESUME | MULTI_DOC_CORPUS | NONE>
- Job-fit feature: <YES | NO>

Your job:

1. Keep private corpus, generated indexes, generated datasets, model artifacts,
   and secrets out of Git.
2. Decide whether to build static-only, single-resume, RAG, fine-tuned, or
   job-fit scope.
3. Tell me exactly which documents I need to provide. If one Markdown resume is
   enough, say so and do not invent a RAG corpus requirement.
4. Curate or validate the raw corpus using docs/corpus-curation.md, or use
   docs/minimal-resume-mode.md for a single resume.
5. Build a backend that implements docs/api-contract.md when needed.
6. Build a static frontend using docs/frontend-static-site.md.
7. Add role routing from docs/role-prompt-routing.md.
8. Add job-fit from docs/job-fit-feature.md if requested.
9. Add evals using docs/evaluation.md.
10. Follow docs/public-safety.md before exposing anything publicly.
11. Only fine-tune after baseline RAG evals identify failures that fine-tuning
   can actually improve.

Ask me before:

- Using cloud model APIs with corpus content.
- Publishing any generated source summaries.
- Changing public domains.
- Exposing the API publicly.
- Training on any data that may include third-party confidential content.

At the end, report:

- Selected implementation level: static-only, single-resume, RAG, fine-tuned,
  job-fit, or a stated combination.
- Exact files created or changed.
- Exact commands run.
- Test and eval results, including failures.
- Local preview URL.
- Public deployment status and public URLs if deployed.
- Model/runtime choices, including whether placeholder generation is still in
  use instead of a real local model.
- Corpus version or corpus/index build summary.
- Privacy scan summary.
- Remaining owner decisions.
- Known limitations.
```
