#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKIP_INSTALL="${SKIP_INSTALL:-0}"

step() {
  printf '\n== %s ==\n' "$1"
}

step "Backend install"
if [[ "$SKIP_INSTALL" != "1" ]]; then
  (cd "$REPO_ROOT/backend" && python -m pip install -e '.[dev]')
fi

step "Example ingest"
(cd "$REPO_ROOT/backend" && python -m app.ingest --corpus ../examples/raw-corpus)

step "Backend tests"
(cd "$REPO_ROOT/backend" && python -m pytest)

step "Smoke eval"
(cd "$REPO_ROOT/backend" && python -m app.evaluate --questions ../examples/evals/smoke-questions.jsonl)

step "Frontend install and tests"
if [[ "$SKIP_INSTALL" != "1" ]]; then
  (cd "$REPO_ROOT/frontend" && npm install)
fi
(cd "$REPO_ROOT/frontend" && npm test && npm run build)

step "Public hygiene scan"
if rg -n --hidden -g '!/.git/**' -g '!frontend/dist/**' -g '!backend/data/**' '(\bsk-[A-Za-z0-9_]{16,}\b|BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY|password\s*=|api[_-]?key\s*=)' "$REPO_ROOT"; then
  echo "Secret-shaped strings found" >&2
  exit 1
fi

if git -C "$REPO_ROOT" status --short -- raw-corpus private-corpus backend/data/index | grep .; then
  echo "Private/generated corpus or index files appear in git status" >&2
  exit 1
fi

printf '\nTemplate verification completed.\n'
