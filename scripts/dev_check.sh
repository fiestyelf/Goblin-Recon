#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# Goblin Recon — Dev Health Check
# Run this before every commit, push, or share.
# ──────────────────────────────────────────────────────────────────────────────

set -euo pipefail
cd "$(dirname "$0")/.."
ROOT=$(pwd)
PYTHON="$ROOT/.venv/bin/python"
if [ ! -x "$PYTHON" ]; then
    PYTHON="python3"
fi

PASS=0
FAIL=0

green() { echo -e "\033[32m✓ $1\033[0m"; PASS=$((PASS + 1)); }
red()   { echo -e "\033[31m✗ $1\033[0m"; FAIL=$((FAIL + 1)); }
sep()   { echo "────────────────────────────────────────────"; }

echo
echo "  ╔══════════════════════════════════════════════╗"
echo "  ║   Goblin Recon — Pre-Flight Check            ║"
echo "  ╚══════════════════════════════════════════════╝"
echo

sep
echo "📦 Unit Tests"
sep

if "$PYTHON" -m pytest tests/ -v --tb=short --no-header 2>&1; then
    green "All unit tests pass"
else
    red "Unit tests failed — run bash scripts/setup.sh, then fix failures before committing"
fi

sep
echo "🔐 Secret Scanner"
sep

if "$PYTHON" scripts/check_secrets.py; then
    green "No secrets leaked"
else
    red "Secrets detected! Check findings above."
fi

sep
echo "📁 Project Structure"
sep

MISSING=0
for f in \
    "AGENTS.md" "SOUL.md" "INSTRUCTIONS.md" "README.md" \
    "scripts/extract_clip.py" "scripts/score_engagement.py" \
    "scripts/get_youtube_transcript.py" "scripts/check_secrets.py" \
    "templates/social-pulse-report.md" "templates/clip-mine-brief.md" \
    "config/sources.yaml" "config/content-sources.yaml" "config/scoring.yaml"
do
    if [ -f "$ROOT/$f" ]; then
        echo "  ✓ $f"
    else
        echo "  ⚠ Missing: $f"
        ((MISSING++))
    fi
done

if [ "$MISSING" -eq 0 ]; then
    green "All project files present"
else
    red "$MISSING file(s) missing"
fi

sep
echo "🧹 Dead File Check"
sep

if [ -f "$ROOT/templates/clip-brief.md" ]; then
    echo "  ⚠ Deprecated template still exists: templates/clip-brief.md"
    echo "    → Delete it: rm templates/clip-brief.md"
    echo "    → Use: templates/clip-mine-brief.md"
fi

if ls "$ROOT/skills/"*/SKILL.md 2>/dev/null | grep -q .; then
    green "Skills directory has content"
else
    red "All skill directories are empty"
fi

sep
echo "📝 Local Dumpground"
sep

if [ -d "$ROOT/personal-dumpground" ]; then
    echo "  personal-dumpground/ exists locally and is ignored by Git"
    green "Personal/change notes are separated"
else
    echo "  Optional: create personal-dumpground/ for local-only notes"
    green "No required personal files in release tree"
fi

sep
echo
echo "  ╔══════════════════════════════════════════════╗"
echo "  ║   Results: $PASS passed, $FAIL failed"
echo "  ╚══════════════════════════════════════════════╝"
echo

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
