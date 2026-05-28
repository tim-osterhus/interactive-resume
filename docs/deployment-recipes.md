# Deployment Recipes

These recipes are provider-neutral patterns. Keep the raw corpus, generated
index, secrets, and model runtime private in every option.

## Local-Only Development

Public: nothing.

Private: backend API, raw corpus, generated index, local model runtime.

Environment:

- `RAG_GENERATION_PROVIDER=placeholder` for smoke tests.
- `RAG_GENERATION_PROVIDER=ollama` plus `RAG_GENERATION_BASE_URL` and model names
  for local model testing.
- `RAG_ALLOWED_ORIGINS=http://127.0.0.1:5173`.

Health check:

```powershell
curl http://127.0.0.1:8788/health
```

Rollback/offline behavior: stop the backend; the static frontend still shows
proof notes and a clear API-offline state.

## Static Hosting With No Public API

Public: static HTML/CSS/JS and reviewed proof summaries.

Private: all raw corpus, generated data, eval outputs, and model files.

Environment: none required for the frontend. Leave the API URL unset or point
it at a disabled endpoint.

Health check: open the static site and confirm it displays the offline badge.

Rollback/offline behavior: redeploy the previous static build.

## Static Hosting Plus Cloudflare Tunnel

Public: static site and one HTTPS API hostname.

Private: desktop/home-server backend, raw corpus, index, model runtime ports.

Environment:

- `RAG_ALLOWED_ORIGINS=https://resume.example.com`
- `RAG_API_HOST=127.0.0.1`
- `RAG_API_PORT=8788`
- tunnel config that forwards only the API hostname to `127.0.0.1:8788`

Health check:

```powershell
curl https://evidence-api.example.com/health
```

Rollback/offline behavior: disable the tunnel route or point the frontend at a
static-only build.

## VPS Reverse Proxy

Public: reverse proxy HTTPS endpoint and static site.

Private: backend process, corpus directory, index, runtime credentials.

Environment:

- `RAG_ALLOWED_ORIGINS=https://resume.example.com`
- `RAG_API_HOST=127.0.0.1`
- `RAG_API_PORT=8788`
- process manager config for the backend

Health check:

```bash
curl https://api.resume.example.com/health
```

Rollback/offline behavior: keep the previous backend release directory and
switch the reverse proxy upstream back to it.

## Private GPU Host

Public: only the narrow API endpoint and static site.

Private: GPU runtime, model files, corpus, generated training/eval artifacts.

Environment:

- `RAG_GENERATION_PROVIDER=ollama` or the adapter implemented for the host.
- runtime URL bound to localhost or a private network only.
- strict firewall rules allowing public traffic only to the API/proxy.

Health check:

```bash
curl https://api.resume.example.com/health
```

Rollback/offline behavior: keep the previous model available and switch the
model env var back after eval or latency regression.

## No-Backend Static-Only Mode

Public: static resume, proof links, limitations, and optional downloadable
resume.

Private: any source notes or raw documents not explicitly published.

Environment: none.

Health check: browser check only.

Rollback/offline behavior: redeploy the last known good static build.
