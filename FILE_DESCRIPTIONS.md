# Goblin Recon — File Descriptions

One-line purpose for every tracked file and folder in this repo.

---

## Start Here

| File | Job |
|---|---|
| `SOUL.md` | Hermes profile identity — compact operating memory loaded into the goblin-recon profile. |
| `AGENTS.md` | Agent rulebook — identity, behavior, source verification, brand rules, security guardrails. |
| `ARCHITECTURE.md` | Professional system map — router, workflows, scan modes, tool policy, social extraction ladder, and memory policy. |
| `COMMANDS.md` | Plain-language command guide for scan modes, Clip Mine, Clip Vault, captions, email hooks, and setup commands. |
| `GETTING_STARTED.md` | Quickstart for new users who already have Hermes. |
| `mcp.json` | Optional MCP helper server config. Disabled until approved. |

## Core Docs

| File | Job |
|---|---|
| `README.md` | Project overview. One-liner setup, commands, and pointers to detailed guides. |
| `FILE_DESCRIPTIONS.md` | This file — one-line purpose for every file and folder. |
| `INSTRUCTIONS.md` | Step-by-step setup and daily workflow guide for the GenX Academy marketing team. |

## Security, Legal, and API Docs

| File | Job |
|---|---|
| `SECURITY.md` | Security policy — secrets, public-source rules, retention, incident response. |
| `API_KEYS.md` | Safe API key storage, rotation, and leak response. |
| `API_KEYS_TODO.md` | Checklist for optional API keys that still need owner approval/configuration. |
| `SOCIAL_API_SETUP.md` | Guide for adding approved social API keys (YouTube, Reddit, X/Twitter, etc.). |
| `LEGAL_GUARDRAILS.md` | Platform, copyright, competitor research, and publishing rules. |
| `HERMES_APPROVALS.md` | Which Hermes tool permissions to approve or deny. |

## Repository Safety

| File | Job |
|---|---|
| `.gitignore` | Blocks secrets, environments, caches, logs, docs/, and vault outputs from being committed. |
| `.env.example` | Safe template showing environment variable names for optional API keys. |

## Python Project and Setup

| File | Job |
|---|---|
| `requirements.txt` | Pinned Python dependencies. |
| `requirements-dev.txt` | Pinned developer/test dependencies for local release checks. |
| `pyproject.toml` | Python project metadata for `uv`. |
| `scripts/setup.sh` | One-command setup for Hermes profile, SOUL.md, skills, profile defaults, Python venv, and dependencies. |
| `conftest.py` | Pytest path setup so tests can import the local `goblin_recon` package. |

## Config Files

| File | Job |
|---|---|
| `config/sources.yaml` | Trend source definitions, scan modes, social extraction policy, and normalized social record fields. Used by Trend Radar. |
| `config/scoring.yaml` | Scoring weights and thresholds for all three layers and the brand gate. |
| `config/brand-voice.yaml` | Brand voice rules, blacklist, brand gate thresholds, visual rules. |
| `config/email-campaigns.yaml` | Email campaign types mapped to triggers, tones, CTAs, and subject formulas. |
| `config/email-guardrails.yaml` | Email quality guardrails for spam triggers, filler openers, CTAs, and GenX subject rules. |
| `config/content-sources.yaml` | YouTube channels, Instagram accounts, hashtags, and topic patterns for Source Hunter. |
| `config/competitors.yaml` | Empty template for competitor tracking. |
| `config/security.yaml` | Machine-readable security defaults — public-only sources, rate limits, human review. |
| `config/integrations.yaml` | Registry of optional integrations (all disabled by default). |
| `config/social-extraction.yaml` | Platform-by-platform social extraction playbook for approved APIs, public access, and manual assisted intake. |
| `config/content-tracker.yaml` | Optional Notion/Sheets content tracker config. Disabled by default. |

## Skills

| File | Job |
|---|---|
| `skills/orchestrator/SKILL.md` | Pipeline driver — runs Trend Radar → Source Hunter → Moment Finder → Human Gate. |
| `skills/trend-radar/SKILL.md` | Layer 1 — finds and scores trending AI stories. |
| `skills/source-hunter/SKILL.md` | Layer 2 — finds YouTube/Instagram sources for a trend or topic. |
| `skills/moment-finder/SKILL.md` | Layer 3 — extracts 15-60s clip moments from transcripts. |
| `skills/competitor-scout/SKILL.md` | Standalone competitor/campaign research — pricing, features, messaging. |
| `skills/caption-tone/SKILL.md` | Reusable caption/description skill with platform formats and tone variants. |
| `skills/email-hook/SKILL.md` | Reusable outbound email subject/opening generator with automated quality-gate scoring. |
| `skills/goblin-recon/SKILL.md` | Operational skill — setup, commands, pipeline workflow, scoring, and release pitfalls. |

## Scripts

