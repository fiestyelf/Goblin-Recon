#!/usr/bin/env bash
# =============================================================================
# Goblin Recon — MCP Setup Script
# =============================================================================
# Run this once after cloning the repo:
#
#   git clone <repo-url>
#   cd goblin-recon
#   cp .env.example .env
#   # edit .env → add EXA_API_KEY, TAVILY_API_KEY, FIRECRAWL_API_KEY, SCRAPEGRAPH_API_KEY
#   bash scripts/setup-mcp.sh
#
# What it does:
#   1. Creates the Hermes profile 'goblin-recon' (safe to re-run)
#   2. Appends the portable MCP config to the profile's config.yaml
#   3. Enables the required Hermes toolsets
#   4. Verifies the config and prints next steps
# =============================================================================

set -euo pipefail

# Colours for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

PROFILE="goblin-recon"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
MCP_CONFIG="$PROJECT_DIR/config/hermes-mcp.yaml"

echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}  Goblin Recon — MCP Setup${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo ""

# ------------------------------------------------------------------
# 1. Verify we're in the right directory
# ------------------------------------------------------------------
if [ ! -f "$MCP_CONFIG" ]; then
  echo -e "${RED}✖ config/hermes-mcp.yaml not found${NC}"
  echo "  Run this script from the goblin-recon project root."
  echo "  Expected: $MCP_CONFIG"
  exit 1
fi
echo -e "${GREEN}✓ Project directory: $PROJECT_DIR${NC}"

# ------------------------------------------------------------------
# 2. Check for hermes CLI
# ------------------------------------------------------------------
if ! command -v hermes &> /dev/null; then
  echo -e "${RED}✖ hermes CLI not found${NC}"
  echo "  Install Hermes Agent first: https://hermes-agent.nousresearch.com/docs"
  exit 1
fi
echo -e "${GREEN}✓ hermes CLI found: $(hermes --version 2>&1 | head -1)${NC}"

# ------------------------------------------------------------------
# 3. Create the Hermes profile (idempotent)
# ------------------------------------------------------------------
# Resolve the real home directory (some Hermes profiles override $HOME)
# Works on macOS and Linux
if command -v dscl &>/dev/null; then
  REAL_HOME=$(dscl . -read /Users/"$(whoami)" NFSHomeDirectory 2>/dev/null | awk '{print $2}')
elif command -v getent &>/dev/null; then
  REAL_HOME=$(getent passwd "$(whoami)" | cut -d: -f6)
else
  REAL_HOME="$HOME"
fi
HERMES_PROFILES_DIR="$REAL_HOME/.hermes/profiles"

if [ -d "$HERMES_PROFILES_DIR/$PROFILE" ]; then
  echo -e "${GREEN}✓ Profile '$PROFILE' already exists${NC}"
else
  echo "  Creating Hermes profile '$PROFILE'..."
  hermes profile create "$PROFILE"
  echo -e "${GREEN}✓ Profile '$PROFILE' created${NC}"
fi

# ------------------------------------------------------------------
# 4. Append MCP config to profile's config.yaml
# ------------------------------------------------------------------
PROFILE_DIR="$HERMES_PROFILES_DIR/$PROFILE"
CONFIG_FILE="$PROFILE_DIR/config.yaml"

if [ ! -f "$CONFIG_FILE" ]; then
  echo -e "${RED}✖ Profile config not found at $CONFIG_FILE${NC}"
  echo "  Run: hermes profile create $PROFILE"
  exit 1
fi

# Check if MCP servers are already appended (idempotent guard)
if grep -q "mcp_servers:" "$CONFIG_FILE"; then
  echo -e "${YELLOW}⚠ MCP servers already present in $CONFIG_FILE${NC}"
  echo "  Remove the 'mcp_servers:' block manually if you want to re-apply."
else
  echo "" >> "$CONFIG_FILE"
  cat "$MCP_CONFIG" >> "$CONFIG_FILE"
  echo -e "${GREEN}✓ MCP servers appended to $CONFIG_FILE${NC}"
fi

# ------------------------------------------------------------------
# 5. Enable required Hermes toolsets
# ------------------------------------------------------------------
echo "  Enabling Hermes toolsets..."
TOOLS=(web browser file terminal memory)
for tool in "${TOOLS[@]}"; do
  hermes tools enable "$tool" -p "$PROFILE" 2>/dev/null || true
done
echo -e "${GREEN}✓ Toolsets enabled${NC}"

# ------------------------------------------------------------------
# 6. Check .env exists — REQUIRED API KEYS
# ------------------------------------------------------------------
REQUIRED_KEYS=(
  "EXA_API_KEY:Semantic web search for trend discovery (exa.ai)"
  "TAVILY_API_KEY:Backup AI-optimised web search (tavily.com)"
  "FIRECRAWL_API_KEY:Extract web pages to clean markdown (firecrawl.dev)"
  "SCRAPEGRAPH_API_KEY:AI-powered structured data extraction (scrapegraphai.com)"
)

echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║          REQUIRED API KEYS — MCP Servers                ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

if [ -f "$PROJECT_DIR/.env" ]; then
  ALL_PRESENT=true
  for entry in "${REQUIRED_KEYS[@]}"; do
    key="${entry%%:*}"
    desc="${entry#*:}"
    value=$(grep -E "^${key}=" "$PROJECT_DIR/.env" 2>/dev/null | head -1 | cut -d= -f2-)
    if [ -z "$value" ] || [ "$value" = "\"\"" ] || [ "$value" = "''" ]; then
      echo -e "  ${RED}✖ $key${NC}"
      echo -e "    ${YELLOW}→ $desc${NC}"
      echo -e "    ${YELLOW}→ Not set. Goblin Recon will run with reduced capabilities.${NC}"
      echo ""
      ALL_PRESENT=false
    else
      echo -e "  ${GREEN}✓ $key${NC}  — ${desc}"
    fi
  done
  echo ""
  if [ "$ALL_PRESENT" = true ]; then
    echo -e "  ${GREEN}All 4 API keys found. Goblin Recon runs at full strength.${NC}"
  else
    echo -e "  ${YELLOW}⚠ Some keys are missing. Goblin Recon will still work${NC}"
    echo -e "  ${YELLOW}  but MCP servers without keys won't connect.${NC}"
  fi
else
  echo -e "  ${RED}✖ No .env file found.${NC}"
  echo ""
  echo -e "  ${YELLOW}Goblin Recon REQUIRES the following API keys to function:${NC}"
  for entry in "${REQUIRED_KEYS[@]}"; do
    key="${entry%%:*}"
    desc="${entry#*:}"
    echo -e "  ${YELLOW}  • $key — ${desc}${NC}"
  done
  echo ""
  echo -e "  Run: cp .env.example .env"
  echo -e "  Then add your API keys before starting Goblin Recon."
fi

echo ""
echo -e "${YELLOW}  Where to get these keys (free tiers available):${NC}"
echo -e "  ${YELLOW}  • EXA_API_KEY       → https://dashboard.exa.ai/api-keys${NC}"
echo -e "  ${YELLOW}  • TAVILY_API_KEY    → https://app.tavily.com/home${NC}"
echo -e "  ${YELLOW}  • FIRECRAWL_API_KEY → https://www.firecrawl.dev/app/api-keys${NC}"
echo -e "  ${YELLOW}  • SCRAPEGRAPH_API_KEY → https://scrapegraphai.com/ (dashboard)${NC}"
echo ""

# ------------------------------------------------------------------
# 7. Done — print next steps
# ------------------------------------------------------------------
echo ""
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}  Setup Complete${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo ""
echo "  ════════════════════════════════════════════════════════════════"
echo -e "  ${YELLOW}IMPORTANT: Before running any Goblin Recon commands,${NC}"
echo -e "  ${YELLOW}make sure you have added your API keys to .env first.${NC}"
echo -e "  ${YELLOW}Without them, the MCP servers won't connect and Goblin${NC}"
echo -e "  ${YELLOW}Recon will have limited search and extraction ability.${NC}"
echo "  ════════════════════════════════════════════════════════════════"
echo ""
echo "  1. cd $PROJECT_DIR"
echo "  2. hermes -p $PROFILE"
echo ""
echo "  Hermes will load the profile with 62 MCP tools across 6 servers."
echo "  The bash-based servers (exa, tavily, firecrawl, scrapegraph)"
echo "  read .env from your working directory at startup."
echo ""
echo -e "${CYAN}  Optional: install as a launchd service${NC}"
echo "    hermes gateway start -p $PROFILE"
echo ""
