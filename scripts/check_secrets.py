#!/usr/bin/env python3
"""Lightweight local secret scanner for Goblin Recon.

This catches common accidental leaks before the folder is shared or committed.
It is not a replacement for company secret scanning in GitHub.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".venv", ".git", "__pycache__"}
TEXT_EXTENSIONS = {".md", ".py", ".yaml", ".yml", ".toml", ".txt", ".example", ".sh"}

PATTERNS = {
    "generic_api_key_assignment": re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{20,}"),
    "openai_key": re.compile(r"sk-[A-Za-z0-9]{20,}"),
    "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    "slack_token": re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
    "discord_webhook": re.compile(r"https://discord(?:app)?\.com/api/webhooks/[A-Za-z0-9_\-/]+"),
}


def should_scan(path: Path, *, include_local_env: bool = False) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    if path.name == ".env.example":
        return True
    if path.name.startswith(".env"):
        # Local .env files are intentionally ignored by git and often contain
        # real development credentials. Keep CI/pre-commit scans clean by
        # default; use --include-local-env before packaging or sharing a folder.
        return include_local_env
    return path.suffix in TEXT_EXTENSIONS


def scan(*, include_local_env: bool = False) -> list[str]:
    findings: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or not should_scan(path, include_local_env=include_local_env):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            if path.name == ".env.example" and line.strip().startswith("#"):
                continue
            for name, pattern in PATTERNS.items():
                if pattern.search(line):
                    rel = path.relative_to(ROOT)
                    findings.append(f"{rel}:{line_no}: possible {name}")
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan Goblin Recon for obvious leaked secrets.")
    parser.add_argument(
        "--include-local-env",
        action="store_true",
        help="also scan ignored local .env files before packaging or sharing the folder",
    )
    args = parser.parse_args([] if argv is None else argv)

    findings = scan(include_local_env=args.include_local_env)
    if findings:
        print("Potential secrets found:")
        for finding in findings:
            print(f"- {finding}")
        print("Remove secrets before sharing or committing this folder.")
        return 1
    print("No obvious secrets found.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
