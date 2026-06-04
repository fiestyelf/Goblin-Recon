#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v uv >/dev/null 2>&1; then
  printf '%s\n' "uv is required. Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
  exit 1
fi

uv venv
uv pip install -r requirements.txt

printf '%s\n' "Setup complete. Use: source .venv/bin/activate"
