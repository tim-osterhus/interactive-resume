# Frontend Static Site

The frontend should remain static. It can be deployed to Cloudflare Pages,
GitHub Pages, Netlify, S3, or any static host.

## Required Features

- Public resume/proof-file content that works without the backend.
- Chat form connected to the API.
- Role picker.
- Optional answer-depth toggle mapped to backend `model_profile`.
- Optional job-fit/opportunity-fit panel when enabled.
- Browser-side input cap aligned with `/health.max_message_chars`.
- Client-generated `session_id`.
- Offline/degraded state when `/health` fails.
- Busy/rate-limit state for backend limits.
- Citation chips parsed from `[S1]` answer text.
- Source drawer/modal for source objects.
- Public-safe source content fallback.

## Suggested UI Framing

Avoid marketing fluff. The page should feel like a proof file:

- What this person has built.
- Evidence links.
- Selected artifacts.
- Known limits.
- Contact path.
- Question-and-answer area.

## No Secrets

The static site must not include:

- API keys.
- Private corpus documents.
- Hidden private metadata.
- Runtime hostnames that should remain private.
- Admin endpoints.

Only the public API base URL should be configured.

## Config Template

Use [templates/frontend/site-config.example.json](../templates/frontend/site-config.example.json)
as a starting point.

For role labels, keep frontend options aligned with
[templates/backend/role-prompts.example.json](../templates/backend/role-prompts.example.json).

## Job-Fit UI

If enabled:

- provide a textarea for a pasted job description;
- disclose whether pasted jobs are logged;
- show matches, gaps, risks, and suggested follow-up questions;
- render citations with the same source drawer as chat;
- avoid user-facing language that implies a definitive hiring decision.

## Build Output

The deployable output should be a static directory such as:

```text
dist/
```

The build should copy HTML, CSS, JavaScript, and public-safe generated evidence
summaries. Generated private corpus files should never be copied to `dist/`.

## Tests

Minimum frontend checks:

- Template copy stays generic before personalization.
- Answer rendering uses DOM APIs such as `textContent` and `createTextNode`,
  not arbitrary HTML insertion from model output.
- Citation chips are parsed from `[S1]` text without losing surrounding text.
- Source drawer content is rendered as text.
- The build writes the expected static files to `dist/`.
