#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────────────────────
# Goblin Recon — One-Command Setup
# Usage: cd goblin-recon && bash scripts/setup.sh
# ─────────────────────────────────────────────────────────────

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# Project root (parent of scripts/)
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PROFILE_NAME="goblin-recon"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
PROFILE_DIR="$HERMES_HOME/profiles/$PROFILE_NAME"
SKILLS_DIR="$PROFILE_DIR/skills"

# ─────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}🔧 Goblin Recon Setup${NC}"
echo -e "${DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ─────────────────────────────────────────────────────────────
# Step 1: Prerequisites
# ─────────────────────────────────────────────────────────────
echo -e "${CYAN}🔍  Checking prerequisites...${NC}"

# Hermes Agent
if ! command -v hermes &> /dev/null; then
    echo -e "${RED}    ❌  Hermes Agent not found.${NC}"
    echo ""
    echo "    Install it first:"
    echo "    https://hermes-agent.nousresearch.com/docs"
    echo ""
    exit 1
fi
echo -e "    ✅  Hermes Agent found"

# Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}    ❌  Python 3 not found.${NC}"
    echo ""
    echo "    Install Python 3.9+: https://python.org"
    echo ""
    exit 1
fi
PY_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "    ✅  Python $PY_VERSION"

# uv (Python package manager)
if ! command -v uv &> /dev/null; then
    echo -e "    ⏳  Installing uv (Python package manager)..."
    if curl -LsSf https://astral.sh/uv/install.sh | sh > /dev/null 2>&1; then
        export PATH="$HOME/.local/bin:$PATH"
        echo -e "    ✅  uv installed"
    else
        echo -e "${RED}    ❌  Failed to install uv.${NC}"
        echo ""
        echo "    Install manually: curl -LsSf https://astral.sh/uv/install.sh | sh"
        echo ""
        exit 1
    fi
else
    echo -e "    ✅  uv found"
fi

# LLM Provider check (any provider works)
PROVIDER_CONFIGURED=false
for config_file in "$HERMES_HOME/config.yaml" "$PROFILE_DIR/config.yaml"; do
    if [ -f "$config_file" ]; then
        if grep -q "api_key" "$config_file" 2>/dev/null || \
           grep -q "provider" "$config_file" 2>/dev/null; then
            PROVIDER_CONFIGURED=true
            break
        fi
    fi
done

# Also check .env files for API keys
for env_file in "$HERMES_HOME/.env" "$PROFILE_DIR/.env" "$HOME/.env"; do
    if [ -f "$env_file" ]; then
        if grep -qE "(API_KEY|OPENAI|ANTHROPIC|DEEPSEEK)" "$env_file" 2>/dev/null; then
            PROVIDER_CONFIGURED=true
            break
        fi
    fi
done

if [ "$PROVIDER_CONFIGURED" = true ]; then
    echo -e "    ✅  LLM provider configured"
else
    echo -e "${YELLOW}    ⚠️  No LLM provider detected.${NC}"
    echo ""
    echo "    Goblin Recon needs an LLM provider to work."
    echo "    Set one up with: hermes config set provider <name>"
    echo ""
    echo "    Supported: deepseek, openai, anthropic, openrouter, and more."
    echo "    See: https://hermes-agent.nousresearch.com/docs"
    echo ""
    echo "    Continuing setup — you can configure the provider later."
    echo ""
fi

echo ""

# ─────────────────────────────────────────────────────────────
# Step 2: Profile
# ─────────────────────────────────────────────────────────────
echo -e "${CYAN}📦  Setting up Goblin Recon profile...${NC}"

if [ -d "$PROFILE_DIR" ]; then
    echo -e "    ℹ️  Profile exists — updating"
else
    if hermes profile create "$PROFILE_NAME" > /dev/null 2>&1; then
        echo -e "    ✅  Profile created: $PROFILE_NAME"
    else
        mkdir -p "$PROFILE_DIR"
        echo -e "    ⚠️  Hermes profile command failed; created profile directory fallback"
        echo -e "       If Hermes cannot launch this profile, run: hermes profile create $PROFILE_NAME"
    fi
fi

# ─────────────────────────────────────────────────────────────
# Step 3: SOUL.md
# ─────────────────────────────────────────────────────────────
if [ -f "$PROJECT_DIR/SOUL.md" ]; then
    cp "$PROJECT_DIR/SOUL.md" "$PROFILE_DIR/SOUL.md"
    echo -e "    ✅  SOUL.md installed"
