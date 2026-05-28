# Architecture

## Target Shape

```text
visitor browser
  -> static website host
  -> HTTPS API endpoint
  -> tunnel or reverse proxy
  -> private RAG backend
  -> vector index
  -> private raw corpus
  -> model runtime
```

Use a static site for the public experience. Keep the backend narrow and
explicit. Keep raw documents, embeddings, and model ports private.

## Components

### Static Website

The static site owns:

- Resume/proof-file content that should work when the backend is offline.
- Role or audience picker.
- Optional answer-depth toggle.
- Chat form.
- Citation chip rendering.
- Source drawer or modal.
- Offline and busy states.

It must not contain secrets or private corpus content unless that content has
been intentionally published.

### RAG API

The API owns:

- Request validation.
- CORS.
- Public rate limits.
- Session cooldowns.
- Retrieval.
- Prompt construction.
- Generation runtime calls.
- Source object shaping.
- Error shaping.

Recommended first implementation: Python + Flask/FastAPI + Waitress/Uvicorn.
Keep the API small enough to audit.

### Vector Index

Use a local index first. SQLite with vector blobs is enough for a small resume
corpus. FAISS, LanceDB, Chroma, or Postgres/pgvector are also acceptable if the
owner already operates them.

The index is generated from the private raw corpus and should be ignored by Git.

### Model Runtime

Common local choices:

- Ollama for simple local model management.
- llama.cpp server for direct GGUF testing.
- vLLM or Text Generation Inference on stronger GPU hardware.

The runtime should listen only on localhost or a private network. The public
internet should reach only the RAG API.

## Profiles

A useful production shape has at least one profile:

- `fast`: small local model, lower latency, compact context.

Optional second profile:

- `thinking`: slower model, larger context, broader retrieval, better synthesis.

Do not expose chain-of-thought. If you add streaming, stream deterministic
status events such as `retrieving`, `reading sources`, and `drafting answer`.

## Public Endpoint

Use one public API endpoint, for example:

```text
https://evidence-api.example.com
```

Implementation options:

- Cloudflare Tunnel from the private machine to the public hostname.
- Nginx/Caddy reverse proxy on a VPS.
- Cloudflare Worker as a thin validation/proxy layer.

The endpoint should forward only to the RAG API port. Never proxy raw Ollama,
llama.cpp, Docker, or database ports.
