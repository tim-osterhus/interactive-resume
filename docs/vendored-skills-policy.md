# Vendored Skills Policy

The `.codex/skills/` folder is optional helper context for coding agents. It is
not a runtime dependency for the backend or frontend.

Policy for this template:

- Keep template-specific skills in `.codex/skills/interactive-resume-*`.
- Keep `.codex/skills/vendor/` only if the public repo owner is willing to
  maintain and sanitize the copied skill content.
- Remove compiled artifacts and caches from vendored skills.
- Replace personal examples, real project names, real local paths, and
  secret-shaped placeholders with generic template language.
- Preserve upstream license files when vendored skills include them.
- Mention in release notes that vendored skills are convenience context, not
  authoritative legal, security, or model-provider guidance.

If the repo should be smaller, remove `.codex/skills/vendor/` and replace it
with instructions to install equivalent fine-tuning, RAG evaluation, synthetic
data, and dataset-quality skills in the user's agent environment.
