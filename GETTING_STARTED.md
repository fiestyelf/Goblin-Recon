# Goblin Recon Quick Start

Use this guide when you already have the Goblin Recon folder and want to run it with Hermes.

## Prerequisites

- Hermes installed. Check with `hermes --version`.
- Python 3.12 or newer.
- A model/API provider available to Hermes, such as OpenAI, Anthropic, DeepSeek, Google, or a local provider.
- Access to this folder: `goblin-recon/`.

## 1. Open The Project Folder

Run all setup commands from the project root. Replace the path with wherever you keep the repo locally:

```bash
cd "/path/to/goblin-recon"
```

## 2. Run One-Command Setup

```bash
bash scripts/setup.sh
```

This sets up the full local workspace:

- Creates or updates the `goblin-recon` Hermes profile.
- Installs `SOUL.md` into the profile.
- Installs bundled Goblin Recon skills.
- Sets safe profile defaults such as skill auto-load and terminal timeout.
- Creates `.venv/` and installs Python dependencies for transcript and scoring tools.
- Verifies the expected profile files, skills, and scripts are present.

Hermes profiles are stored outside the repo at:

```text
~/.hermes/profiles/goblin-recon/
```

If setup warns that profile creation failed, run this manually and then rerun setup:

```bash
hermes profile create goblin-recon
```

## 3. Choose A Model Provider

Pick whichever provider/model your company has approved. Every provider below offers options — stronger models improve brand judgment and source verification, lighter models work for bulk scanning. You decide what fits each task.

| Provider | Available Models | Strengths |
|---|---|---|
| OpenAI | `gpt-4o`, `gpt-4o-mini` | Strong reasoning, source review, polished briefs |
| Anthropic | `claude-sonnet-4-20250514`, `claude-3-5-haiku-20241022` | Brand-sensitive judgment, long-context review |
| DeepSeek | `deepseek-v4-pro`, `deepseek-v4-flash` | Cost-effective scanning, structured reports |
| Google | `gemini-2.5-pro`, `gemini-2.0-flash` | Large-context source review, fast trend sweeps |
| Local/Ollama | `qwen2.5`, `llama3.1`, or your approved local model | Private/offline drafts, low-cost experiments |

Example for OpenAI:

```bash
hermes -p goblin-recon config set model.provider openai
hermes -p goblin-recon config set model.default gpt-4o
```

If your provider needs a key, set it through Hermes secrets or your approved local secret method. Example:

```bash
hermes -p goblin-recon secrets set OPENAI_API_KEY
```

Never paste API keys into chat.

## 4. Optional MCP Servers

MCP servers are optional plugins that give Hermes/Goblin Recon extra abilities. They should not replace the existing skills. Use them as helpers only when they improve output without making the workflow harder.

Priority means install order: start with the lowest-risk tool that gives the most value, then add more specialized tools only when needed.

| Priority | MCP Server | Install / Command | Why It Matters | Status |
|---|---|---|---|---|
| 1 | Memory | `npx -y @modelcontextprotocol/server-memory` | Stores approved examples and recurring patterns better than flat notes | Recommended first |
| 2 | Fetch | `uvx mcp-server-fetch` | Cleaner public web extraction for source review | Recommended second |
| 3 | Scrapling | `pip install "scrapling[ai]"` | Better extraction from JavaScript-heavy public pages | Optional, use only when normal extraction fails |
| 4 | Notion / Sheets | approved workspace integration | Tracks approved clips from brief to production | Optional after approval |
| 5 | Brave Search | provider-approved MCP server | More structured search results with dates and snippets | Optional |
| 6 | GPT Researcher | approved local/MCP setup | Deep research helper for difficult topics | Optional sub-agent only |
| 7 | TrendRadar | approved local/MCP setup | Extra trend source ideas; do not replace Layer 1 | Optional reference/input only |

This repo includes a starter `mcp.json`. Review it before enabling any server. Keep manual approval on, and do not connect private accounts unless an admin approves the exact integration and scope.

