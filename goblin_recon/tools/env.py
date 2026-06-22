"""Tiny .env fallback for local CLI tools."""

from __future__ import annotations

import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]


def _read_dotenv(path: Path, name: str) -> str | None:
    if not path.is_file():
        return None
    for raw in path.read_text(errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        if key.strip() == name:
            return value.strip().strip('"').strip("'") or None
    return None


def resolve_key(name: str) -> str | None:
    return (
        _read_dotenv(ROOT_DIR / ".env", name)
        or _read_dotenv(Path.home() / ".hermes" / "profiles" / "goblin-recon" / ".env", name)
        or os.environ.get(name)
    )
