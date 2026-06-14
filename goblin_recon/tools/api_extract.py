"""API-powered web extraction for Goblin Recon — Firecrawl + ScrapeGraph.

Usage:
    .venv/bin/python -m goblin_recon.tools.api_extract --firecrawl "https://example.com"
    .venv/bin/python -m goblin_recon.tools.api_extract --scrapegraph "https://example.com" --schema "pricing"
    .venv/bin/python -m goblin_recon.tools.api_extract --firecrawl "https://..." --json

Keys are read from:
    1. Project .env (goblin-recon/.env) — user's working copy, always wins
    2. Profile .env (~/.hermes/profiles/goblin-recon/.env)
    3. Process environment (os.environ)
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

# ---- key loading (shared with api_search.py) -------------------------------

def _load_dotenv(path: Path) -> dict[str, str]:
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


# ---- Firecrawl --------------------------------------------------------------

FIRECRAWL_BASE = "https://api.firecrawl.dev/v1/scrape"

def firecrawl_extract(url: str) -> dict[str, Any]:
    """Extract clean markdown/content from a URL via Firecrawl."""
    key = _resolve_key("FIRECRAWL_API_KEY")
    if not key:
        return {"error": "FIRECRAWL_API_KEY not set"}

    payload = {
        "url": url,
        "formats": ["markdown"],
    }
    req = urllib.request.Request(
        FIRECRAWL_BASE,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except Exception as exc:
        return {"error": str(exc), "url": url}

    md = data.get("data", {}).get("markdown", "")
    return {
        "url": url,
        "title": _extract_title(data),
        "content": md[:5000],
        "content_length": len(md),
        "source": "firecrawl",
    }


def _extract_title(data: dict) -> str:
    meta = data.get("data", {}).get("metadata", {})
    return meta.get("title", "") or meta.get("ogTitle", "") or ""


# ---- ScrapeGraph ------------------------------------------------------------

SCRAPEGRAPH_BASE = "https://v2-api.scrapegraphai.com/api/extract"

def scrapegraph_extract(url: str, schema: str = "article") -> dict[str, Any]:
    """Extract structured data from a URL via ScrapeGraph v2."""
    key = _resolve_key("SCRAPEGRAPH_API_KEY")
    if not key:
        return {"error": "SCRAPEGRAPH_API_KEY not set"}

    prompts = {
        "article": "Extract the main content, title, author, and publication date from this page.",
        "pricing": "Extract all pricing plans with plan name, price, and features list.",
        "features": "Extract all product features with name and description.",
        "competitor": "Extract the company name, products with pricing and key features.",
    }

    payload = {
        "url": url,
        "prompt": prompts.get(schema, prompts["article"]),
        "mode": "normal",
    }
    req = urllib.request.Request(
        SCRAPEGRAPH_BASE,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "SGAI-APIKEY": key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except Exception as exc:
        return {"error": str(exc), "url": url}

    return {
        "url": url,
        "schema": schema,
        "data": data.get("result", data),
        "source": "scrapegraph",
    }


# ---- CLI -------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="API-powered extraction for Goblin Recon")
    parser.add_argument("--firecrawl", type=str, metavar="URL", help="Extract page content via Firecrawl")
    parser.add_argument("--scrapegraph", type=str, metavar="URL", help="Extract structured data via ScrapeGraph")
    parser.add_argument("--schema", type=str, default="article",
                        choices=["article", "pricing", "features", "competitor"],
                        help="Schema for ScrapeGraph (default: article)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    if args.firecrawl:
        result = firecrawl_extract(args.firecrawl)
    elif args.scrapegraph:
        result = scrapegraph_extract(args.scrapegraph, args.schema)
    else:
        parser.print_help()
        sys.exit(1)

    if args.json or "error" in result:
        print(json.dumps(result, indent=2))
    else:
        title = result.get("title", result.get("url", ""))
        content = result.get("content", "")
        if content:
            print(f"  {title}")
            print(f"  {len(content)} chars extracted\n")
            print(content[:800])
            if len(content) > 800:
                print(f"\n  … ({len(content) - 800} more chars)")
        else:
            print(f"  {title}")
            print(json.dumps(result.get("data", {}), indent=2)[:2000])


if __name__ == "__main__":
    main()