FunASR is intentionally not part of the first setup. Start with YouTube captions through `goblin_recon.tools.youtube_tool`. Add speech recognition later only if too many useful videos lack captions.

## 5. Enable Required Tools

```bash
hermes tools enable web -p goblin-recon
hermes tools enable browser -p goblin-recon
hermes tools enable file -p goblin-recon
hermes tools enable terminal -p goblin-recon
hermes tools enable memory -p goblin-recon
hermes tools enable session_search -p goblin-recon
hermes tools enable skills -p goblin-recon
```

Keep manual approval mode on. Deny requests to access private accounts, personal cookies, paywalled sources, captchas, or files outside the project unless an admin approves the exact use.

## 6. Launch Goblin Recon

```bash
hermes -p goblin-recon
```

Send this first message:

```text
Load this folder as the Goblin Recon agent. Follow AGENTS.md, SECURITY.md, LEGAL_GUARDRAILS.md, config/security.yaml, memory/brand-rules.md, config/brand-voice.yaml, and the skills under skills/. Use only public sources unless an integration is explicitly approved. Do not ask for or reveal API keys. Start in manual approval mode.
```

## Daily Commands

- `find trending AI stories` - Run Trend Radar.
- `find sources for [topic]` - Run Source Hunter.
- `find the moment in [video URL]` - Run Moment Finder.
- `run full scan` - Run the full trend-to-clip pipeline.
- `run competitor scan` - Run Competitor Scout.
- `run brand check on [content]` - Validate content against GenX brand rules.
- `what did we find yesterday?` - Search previous session memory.

## Content Tracking

Approved clips should be tracked in Notion or Google Sheets after human approval. The default recommendation is Notion if the team wants a database-style production board, or Google Sheets if the team wants the simplest shared tracker.

Use `config/content-tracker.yaml` as the source of truth for fields and status names. Do not send briefs to Notion or Sheets until the integration is explicitly approved and the required secret is set through Hermes secrets or an approved local secret method.

Recommended statuses:

| Status | Meaning |
|---|---|
| `pending_review` | Found by Goblin Recon, waiting for human decision |
| `approved` | Approved by human gate |
| `in_production` | Being edited or prepared |
| `scheduled` | Scheduled for posting |
| `posted` | Published |
| `shelved` | Rejected or paused |

## What This Folder Provides

- `AGENTS.md` - Main agent rules.
- `skills/` - Trend Radar, Source Hunter, Moment Finder, Competitor Scout, Caption Tone, and Orchestrator.
- `config/` - Sources, scoring, security, brand voice, and integrations.
- `memory/` - Brand rules and ongoing memory files.
- `templates/` - Output formats for reports and briefs.
- `goblin_recon/tools/` - Importable tool modules.
- `scripts/` - Standalone setup, secret scan, and query helpers.

## Making It Better

Use this roadmap incrementally. Do not add complexity until the current pipeline is producing useful clips.

| Area | Improvement | When To Add |
|---|---|---|
| Scoring | Store approved examples in MCP Memory for pattern learning | After 10+ approved clips |
| Trend Radar | Adapt TrendRadar ideas: RSS feeds, keyword filters, multi-platform alerts | When daily scans miss obvious trends |
| Source Hunter | Use GPT Researcher as an optional deep-research helper | When a topic is important but sources are thin |
| Moment Finder | Add FunASR transcription/emotion detection | When captionless videos become a regular blocker |
| Competitor Scout | Use Scrapling for public pages that normal extraction cannot read | When competitor pages are JavaScript-heavy |
| Operations | Send approved clips to Notion or Sheets | When production tracking becomes manual overhead |
| Brand | Review approved/shelved clips monthly and update `memory/brand-rules.md` | Every 20-30 decisions |

## Troubleshooting

- `Profile not found`: run `hermes profile create goblin-recon`.
- Python dependency errors: run `bash scripts/setup.sh` again.
- Model does not respond: confirm the provider/model config and API key.
- Skills do not load: confirm you launched Hermes from the `goblin-recon/` folder and enabled `skills`.
- Tool approval confusion: read `HERMES_APPROVALS.md`.
