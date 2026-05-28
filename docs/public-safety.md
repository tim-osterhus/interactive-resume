# Public Safety

This system puts a private machine or private model runtime behind a public
website. Treat the public API as hostile.

## Never Expose Directly

Do not expose:

- Ollama ports.
- llama.cpp server ports.
- Docker API.
- SSH/RDP.
- Database ports.
- Raw vector index files.
- Local file browsers.
- Model management endpoints.

Expose only the RAG API.

## Required Controls

Implement:

- HTTPS.
- CORS allowlist.
- Request body limit.
- Message character limit.
- Per-session cooldown.
- Per-IP or edge rate limiting when available.
- Max concurrent generations.
- Queue depth cap.
- Timeout for generation calls.
- Safe error messages.
- Logging without secrets or full private source dumps.

Recommended starting limits:

```text
max_message_chars=2000
max_concurrent_generations=1
max_active_sessions=2
message_cooldown_seconds=15
max_queue_depth=5
generation_timeout_seconds=120
```

Tune upward only after measuring hardware behavior.

## Tunnel Or Proxy

Safe choices:

- Cloudflare Tunnel to `127.0.0.1:<api-port>`.
- Caddy/Nginx reverse proxy to a private backend.
- Cloudflare Worker proxy with validation and rate limiting.

The tunnel/proxy should target only the API service.

## Privacy Boundaries

The backend should avoid returning:

- Raw frontmatter.
- Private local paths.
- Private source body text marked as private.
- Secrets from source documents.
- System prompts.
- Debug traces.

Source objects can include public-safe excerpts and public URLs.

## Abuse Testing

Before launch, test:

- Very long input.
- Repeated requests from same session.
- Invalid JSON.
- Unknown role/mode/profile.
- Prompt injection asking for private corpus dumps.
- Prompt injection asking for system prompts.
- Requests from unapproved origins.
- Backend offline state.
- Model runtime timeout.
