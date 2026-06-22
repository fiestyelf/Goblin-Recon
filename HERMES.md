# Hermes — Goblin Recon

Goblin Recon runs on Hermes Agent as the local operator shell. This file is the **#1 priority project context file** — Hermes loads it before `AGENTS.md` and injects it into every session as "Project Context." It is the definitive reference for operating Goblin Recon on Hermes.

## Quick Start

```bash
hermes --profile goblin-recon
```

Working directory: the project root (`goblin-recon/`). All paths below are relative to it unless noted.

## Context File Priority

Hermes discovers and loads context files in this order (first match wins per category):

| Priority | File | Purpose | Loaded |
|----------|------|---------|--------|
| 1 | `HERMES.md` | Project Hermes configuration (this file) | Session startup |
| 2 | `AGENTS.md` | Agent behavior rules, workflows, scoring | Session startup |
| — | `SOUL.md` | Global brand identity + voice (loaded independently) | Session startup |

`HERMES.md` tells Hermes **how to run**. `AGENTS.md` tells the agent **how to behave**. `SOUL.md` tells the agent **who it is**.

## Profile Configuration

```bash
hermes config set model.provider <approved-provider> -p goblin-recon
hermes config set model.default <latest-approved-llm> -p goblin-recon
hermes config set agent.max_turns 90 -p goblin-recon
hermes config set terminal.timeout 120 -p goblin-recon
hermes config set skills.auto_load goblin-recon -p goblin-recon
```

Use the latest approved LLM model for the active provider. Never paste or commit API keys — use Hermes secrets or the project `.env`.

## Environment Variables

Create a `.env` file at the project root (ignored by Git). `mcp.json` sources this file before starting API-key MCPs, including non-native/remote MCPs.

| Variable | Required? | Used By |
|----------|-----------|---------|
| `EXA_API_KEY` | Required | `exa` remote MCP |
| `TAVILY_API_KEY` | Required | `tavily` MCP |
| `FIRECRAWL_API_KEY` | Required | `firecrawl` MCP |
| `SCRAPEGRAPH_API_KEY` | Required | `scrapegraph` remote MCP header |
| `REPLICATE_API_TOKEN` | Optional | `replicate` MCP and local carousel renderer |

Keys live in `.env` or Hermes secrets only. Never in `config/*.yaml`, `README.md`, `AGENTS.md`, skill files, or chat messages. See `API_KEYS.md` for the full key handling policy.

## MCP Servers

Configured in `mcp.json` at the project root. Ten servers are active. For any MCP that needs a key, put the key in `.env`; `mcp.json` loads it before the server starts.

### Active (10 servers)

| Server | Loads As | Key | What It Does |
|--------|----------|-----|--------------|
| **exa** | remote MCP via `mcp-remote` | `EXA_API_KEY` | Semantic search (primary). Query by meaning, not keywords. |
| **tavily** | npm MCP | `TAVILY_API_KEY` | AI-optimized search (fallback). |
| **firecrawl** | npm MCP | `FIRECRAWL_API_KEY` | Clean markdown extraction from any URL. |
| **scrapegraph** | remote MCP via `mcp-remote` | `SCRAPEGRAPH_API_KEY` | Structured data extraction with AI. |
| **replicate** | npm MCP | `REPLICATE_API_TOKEN` | Carousel visual/background layer generation only; final text is rendered locally with Pillow. |
| **ghost-browser** | `uvx` MCP | — | Browser automation helper for public pages. |
| **youtube-transcript** | npm MCP | — | YouTube transcript extraction. |
| **memory** | npm MCP | — | Knowledge graph for brand-gate decisions and recurring patterns. |
| **fetch** | `uvx` MCP | — | Public web extraction helper (supplementary). |
| **sequential-thinking** | npm MCP | — | Structured reasoning for scoring and source validation. |

No optional MCPs are configured right now. Add one only when a workflow actually needs it.

### MCP Tool Fallback Chain

When an MCP tool fails, fall back in this order:
```
MCP tool → firecrawl_search → tavily_search → web_search + web_extract (Hermes built-in)
```

Always try MCP first. Always have a fallback. Never return "I couldn't do this" without attempting Hermes built-in tools.

## Skills Catalog

Ten localized skills in `skills/`. All are auto-synced to the profile.

| Skill | Triggers On | What It Does |
|-------|------------|--------------|
| **goblin-recon** | Auto-loaded | Router. Picks the smallest useful workflow for any command. |
| **orchestrator** | Internal routing | Routes requests to one primary workflow, runs the sequence. |
| **trend-radar** | Social Pulse, scans | Finds and scores current AI/social content signals. |
| **source-hunter** | Clip Mine | Finds public source videos/pages for a trend. |
| **moment-finder** | Clip Mine | Extracts 15-60s clip moments from transcripts. |
| **security-rail** | All user-facing output | Final safety, source, claim, and usefulness gate. |
| **caption-tone** | Caption tasks | Writes platform-ready GenX captions and descriptions. |
| **competitor-scout** | Competitor scans | Public competitor scan → cell-ready moves. |
| **email-hook** | Email tasks | Generates and scores outbound subject lines and openers. |
| **carousel-generator** | Carousel tasks | Builds editable carousel layers and social images. |

