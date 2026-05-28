# Interactive Resume Evidence Console Template

This repository is a portable template for building a public interactive resume
backed by private, source-grounded local RAG.

The goal is not to create a chatbot that improvises a resume. The goal is to
create an evidence console: a public static website where visitors can ask
questions and receive concise, cited answers grounded in artifacts the owner
has curated.

## What You Build

```text
public static website
  -> public API endpoint
  -> reverse proxy or tunnel
  -> private backend API
  -> local vector index
  -> private raw evidence corpus
  -> local or self-hosted model runtime
```

The website can be hosted cheaply as static files. The backend can run on a
desktop, workstation, home server, rented GPU box, or small private cloud
instance. The raw evidence corpus and model runtime stay private.

## Minimum Practical Hardware

Recommended minimum:

- 4 CPU cores.
- 16 GB RAM.
- 8 GB VRAM if running local generation models on GPU.
- 20 GB free disk for models, indexes, and generated datasets.

CPU-only can work for small models and embeddings, but public latency will be
worse. If the owner does not have suitable local hardware, use a private
self-hosted GPU instance and keep the same API safety rules.

## Runnable Starter

This repository includes a minimal working reference stack. It is designed to
run against the fictional sample corpus before any personal data is added.

Backend smoke path:

```powershell
cd backend
python -m pip install -e ".[dev]"
python -m app.ingest --corpus ../examples/raw-corpus
python -m pytest
python -m app.evaluate --questions ../examples/evals/smoke-questions.jsonl
python -m app.main
```

Frontend smoke path:

```powershell
cd frontend
npm install
npm test
npm run build
npm run dev
```

Open `http://127.0.0.1:5173` while the backend is running on
`http://127.0.0.1:8788`.

The default backend uses deterministic placeholder generation so the template
can be tested without a local model. Set `RAG_GENERATION_PROVIDER=ollama` and
the model/runtime variables in `templates/backend/.env.example` when switching
to a real local model.

## Repository Map

- [AGENTS.md](AGENTS.md): instructions for coding agents.
- [docs/agent-implementation-playbook.md](docs/agent-implementation-playbook.md):
  end-to-end build checklist.
- [docs/implementation-blueprint.md](docs/implementation-blueprint.md):
  complexity levels from static resume to full RAG/fine-tuned/job-fit stack.
- [docs/personalization-intake.md](docs/personalization-intake.md): what an
  agent should ask the owner before building.
- [docs/minimal-resume-mode.md](docs/minimal-resume-mode.md): single Markdown
  resume mode when a full RAG corpus is unnecessary.
- [docs/role-prompt-routing.md](docs/role-prompt-routing.md): multi-role prompt
  routing and role-differentiation eval guidance.
- [docs/job-fit-feature.md](docs/job-fit-feature.md): evidence-backed job-fit
  feature design.
- [docs/architecture.md](docs/architecture.md): system design and deployment
  topology.
- [docs/api-contract.md](docs/api-contract.md): backend API shape expected by
  the frontend.
- [docs/corpus-curation.md](docs/corpus-curation.md): how to collect, sanitize,
  and structure evidence.
- [docs/dataset-synthesis.md](docs/dataset-synthesis.md): how to create
  training and eval datasets from the corpus.
- [docs/dataset-quality.md](docs/dataset-quality.md): dataset review,
  validation, dedupe, and split guidance.
- [docs/fine-tuning-local-models.md](docs/fine-tuning-local-models.md): how to
  fine-tune small local answer models.
- [docs/fine-tuning-best-practices.md](docs/fine-tuning-best-practices.md):
  practical SFT/LoRA/QLoRA guidance and adoption rules.
- [docs/model-selection.md](docs/model-selection.md): model, embedding,
  reranker, quantization, and hardware-fit decision guidance.
- [docs/frontend-static-site.md](docs/frontend-static-site.md): static website
  requirements.
- [docs/public-safety.md](docs/public-safety.md): public exposure and abuse
  controls.
- [docs/evaluation.md](docs/evaluation.md): quality gates and regression evals.
- [docs/eval-creation-cookbook.md](docs/eval-creation-cookbook.md): concrete
  eval-set design patterns and failure classification.
- [docs/runtime-and-deployment.md](docs/runtime-and-deployment.md): runtime,
  local run, tunnel, and static deployment patterns.
- [docs/deployment-recipes.md](docs/deployment-recipes.md): local-only,
  static-hosting, tunnel, VPS, GPU-host, and static-only recipes.
- [docs/public-repo-hygiene.md](docs/public-repo-hygiene.md): release cleanup
  checklist for public template publication.
- [docs/vendored-skills-policy.md](docs/vendored-skills-policy.md): how to
  treat `.codex/skills/vendor/`.
- [docs/model-candidate-evaluation.md](docs/model-candidate-evaluation.md):
  model bakeoff process before changing live models.
- [IMPLEMENTATION_PROMPT.md](IMPLEMENTATION_PROMPT.md): copy/paste prompt for
  instantiating this template with an agent.
- [docs/agent-skills.md](docs/agent-skills.md): repo-local and vendored skills
  for RAG, corpus, evals, model selection, dataset quality, and fine-tuning
  workflows.
- [templates/](templates): copyable starter files.
  - `templates/owner-inputs/resume.md` for single-document mode.
  - `templates/owner-inputs/intake-answers.md` for personalization intake.
- [examples/](examples): fictional public-safe corpus and smoke evals.
- [backend/](backend): minimal Flask API, ingestion, retrieval, placeholder
  generation, and local eval harness.
- [frontend/](frontend): dependency-light static frontend scaffold with
  citation chips and a source drawer.
- [scripts/](scripts): local verification scripts for agents before handoff.

## Private Inputs You Must Provide

This template deliberately contains no personal corpus. Before an agent can
implement it for a person, the owner should provide:

- A public display name and preferred headline.
- Public contact paths.
- A list of projects, roles, artifacts, and links that are safe to discuss.
- A private raw corpus folder containing sanitized evidence documents.
- A target public domain or subdomain.
- The chosen runtime location: local machine, home server, or private GPU host.
- Approved models and provider terms for any cloud-assisted dataset generation.

## Fast Start For An Implementing Agent

1. Start with `docs/implementation-blueprint.md`.
2. Run the intake in `docs/personalization-intake.md`.
3. Choose static, single-resume, RAG, fine-tuned, or job-fit scope.
4. Copy `templates/backend/.env.example` to the backend implementation as
   `.env.example`, then create a private `.env`.
5. Build or adapt a backend that implements `docs/api-contract.md`.
6. Curate `raw-corpus/` using `docs/corpus-curation.md`, or use
   `docs/minimal-resume-mode.md` for a single resume.
7. Ingest the corpus into a local vector index if using RAG.
8. Build the static frontend described in `docs/frontend-static-site.md`.
9. Run the eval process in `docs/evaluation.md`.
10. Add fine-tuning only after retrieval and prompt baselines are measured.
11. Deploy using `docs/public-safety.md` and `docs/architecture.md`.
12. Run `scripts/verify-template.ps1` or `scripts/verify-template.sh` before
    reporting success.

## Design Principle

Every impressive answer should point to receipts. Every unsupported answer
should admit the boundary.
