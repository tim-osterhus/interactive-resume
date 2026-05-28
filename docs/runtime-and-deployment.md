# Runtime And Deployment

This document gives generic command patterns. Replace placeholders with the
owner's machine, domain, and model choices.

## Local Model Runtime

### Ollama

Install Ollama from the official project instructions for the target operating
system.

Pull an embedding model:

```bash
ollama pull snowflake-arctic-embed2:latest
```

Pull or create a generation model:

```bash
ollama pull <small-instruction-model>
```

Verify:

```bash
ollama list
ollama run <small-instruction-model> "Reply with one sentence."
```

Keep Ollama bound to localhost or a private interface. Do not expose the Ollama
port publicly.

### llama.cpp Server

Use llama.cpp when you want direct GGUF control.

Generic command:

```bash
llama-server \
  --model /path/to/model.gguf \
  --host 127.0.0.1 \
  --port 11437 \
  --ctx-size 8192
```

Point the backend generation adapter at the OpenAI-compatible endpoint:

```bash
RAG_GENERATION_PROVIDER=llama-cpp-openai
RAG_GENERATION_BASE_URL=http://127.0.0.1:11437
```

The runnable starter includes an Ollama adapter. Other providers are documented
as implementation targets and should be added before using those provider
values in production.

## Backend Local Run

Example Python setup:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

On Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Run ingestion:

```bash
python -m app.ingest --corpus ../raw-corpus --index data/index/sources.json
```

The starter writes a small JSON index so the template can run without a vector
database. The full RAG version can replace this with SQLite/vector storage.

Run API:

```bash
python -m app.main
```

Health check:

```bash
curl http://127.0.0.1:8788/health
```

## Static Frontend Deployment

Build locally:

```bash
cd frontend
npm install
npm run build
```

Deploy the generated `dist/` directory to a static host.

For Cloudflare Pages, generic settings:

```text
Framework preset: None
Build command: npm run build
Build output directory: dist
Production branch: main
```

For GitHub Pages, use a static build artifact workflow that uploads `dist/`.

## Public API Exposure

### Cloudflare Tunnel Pattern

Create a public hostname such as:

```text
evidence-api.example.com
```

Route it to:

```text
http://127.0.0.1:8788
```

Only the backend API should be routed. Runtime and database ports remain
private.

### Reverse Proxy Pattern

With Caddy:

```text
evidence-api.example.com {
  reverse_proxy 127.0.0.1:8788
}
```

Add edge rate limiting if your provider supports it.

## Launch Verification

Before sharing the site:

```bash
curl https://evidence-api.example.com/health
```

Then send a small chat request:

```bash
curl -X POST https://evidence-api.example.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What can you prove from the corpus?","role":"recruiter","model_profile":"fast","session_id":"launch-smoke"}'
```

Verify:

- The response contains citations.
- The citations map to source objects.
- No private paths or secrets appear.
- CORS allows the static site origin.
- CORS rejects unknown origins.
- Rate limits and cooldowns work.