See `skills/<name>/SKILL.md` for the full content of any skill.

## Source of Truth

| Need | File |
|------|------|
| Agent rules + workflows | `AGENTS.md` |
| Team commands | `COMMANDS.md` |
| Architecture | `ARCHITECTURE.md` |
| MCP servers | `mcp.json` |
| Setup guide | `docs/ops/getting-started.md` |
| Full instructions | `docs/ops/instructions.md` |
| Hermes approvals | `docs/hermes/approvals.md` |
| API key policy | `API_KEYS.md` |
| Security policy | `SECURITY.md` |
| Legal guardrails | `docs/security/legal-guardrails.md` |
| Brand voice config | `config/brand-voice.yaml` |
| Source/scoring config | `config/sources.yaml`, `config/scoring.yaml` |
| Competitor config | `config/competitors.yaml` |
| Content sources | `config/sources.yaml` → `sources.content_sources` |
| Carousel memory | `memory/carousel/` |
| Carousel outputs | `vault/carousels/` |
| Replicate integration | `mcp.json` plus `REPLICATE_API_TOKEN` in `.env` |

## Boundaries

### Allowed (no approval needed)
- Read, search, and edit project files
- Run local tests, checks, and Python tools
- Create vault reports, briefs, carousel assets, and local exports
- Use approved public sources (MCP or Hermes built-in)
- Update local memory (`memory/`, `vault/`)

### Needs explicit approval
- Reveal or use API keys, tokens, or credentials
- Set up paid services or external accounts
- Bypass login, paywall, captcha, robots.txt, or rate limits
- Publish, post, email, DM, or contact anyone externally
- Delete important source data
- Commit or push to Git
- Rewrite Git history or force-push

## Quick Health Check

```bash
cd goblin-recon
bash scripts/dev_check.sh
```

Runs: pytest (85 tests), secret scanner, project structure validation, dead file check. All must pass before committing.

### Verify Profile Identity

```bash
hermes --profile goblin-recon "who are you and who do you work for?"
```

Should respond as Goblin Recon at GenX Academy.

## Maintenance — Syncing After Editing Project Files

When you edit project files in VS Code (or any editor) and the Hermes profile needs to catch up:

```bash
# 1. Check what changed
git diff --stat

# 2. Sync critical files to profile
cp SOUL.md ~/.hermes/profiles/goblin-recon/SOUL.md
cp AGENTS.md ~/.hermes/profiles/goblin-recon/AGENTS.md
cp HERMES.md ~/.hermes/profiles/goblin-recon/HERMES.md

# 3. Sync all skills
for skill in caption-tone competitor-scout email-hook goblin-recon \
             moment-finder orchestrator security-rail source-hunter \
             trend-radar carousel-generator; do
  mkdir -p ~/.hermes/profiles/goblin-recon/skills/genx-marketing/$skill
  cp skills/$skill/SKILL.md ~/.hermes/profiles/goblin-recon/skills/genx-marketing/$skill/SKILL.md
done

# 4. Verify all match
diff SOUL.md ~/.hermes/profiles/goblin-recon/SOUL.md && echo "MATCH" || echo "DIFF"
diff AGENTS.md ~/.hermes/profiles/goblin-recon/AGENTS.md && echo "MATCH" || echo "DIFF"
diff HERMES.md ~/.hermes/profiles/goblin-recon/HERMES.md && echo "MATCH" || echo "DIFF"
```

Or run `bash scripts/setup.sh` which does all of this in one command.

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Agent doesn't know it's Goblin Recon | `skills.auto_load` not set | `hermes config set skills.auto_load goblin-recon -p goblin-recon` |
| MCP tools return errors | Missing `.env` keys | Check `.env` has `EXA_API_KEY`, `TAVILY_API_KEY`, `FIRECRAWL_API_KEY`, `SCRAPEGRAPH_API_KEY` |
| Replicate carousel generation falls back to gradients | Missing or invalid Replicate token | Add `REPLICATE_API_TOKEN` to `.env` or accept local fallback backgrounds; the renderer uses this env var directly, not the MCP process |
| Skills not found | Skills not synced to profile | Run sync procedure above or `bash scripts/setup.sh` |
| `web_search` / `web_extract` fail | MCP fallback issue | These are Hermes built-in tools — they work without MCP keys |
| Instagram/TikTok blocked | Platform access limits | Normal — use manual assisted input or switch to Fast Scan |
| YouTube "Before you continue" dialog | Cookie wall | Click reject/accept in browser, retry once; do not use personal accounts |
| Transcript in wrong language | Non-English captions | GenX requires English-only; fall back to alternative source |
| Search returns zero results after 3 attempts | Topic too narrow or obscure | Stop and ask user for a URL, screenshot, or creator name |
| `delegate_task` produces wrong output | Subagents don't inherit context | Pass explicit source URLs, query limits, blocked-source rules, brand rules, and expected output fields |

## Ponytail Rule

Prefer the smallest working path:

```text
standard tool → existing script → tiny helper → only then new workflow
```

Do not add another config file, doc page, or skill unless it removes more confusion than it creates.

---

*This file is version-controlled at the project root. Hermes discovers it at session startup and injects it as the #1 priority context file. Edit it when project-level Hermes configuration changes.*
