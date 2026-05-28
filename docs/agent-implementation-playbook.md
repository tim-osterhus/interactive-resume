# Agent Implementation Playbook

Use this when pointing a coding agent at the repository to implement an
evidence-backed interactive resume for a specific person.

## Phase 0: Owner Inputs

Collect:

- Public display name.
- Public title/headline.
- Public contact links.
- Target domain.
- Hardware/runtime choice.
- Hosting provider.
- Approved model licenses.
- Approved cloud providers, if any, for dataset synthesis.
- Private raw corpus location.

Do not proceed with public deployment until the owner has reviewed privacy
boundaries.

## Phase 1: Corpus

1. Create a gitignored `raw-corpus/` directory or point config to an external
   private corpus path.
2. Add evidence docs using `templates/corpus/evidence-document.md`.
3. Label visibility for each document.
4. Sanitize secrets, local paths, and private third-party details.
5. Add limitation documents for things the resume should not overclaim.

Output:

- Curated raw corpus.
- Corpus coverage notes.

## Phase 2: Backend

1. Create `backend/`.
2. Implement `/health` and `/chat` from `docs/api-contract.md`.
3. Add `.env.example` based on `templates/backend/.env.example`.
4. Add ingestion command.
5. Add retrieval and source packing.
6. Add generation adapter.
7. Add public limits.
8. Add tests.

Output:

- Local API running on localhost.
- Generated local vector index.
- Passing smoke tests.

## Phase 3: Frontend

1. Create `frontend/`.
2. Build static resume/proof-file pages.
3. Add chat client.
4. Add role picker and optional answer-depth toggle.
5. Render citation chips.
6. Add source modal/drawer.
7. Add offline and busy states.

Output:

- Static build directory.
- Local preview verified in browser.

## Phase 4: Evals

1. Create held-out eval questions using `docs/eval-creation-cookbook.md`.
2. Include smoke, full, and red-team eval files.
3. Run baseline.
4. Classify failures by root cause.
5. Fix corpus, retrieval, prompts, or UI issues before training.
6. Record baseline summary.

Output:

- Eval run files.
- Baseline score and latency.

## Phase 5: Fine-Tuning

Only start if baseline failures justify it.

1. Read `docs/fine-tuning-best-practices.md`.
2. Choose candidates using `docs/model-selection.md`.
3. Synthesize SFT rows from retrieved source packs.
4. Validate rows using `docs/dataset-quality.md`.
5. Run a smoke LoRA/QLoRA training job.
6. Export and serve candidate model.
7. Compare against baseline.

Output:

- Candidate model.
- Eval comparison.
- Decision note: adopt or reject.

## Phase 6: Public Launch

1. Deploy static frontend.
2. Run backend locally or on private host.
3. Configure tunnel/proxy to API only.
4. Set CORS to frontend origins only.
5. Verify `/health`.
6. Verify `/chat`.
7. Run abuse tests from `docs/public-safety.md`.

Output:

- Public static site.
- Public API endpoint.
- Private runtime.
- Launch checklist complete.

## Phase 7: Operations

1. Keep a private runbook with local startup commands.
2. Record corpus versions and eval results.
3. Re-run evals after corpus, prompt, retrieval, or model changes.
4. Monitor latency, queue depth, and timeout failures.
5. Periodically review source displays for privacy and usefulness.

Output:

- Current baseline note.
- Known failure modes.
- Next improvement queue.
