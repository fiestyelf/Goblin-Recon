"""API-powered search for Goblin Recon — Exa semantic search + Tavily research search.

Usage:
    .venv/bin/python -m goblin_recon.tools.api_search --exa "AI agents 2026"
    .venv/bin/python -m goblin_recon.tools.api_search --tavily "OpenAI funding round"
    .venv/bin/python -m goblin_recon.tools.api_search --exa "AI safety" --limit 10 --json

Keys are read from:
    1. Project .env (goblin-recon/.env)
    2. Profile .env (~/.hermes/profiles/goblin-recon/.env)
    3. Environment variables (os.environ)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[2]

# ---- key loading -----------------------------------------------------------

def _load_dotenv(path: Path) -> dict[str, str]:
    """Parse a .env file into a dict. Ignores comments and blank lines."""
    result: dict[str, str] = {}
    if not path.is_file():
        return result
    for line in path.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key:
            result[key] = val
    return result


def _resolve_key(name: str) -> str | None:
    """Resolve an env var. Project .env wins — it's what the user edits."""
    # 1. Project .env (user's working copy — highest priority)
    project_env = ROOT_DIR / ".env"
    val = _load_dotenv(project_env).get(name)
    if val:
        return val
    # 2. Profile .env (Hermes copy)
    profile_env = Path.home() / ".hermes" / "profiles" / "goblin-recon" / ".env"
    val = _load_dotenv(profile_env).get(name)
    if val:
        return val
    # 3. Process environment (may be stale from session start)
    val = os.environ.get(name)
    if val:
        return val
    return None


# ---- Exa -------------------------------------------------------------------

EXA_BASE = "https://api.exa.ai/search"

def exa_search(query: str, limit: int = 5) -> list[dict[str, Any]]:
    """Search Exa for semantically relevant content."""
    key = _resolve_key("EXA_API_KEY")
    if not key:
        return [{"error": "EXA_API_KEY not set"}]

    req = urllib.request.Request(
        EXA_BASE,
        data=json.dumps({"query": query, "numResults": limit}).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        return _normalize_exa(data)
    except Exception as exc:
        return [{"error": str(exc)}]


def _normalize_exa(raw: dict) -> list[dict[str, Any]]:
    results = raw.get("results", [])
    return [
        {
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "published_date": r.get("publishedDate", ""),
            "author": r.get("author", ""),
            "score": r.get("score", None),
            "source": "exa",
        }
        for r in results
    ]


# ---- Tavily -----------------------------------------------------------------

TAVILY_BASE = "https://api.tavily.com/search"

def tavily_search(query: str, limit: int = 5, include_raw: bool = False) -> list[dict[str, Any]]:
    """Search Tavily for AI-optimized research results."""
    key = _resolve_key("TAVILY_API_KEY")
    if not key:
        return [{"error": "TAVILY_API_KEY not set"}]

    payload = {
        "api_key": key,
        "query": query,
        "max_results": limit,
    }
    if include_raw:
        payload["include_raw_content"] = True

    req = urllib.request.Request(
        TAVILY_BASE,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        return _normalize_tavily(data)
    except Exception as exc:
        return [{"error": str(exc)}]


def _normalize_tavily(raw: dict) -> list[dict[str, Any]]:
    results = raw.get("results", [])
    return [
        {
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "content": r.get("content", "")[:300],
            "score": r.get("score", None),
            "source": "tavily",
        }
        for r in results
    ]


# ---- CLI -------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="API-powered search for Goblin Recon")
    parser.add_argument("--exa", type=str, metavar="QUERY", help="Search via Exa")
    parser.add_argument("--tavily", type=str, metavar="QUERY", help="Search via Tavily")
    parser.add_argument("--limit", type=int, default=5, help="Max results (default: 5)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--include-raw", action="store_true", help="Include raw content (Tavily only)")
    args = parser.parse_args()

    if args.exa:
        results = exa_search(args.exa, args.limit)
    elif args.tavily:
        results = tavily_search(args.tavily, args.limit, args.include_raw)
    else:
        parser.print_help()
        sys.exit(1)

    if args.json or any("error" in r for r in results):
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"  {r.get('title', '?')}")
            print(f"  {r.get('url', '?')}")
            if r.get("content"):
                print(f"  {r['content'][:120]}…")
            print()


if __name__ == "__main__":
    main()
