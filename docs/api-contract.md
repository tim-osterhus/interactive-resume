# API Contract

The static frontend should need only two backend endpoints.

If implementing job-fit, add `POST /job-fit` from
[job-fit-feature.md](job-fit-feature.md).

## `GET /health`

Returns public operational metadata.

Example:

```json
{
  "ok": true,
  "model": "local-fast-model-name",
  "generation_provider": "ollama",
  "default_model_profile": "fast",
  "model_profiles": {
    "fast": {
      "model": "local-fast-model-name",
      "think": false,
      "candidate_k": 20,
      "context_max_chars": 6000,
      "final_source_count": 5,
      "packing_strategy": "keyword_sources_placeholder"
    },
    "thinking": {
      "model": "optional-slower-model-name",
      "think": true,
      "candidate_k": 30,
      "context_max_chars": 16000,
      "final_source_count": 5,
      "packing_strategy": "keyword_sources_placeholder"
    }
  },
  "embedding_model": "embedding-model-name",
  "corpus_version": "local-version-hash",
  "uptime_seconds": 123,
  "queue_depth": 0,
  "max_queue_depth": 5,
  "active_sessions": 0,
  "max_active_sessions": 2,
  "active_generations": 0,
  "max_concurrent_generations": 1,
  "max_message_chars": 2000,
  "message_cooldown_seconds": 15
}
```

Keep this response free of secrets, local paths, private hostnames, and hardware
details that should not be public.

The runnable starter intentionally reports a placeholder keyword-retrieval
packing strategy. Replace that with the selected vector index, chunking,
reranking, and context-packing strategy when building the full RAG version.

## `POST /chat`

Request:

```json
{
  "message": "What has this person built?",
  "role": "recruiter",
  "model_profile": "fast",
  "session_id": "browser-generated-session-id"
}
```

Recommended roles:

- `recruiter`
- `investor`
- `customer`
- `builder`
- `friend`

Optional modes:

- `built`: shipped work, products, systems, and artifacts.
- `proof`: public links, receipts, concrete evidence, and source-backed claims.
- `limits`: fair critique, missing proof, weak claims, and evidence gaps.
- `job_fit`: optional compatibility mode when not using a separate `/job-fit`
  endpoint.

Mode is optional routing metadata, not a required frontend control. Prefer role
and task-specific endpoints for new UI behavior.

Recommended model profiles:

- `fast`
- `thinking`

Response:

```json
{
  "answer": "The person has shipped ... [S1]",
  "sources": [
    {
      "id": "S1",
      "title": "Project launch note",
      "url": "https://example.com/public-artifact",
      "excerpt": "Short evidence excerpt.",
      "body_text": "Optional longer public-safe body text.",
      "source_slug": "project-launch-note",
      "static_source_path": "/evidence/project-launch-note/",
      "static_source_anchor": "launch"
    }
  ],
  "confidence": "high",
  "mode": "proof",
  "role": "recruiter",
  "model_profile": "fast",
  "model": "local-fast-model-name",
  "corpus_version": "local-version-hash"
}
```

Allowed confidence values:

- `high`
- `medium`
- `low`

The frontend should display these as evidence-match language, for example
`strong evidence match`, `focused evidence match`, and `broad evidence match`.

The starter backend uses deterministic placeholder generation by default. It is
for local smoke tests only; production builds should switch
`RAG_GENERATION_PROVIDER` and model settings to a real private runtime.

## Errors

Return errors in a stable shape:

```json
{
  "error": {
    "code": "backend_unavailable",
    "message": "Evidence Console is temporarily offline."
  }
}
```

Suggested codes:

- `backend_unavailable`
- `rate_limited`
- `invalid_mode`
- `invalid_role`
- `invalid_model_profile`
- `message_too_long`
- `retrieval_failed`
- `generation_failed`

## Answer Contract

The assistant must:

- Answer from retrieved evidence.
- Use `[S1]`-style citations tied to returned source objects.
- Cite meaningful factual claims.
- Say when evidence is missing.
- Distinguish proven facts from interpretation.
- Avoid private facts not present in sources.
- Avoid uncited claim blocks.
- Surface limitations when relevant.