else
    echo -e "${RED}    ❌  SOUL.md not found in project root${NC}"
    echo "    Expected at: $PROJECT_DIR/SOUL.md"
    exit 1
fi

# ─────────────────────────────────────────────────────────────
# Step 4: Skills
# ─────────────────────────────────────────────────────────────
mkdir -p "$SKILLS_DIR"

# Install goblin-recon operational skill
if [ -f "$PROJECT_DIR/skills/goblin-recon/SKILL.md" ]; then
    mkdir -p "$SKILLS_DIR/genx-marketing/goblin-recon"
    cp "$PROJECT_DIR/skills/goblin-recon/SKILL.md" "$SKILLS_DIR/genx-marketing/goblin-recon/SKILL.md"
    echo -e "    ✅  goblin-recon skill installed"
fi

# Install pipeline and reusable project skills
PIPELINE_SKILLS=(orchestrator trend-radar source-hunter moment-finder competitor-scout caption-tone email-hook)
for skill in "${PIPELINE_SKILLS[@]}"; do
    if [ -d "$PROJECT_DIR/skills/$skill" ]; then
        mkdir -p "$SKILLS_DIR/genx-marketing/$skill"
        cp -r "$PROJECT_DIR/skills/$skill"/* "$SKILLS_DIR/genx-marketing/$skill/"
        echo -e "    ✅  $skill installed"
    fi
done

# Skills are loaded by Hermes directly from the profile skills directory.
# No separate registration command is needed.

# Install project assets that skills call at runtime
for asset_dir in scripts templates config memory; do
    if [ -d "$PROJECT_DIR/$asset_dir" ]; then
        mkdir -p "$PROFILE_DIR/$asset_dir"
        cp -R "$PROJECT_DIR/$asset_dir/." "$PROFILE_DIR/$asset_dir/"
        echo -e "    ✅  $asset_dir installed"
    fi
done

# Cherry-picked marketing skills (from default Hermes profile)
CHERRY_PICKED=(competitor-profiling social-content copywriting content-strategy marketing-psychology)
DEFAULT_SKILLS="$HERMES_HOME/skills/desktop"

for skill in "${CHERRY_PICKED[@]}"; do
    if [ -d "$DEFAULT_SKILLS/$skill" ]; then
        mkdir -p "$SKILLS_DIR/desktop/$skill"
        cp -r "$DEFAULT_SKILLS/$skill"/* "$SKILLS_DIR/desktop/$skill/"
        echo -e "    ✅  $skill installed"
    else
        echo -e "    ⚠️  $skill not found in default skills"
    fi
done

# ─────────────────────────────────────────────────────────────
# Step 5: Configuration
# ─────────────────────────────────────────────────────────────
echo -e "    ⚙️  Configuring profile..."

CONFIG_WARNINGS=0
set_profile_config() {
    if ! hermes config set "$1" "$2" -p "$PROFILE_NAME" > /dev/null 2>&1; then
        echo -e "    ⚠️  Could not set $1; configure it manually if needed"
        CONFIG_WARNINGS=$((CONFIG_WARNINGS + 1))
    fi
}

# Auto-load the goblin-recon skill
set_profile_config skills.auto_load goblin-recon
if [ "$CONFIG_WARNINGS" -eq 0 ]; then
    echo -e "    ✅  Auto-load: goblin-recon"
fi

# Agent settings
set_profile_config agent.max_turns 90
set_profile_config terminal.timeout 300
echo -e "    ✅  Agent settings checked (max_turns=90, timeout=300)"

echo ""

# ─────────────────────────────────────────────────────────────
# Step 6: Environment (.env)
# ─────────────────────────────────────────────────────────────
echo -e "${CYAN}🔑  Checking API keys...${NC}"

if [ -f "$PROJECT_DIR/.env" ]; then
    echo -e "    ✅  .env file already exists"
    # Check if it's still the template (all keys commented out)
    uncommented=$(grep -c "^[^#].*=" "$PROJECT_DIR/.env" 2>/dev/null || echo 0)
    if [ "$uncommented" -eq 0 ]; then
        echo -e "${YELLOW}    ⚠️  .env looks like the template — no API keys filled in yet.${NC}"
        echo -e "    Edit $PROJECT_DIR/.env and add your keys before running scans."
    else
        echo -e "    ✅  $uncommented API key(s) found"
    fi
else
    if [ -f "$PROJECT_DIR/.env.example" ]; then
        cp "$PROJECT_DIR/.env.example" "$PROJECT_DIR/.env"
        echo -e "    ✅  .env created from .env.example"
        echo -e "${YELLOW}    ⚠️  Edit $PROJECT_DIR/.env and add your API keys before running scans.${NC}"
        echo ""
        echo -e "    Required for best results:"
        echo -e "      EXA_API_KEY      — semantic search"
        echo -e "      TAVILY_API_KEY   — research search"
        echo -e "      FIRECRAWL_API_KEY  — deep page extraction"
        echo -e "      SCRAPEGRAPH_API_KEY — structured data extraction"
        echo ""
    else
        echo -e "${RED}    ❌  No .env.example found — create .env manually${NC}"
    fi
fi

# Copy .env to Hermes profile so tools can find keys
if [ -f "$PROJECT_DIR/.env" ]; then
    mkdir -p "$PROFILE_DIR"
    cp "$PROJECT_DIR/.env" "$PROFILE_DIR/.env"
    echo -e "    ✅  .env copied to profile"
fi

echo ""

# ─────────────────────────────────────────────────────────────
# Step 7: Python Environment
# ─────────────────────────────────────────────────────────────
echo -e "${CYAN}🐍  Setting up Python environment...${NC}"

cd "$PROJECT_DIR"

if [ -d ".venv" ]; then
    echo -e "    ℹ️  Python venv already exists"
else
    uv venv > /dev/null 2>&1
    echo -e "    ✅  Python venv created"
fi

if [ -f "requirements.txt" ]; then
    uv pip install -r requirements.txt > /dev/null 2>&1
    echo -e "    ✅  Python dependencies installed"
else
    echo -e "    ⚠️  No requirements.txt found (skipping)"
fi

if [ -f "requirements-dev.txt" ]; then
    uv pip install -r requirements-dev.txt > /dev/null 2>&1
    echo -e "    ✅  Python dev/test dependencies installed"
fi

uv pip install -e . > /dev/null 2>&1
echo -e "    ✅  Goblin Recon Python tools installed"

echo ""

# ─────────────────────────────────────────────────────────────
# Step 8: Verify
# ─────────────────────────────────────────────────────────────
echo -e "${CYAN}🧪  Verifying...${NC}"

ERRORS=0

# Profile directory
if [ -d "$PROFILE_DIR" ]; then
    echo -e "    ✅  Profile directory"
else
    echo -e "${RED}    ❌  Profile directory missing${NC}"
    ERRORS=$((ERRORS + 1))
fi

# SOUL.md
if [ -f "$PROFILE_DIR/SOUL.md" ]; then
    echo -e "    ✅  SOUL.md"
else
    echo -e "${RED}    ❌  SOUL.md missing${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Skills count
SKILL_COUNT=$(find "$SKILLS_DIR" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
if [ "$SKILL_COUNT" -gt 0 ]; then
    echo -e "    ✅  Skills ($SKILL_COUNT installed)"
else
    echo -e "${YELLOW}    ⚠️  No skills found${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Python scripts
SCRIPT_COUNT=$(find "$PROJECT_DIR/scripts" -name "*.py" 2>/dev/null | wc -l | tr -d ' ')
if [ "$SCRIPT_COUNT" -gt 0 ]; then
    echo -e "    ✅  Scripts ($SCRIPT_COUNT Python utilities)"
else
    echo -e "${YELLOW}    ⚠️  No Python scripts found${NC}"
fi

echo ""

# ─────────────────────────────────────────────────────────────
# Done
# ─────────────────────────────────────────────────────────────
if [ "$ERRORS" -gt 0 ]; then
    echo -e "${YELLOW}${BOLD}⚠️  Setup completed with $ERRORS warning(s).${NC}"
    echo -e "${DIM}    Check the messages above and fix any issues.${NC}"
    echo ""
fi

echo -e "${DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}${BOLD}✅  Goblin Recon is ready.${NC}"
echo ""
echo -e "    Start:   ${CYAN}hermes --profile goblin-recon${NC}"
echo ""
echo -e "    Try:     ${CYAN}\"run social pulse\"${NC}"
echo -e "             ${CYAN}\"find clips about AI agents\"${NC}"
echo -e "             ${CYAN}\"what's trending on Instagram\"${NC}"
echo ""
echo -e "${DIM}    Docs:    GETTING_STARTED.md${NC}"
echo -e "${DIM}    Config:  config/${NC}"
echo -e "${DIM}    Scripts: scripts/${NC}"
echo -e "${DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
