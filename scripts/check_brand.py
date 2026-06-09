#!/usr/bin/env python3
"""Pre-flight brand gate check for GenX/Goblin Recon copy."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "brand-voice.yaml"


def _list_items_after(lines: list[str], key: str) -> list[str]:
    """Parse a simple YAML list nested under a top-level or second-level key."""
    items: list[str] = []
    in_section = False
    key_indent = 0

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))
        if stripped == f"{key}:":
            in_section = True
            key_indent = indent
            continue

        if in_section and indent <= key_indent and not stripped.startswith("-"):
            break

        if in_section and stripped.startswith("-"):
            items.append(stripped[1:].strip().strip('"'))

    return items


def load_brand_config(path: Path = DEFAULT_CONFIG) -> tuple[dict[str, list[str]], list[str]]:
    """Load blacklist categories and nuance words from brand-voice.yaml.

    The project does not depend on PyYAML, so this parser intentionally supports only
    the simple list structure used by config/brand-voice.yaml.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    nuance_words = _list_items_after(lines, "nuance_words")
    blacklist: dict[str, list[str]] = {}

    in_blacklist = False
    current_category: str | None = None

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))
        if stripped == "blacklist:":
            in_blacklist = True
            continue

        if in_blacklist and indent == 0 and not stripped.startswith("-"):
            break

        if not in_blacklist:
            continue

        if indent == 2 and stripped.endswith(":"):
            current_category = stripped[:-1]
            blacklist[current_category] = []
        elif indent == 4 and stripped.startswith("-") and current_category:
            blacklist[current_category].append(stripped[1:].strip().strip('"'))

    return blacklist, nuance_words


def _contains_phrase(text: str, phrase: str) -> bool:
    escaped = re.escape(phrase.lower())
    return re.search(rf"(?<![\w-]){escaped}(?![\w-])", text.lower()) is not None


def check_text(text: str, config_path: Path = DEFAULT_CONFIG) -> dict[str, object]:
    blacklist, nuance_words = load_brand_config(config_path)
    violations: dict[str, list[str]] = {}

    for category, phrases in blacklist.items():
        hits = [phrase for phrase in phrases if _contains_phrase(text, phrase)]
        if hits:
            violations[category] = hits

    nuance_hits = [word for word in nuance_words if _contains_phrase(text, word)]
    violation_count = sum(len(hits) for hits in violations.values())
    estimated_score = max(0, 15 - (violation_count * 2))
    verdict = "FAIL" if violations else "PASS"

    return {
        "verdict": verdict,
        "estimated_brand_score": estimated_score,
        "blacklist_violations": violations,
        "nuance_words": nuance_hits,
        "nuance_note": (
            "Nuance words require specific proof or client language."
            if nuance_hits
            else "No nuance words found."
        ),
    }


def _read_input(args: argparse.Namespace) -> str:
    if args.text:
        return args.text
    if args.file:
        return Path(args.file).read_text(encoding="utf-8")
    return sys.stdin.read()


def _print_markdown(result: dict[str, object]) -> None:
    violations = result["blacklist_violations"]
    print(f"Verdict: {result['verdict']}")
    print(f"Estimated brand score: {result['estimated_brand_score']}/15")
    if violations:
        print("Blacklist violations:")
        for category, hits in violations.items():
            print(f"- {category}: {', '.join(hits)}")
    else:
        print("Blacklist violations: none")
    nuance_words = result["nuance_words"]
    print(f"Nuance words: {', '.join(nuance_words) if nuance_words else 'none'}")
    print(str(result["nuance_note"]))


def main() -> int:
    parser = argparse.ArgumentParser(description="Check copy against GenX brand voice rules.")
    parser.add_argument("--text", help="Text to check.")
    parser.add_argument("--file", help="File containing text to check.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Path to brand-voice.yaml.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    args = parser.parse_args()

    text = _read_input(args)
    if not text.strip():
        print("No text provided. Use --text, --file, or stdin.", file=sys.stderr)
        return 2

    result = check_text(text, Path(args.config))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        _print_markdown(result)

    return 1 if result["verdict"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