| File | Job |
|---|---|
| `scripts/setup.sh` | One-command local setup. Creates/updates the Hermes profile, installs project skills, and prepares Python tooling. |
| `scripts/check_secrets.py` | Scans the repo for accidental API keys, tokens, or webhooks. |
| `scripts/dev_check.sh` | Local verification wrapper for tests and safety checks before committing. |
| `goblin_recon.__init__` | Package marker for importable Goblin Recon Python modules. |
| `goblin_recon.tools.__init__` | Tool package marker for Python tool modules. |
| `goblin_recon.tools.brand_gate` | Checks GenX-written copy against the brand blacklist and nuance-word rules. |
| `goblin_recon.tools.youtube_tool` | Pulls public YouTube captions/transcripts with timestamps. |
| `goblin_recon.tools.clip_extractor` | Validates video URLs and clip boundaries, returns clip metadata. |
| `goblin_recon.tools.extract_clip` | Compatibility entry point for clip URL extraction. |
| `goblin_recon.tools.scoring` | Calculates engagement velocity scores for trends/sources. |
| `goblin_recon.tools.score_engagement` | Compatibility entry point for engagement velocity scoring. |
| `goblin_recon.tools.social_intake` | Normalizes approved API, public browser, or manual social observations into one schema before scoring. |
| `goblin_recon.tools.clip_store` | Stores approved/shelved Clip Mine records in local SQLite for cross-session lookup and dedup. |
| `goblin_recon.tools.email_gate` | Scores outbound email drafts across attention, psychological fit, brand voice, guardrails, and campaign alignment. |
| `goblin_recon.tools.web_scraper` | Lightweight public web page fetch helper used for allowed public-source extraction. |
| `scripts/query_clips.py` | CLI for searching stored clips, updating statuses, and exporting clip briefs. |

## Templates

| File | Job |
|---|---|
| `templates/trend-report.md` | Deprecated reference. Use `templates/social-pulse-report.md` for trend reports. |
| `templates/social-pulse-report.md` | Current Social Pulse and trend-report template. |
| `templates/clip-mine-brief.md` | Primary output format for Clip Mine editor-ready briefs. |
| `templates/content-brief.md` | Deprecated reference for standalone planning briefs. Prefer `templates/social-pulse-report.md`. |
| `templates/competitor-report.md` | Output format for competitor intelligence reports. |

## Memory Files

| File | Job |
|---|---|
| `memory/trend-history.md` | Stores past trends for deduplication. Starts empty with example format. |
| `memory/identity.md` | Stable project identity memory for Goblin Recon and GenX Academy positioning. |
| `memory/brand-rules.md` | Operational brand memory — condensed from local-only source material. All skills load this for brand gate checks. |
| `memory/competitor-snapshots.md` | Stores competitor snapshots for change detection. Starts empty with example format. |
| `memory/content-performance.md` | Stores content performance data for future scoring improvements. Starts empty. |
| `memory/decisions/.gitkeep` | Keeps the decisions memory folder in Git. Actual decision logs are local/runtime outputs. |
| `memory/feedback/.gitkeep` | Keeps the feedback memory folder in Git. Actual feedback records are local/runtime outputs. |
| `memory/metrics/.gitkeep` | Keeps the metrics memory folder in Git. Actual performance metrics are local/runtime outputs. |

## Vault Folders

| Path | Job |
|---|---|
| `vault/intake/.gitkeep` | Keeps the intake folder in Git. Actual raw intake files are local-only and ignored. |
| `vault/briefs/.gitkeep` | Keeps the briefs folder in Git. Actual briefs are local outputs and ignored. |
| `vault/reports/.gitkeep` | Keeps the reports folder in Git. Actual reports are local outputs and ignored. |

## Tests

| File | Job |
|---|---|
| `tests/test_scripts.py` | Unit tests for clip extraction, transcript validation, and scoring. |
| `tests/test_social_intake.py` | Unit tests for social signal platform inference, normalization, and JSONL storage. |
| `tests/test_clip_store.py` | Unit tests for persistent clip storage, duplicate detection, and status updates. |
| `tests/test_query_clips.py` | CLI tests for stored clip search and brief export. |
| `tests/test_check_brand.py` | Unit tests for brand-gate blacklist and nuance-word behavior. |
| `tests/test_check_secrets.py` | Unit tests for secret-pattern detection and safe placeholders. |
| `tests/test_email_gate.py` | Unit tests for email-gate pass/reject scoring and emoji-free feedback. |
| `tests/test_pipeline_integration.py` | Contract tests for clip extraction, scoring, and brand-gate handoff behavior. |

---

## Files Not in GitHub

These exist locally but are ignored by `.gitignore`:

| Path | Why |
|---|---|
| `.venv/` | Local Python environment — recreated by `scripts/setup.sh`. |
| `.env` | Local secrets — must stay private. |
| `__pycache__/` | Python cache — not useful in source control. |
| `docs/` | Internal brand and planning documents — local-only. |
| `personal-dumpground/` | Local-only personal notes, session logs, upgrade ideas, and scratch plans. |
| `PRE_LAUNCH_CHECKLIST.md` | Internal rollout checklist — local-only. |
| `VSCODE_CHANGES.md` | Scratch/update notes — local-only if recreated. |
| `*_SCRATCH.md` / `*_LOCAL.md` | Personal scratch files — local-only. |
| `/.codacy/` | CI config — removed from published repo. |
| `vault/intake/*` | May contain sensitive research notes. |
| `vault/briefs/*` | May contain unpublished content. |
| `vault/reports/*` | May contain internal competitor intel. |
| `vault/*.jsonl` | Local social signal intake records, potentially unpublished social notes. |
| `*.log` | May contain runtime details. |
