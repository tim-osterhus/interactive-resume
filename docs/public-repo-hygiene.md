# Public Repo Hygiene

Before publishing this template, do a release cleanup pass.

Required checks:

- Rewrite or squash history if any commit contains a real owner's name,
  private path, private corpus excerpt, secret, or machine-specific detail.
- Decide whether the Git remote should point to a personal namespace or a
  neutral template namespace.
- Remove generated files: `__pycache__/`, `.pyc`, `dist/`, indexes, eval runs,
  datasets, model artifacts, and local dependency folders.
- Confirm `.gitignore` excludes raw corpus, generated datasets, generated
  indexes, model artifacts, eval runs, `.env`, local dependency folders, and
  runtime caches.
- Scan tracked files for personal names, real domains, absolute local paths,
  private hostnames, and secret-shaped values.
- Replace secret-looking examples with safe placeholders like
  `<PROVIDER_API_KEY>`.

Recommended command:

```powershell
scripts/verify-template.ps1
```

History cleanup is intentionally not automated by the verifier because it is
destructive. Do it deliberately before the first public release.
