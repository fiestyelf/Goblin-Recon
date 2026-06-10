"""Brand gate checks for GenX/Goblin Recon copy."""

from __future__ import annotations

import re
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT_DIR / "config"
DEFAULT_CONFIG = CONFIG_DIR / "brand-voice.yaml"


def _list_items_after(lines: list[str], key: str) -> list[str]:
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
    return {
        "verdict": "FAIL" if violations else "PASS",
        "estimated_brand_score": estimated_score,
        "blacklist_violations": violations,
        "nuance_words": nuance_hits,
        "nuance_note": (
            "Nuance words require specific proof or client language."
            if nuance_hits
            else "No nuance words found."
        ),
    }
