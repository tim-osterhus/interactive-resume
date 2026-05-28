# Interactive Resume Template

A runnable starter for building a public, source-grounded interactive resume.

Use this repo when you want a static resume site backed by a private evidence
corpus, a small local API, cited answers, and a path toward local RAG,
fine-tuning, model evaluation, and job-fit analysis. The template ships with a
fictional sample corpus so you can run the stack before adding personal data.

## Tested Hardware Floor

The full local stack has only been tested on this baseline:

| Part | Tested baseline |
| --- | --- |
| CPU | AMD Ryzen 7 5700X, 8 cores / 16 threads |
| GPU | NVIDIA GeForce GTX 1080, 8 GB VRAM |
| RAM | 32 GB |

The smoke-test path can run without a local model because it uses deterministic
placeholder generation. The complete local workflow is different: running small
models, building indexes, running evals, and especially fine-tuning are unlikely
to work well on less hardware than the baseline above. It may still be possible
on smaller machines, but this repo has not been tested below that floor.
Fine-tuning on a GPU with less than 8 GB VRAM should be treated as experimental.

## Status

`v0.1.0` is a runnable template baseline, not a finished hosted product.

Current starter stack:

- Flask backend with `/health` and `/chat`.
- Static frontend with role selection, answer rendering, citation chips, and a
  source drawer.
- Fictional sample corpus under `examples/raw-corpus/`.
- Smoke eval harness under `examples/evals/`.
- Deterministic placeholder generation for first-run testing.
- Ollama adapter and environment template for local model generation.
- Agent-oriented implementation docs, templates, and optional skills.

The starter retrieval path is intentionally simple keyword retrieval. Replace it
with vector retrieval, chunking, reranking, and context packing when building a
full RAG version.

## Quick Start

Run the backend from a clean clone:

```powershell
cd backend
python -m pip install -e ".[dev]"
python -m app.ingest --corpus ../examples/raw-corpus
python -m pytest
python -m app.evaluate --questions ../examples/evals/smoke-questions.jsonl
python -m app.main
```

Run the frontend in another terminal:

```powershell
cd frontend
npm install
npm test
npm run build
npm run dev
```

Open `http://127.0.0.1:5173` while the backend is running on
`http://127.0.0.1:8788`.

You can also run the full local verifier:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/verify-template.ps1
```

Use `-SkipInstall` after dependencies are already installed.

## What This Builds

```text
static public website
  -> narrow public API endpoint
  -> private backend API
  -> private evidence corpus
  -> local index
  -> local or self-hosted model runtime
```

The website can be hosted as static files. The backend can run on a desktop,
home server, workstation, rented GPU box, or private cloud machine. Raw source
documents, model files, generated indexes, eval outputs, and secrets stay
private.

## What Is Included

| Path | Purpose |
| --- | --- |
| `backend/` | Minimal Flask API, ingestion, retrieval, generation adapter, tests, and eval runner. |
| `frontend/` | Dependency-light static site with citation chips and a source drawer. |
| `examples/raw-corpus/` | Fictional Markdown evidence source for first-run testing. |
| `examples/evals/` | Three-question smoke eval for citation and evidence behavior. |
| `templates/` | Copyable env, corpus, dataset, role-prompt, and owner-input templates. |
| `docs/` | Implementation, corpus, eval, deployment, fine-tuning, model-selection, and job-fit guides. |
| `.codex/skills/` | Optional repo-local skills for agents that support skill discovery. |
| `scripts/` | PowerShell and Bash verification scripts. |

## Personalization Flow

1. Read [docs/implementation-blueprint.md](docs/implementation-blueprint.md).
2. Fill out [docs/personalization-intake.md](docs/personalization-intake.md).
3. Decide whether you need static-only, single-document, RAG, fine-tuned, or
   job-fit scope.
4. Add private evidence documents to a local `raw-corpus/` folder.
5. Use [docs/corpus-curation.md](docs/corpus-curation.md) to sanitize and
   structure the corpus.
6. Ingest the corpus and run the smoke eval.
7. Replace placeholder generation with a configured local model runtime.
8. Run evals before changing prompts, retrieval settings, or models.
9. Deploy with the safety rules in [docs/public-safety.md](docs/public-safety.md).

For a very small resume, start with
[docs/minimal-resume-mode.md](docs/minimal-resume-mode.md) instead of building
a vector index immediately.

## Public And Private Boundary

Tracked examples are fictional and public-safe. Real user material should stay
out of the public template repo unless it has been deliberately reviewed and
published.

Keep these private or generated:

- `raw-corpus/`
- `private-corpus/`
- backend indexes
- eval run outputs
- local training datasets
- model files
- checkpoints and adapters
- `.env` files
- runtime credentials

The `.gitignore` is set up for that boundary. The sample corpus under
`examples/raw-corpus/` is intentionally tracked because it is fictional.

## Switching To A Real Local Model

The default backend uses placeholder generation so the template can be tested
without a GPU or model runtime. To use Ollama, copy
`templates/backend/.env.example`, set:

```text
RAG_GENERATION_PROVIDER=ollama
RAG_GENERATION_BASE_URL=http://127.0.0.1:11434
RAG_FAST_MODEL_NAME=replace-with-local-fast-model
RAG_THINKING_MODEL_NAME=replace-with-optional-slower-model
```

Then rerun ingestion, tests, and evals. Do not expose Ollama or other model
runtime ports directly to the public internet.

## Upgrade Paths

The starter is deliberately small. The deeper docs describe how to add:

- vector retrieval and source-aware context packing;
- multi-role prompt routing;
- model bakeoffs and latency checks;
- local SFT/LoRA/QLoRA fine-tuning;
- dataset validation;
- job-fit analysis for pasted role descriptions;
- static hosting plus a private API tunnel or reverse proxy.

Start with measured retrieval and prompt behavior before fine-tuning. The model
should learn answer discipline, citation behavior, and formatting; the corpus
should remain the source of facts.

## Release Checklist

Before publishing a personalized implementation:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/verify-template.ps1
```

Also check:

- no private corpus files are staged;
- no generated indexes or eval runs are staged;
- no `.env` files, tokens, model files, or local paths are staged;
- public claims cite public-safe source documents;
- unsupported claims admit missing evidence.

## License

MIT. See [LICENSE](LICENSE).
