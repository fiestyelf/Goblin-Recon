#!/usr/bin/env python3
"""Lightweight local secret scanner for Goblin Recon.

This catches common accidental leaks before the folder is shared or committed.
It is not a replacement for company secret scanning in GitHub.
"""

from __future__ import annotations

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


def should_scan(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    if path.name == ".env.example":
        return True
    if path.name.startswith(".env"):
        return True
    return path.suffix in TEXT_EXTENSIONS


def scan() -> list[str]:
    findings: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or not should_scan(path):
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


def main() -> int:
    findings = scan()
    if findings:
        print("Potential secrets found:")
        for finding in findings:
            print(f"- {finding}")
        print("Remove secrets before sharing or committing this folder.")
        return 1
    print("No obvious secrets found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
