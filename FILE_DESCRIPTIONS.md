# Goblin Recon File Descriptions

This document explains what each file and folder in Goblin Recon does. Use it when onboarding team members or reviewing the repository in GitHub.

Important GitHub note: the text shown beside files in the GitHub file browser is usually the **latest commit message**, not a custom file description. This file is the actual clean reference for what each file does.

---

## Start Here

| File | Job |
|---|---|
| `README.md` | Main project overview. Explains what Goblin Recon is, how the pipeline works, setup basics, commands, security references, troubleshooting, and repository map. |
| `INSTRUCTIONS.md` | Simple step-by-step guide for marketing team members. Explains setup, commands, what to trigger when, business security rules, weekly workflow, FAQ, and safe usage. |
| `AGENTS.md` | Main Hermes agent rulebook. Defines Goblin Recon identity, behavior, source verification rules, clip rules, security guardrails, and supported commands. |
| `HERMES_APPROVALS.md` | Teaches users what Hermes tool permissions to approve or deny when starting and running Goblin Recon. |

---

## Distribution and Rollout Docs

| File | Job |
|---|---|
| `GITHUB_DISTRIBUTION.md` | Explains how to distribute Goblin Recon through GitHub, what should be committed, what must never be committed, and how team members clone/update the repo. |
| `PRE_LAUNCH_CHECKLIST.md` | Final business rollout checklist covering repository safety, API approval, source approval, legal review, data retention, and team training. |

---

## Security, Legal, and API Docs

| File | Job |
|---|---|
| `SECURITY.md` | Security policy for internal company use. Covers secret handling, public-source rules, account safety, retention, and incident response. |
| `API_KEYS.md` | Explains safe API key storage, key scopes, rotation, leak response, and approved methods such as `.env`, Hermes secrets, and company secret managers. |
| `SOCIAL_API_SETUP.md` | Detailed guide for adding approved social media API keys and enabling YouTube, Reddit, X/Twitter, Instagram/Meta, LinkedIn, or Discord integrations safely. |
| `LEGAL_GUARDRAILS.md` | Platform and publishing rules. Covers copyright, competitor research, source attribution, private sources, paywalls, and when to shelve. |

---

## Repository Safety Files

| File | Job |
|---|---|
| `.gitignore` | Blocks local secrets, virtual environments, cache files, logs, and vault outputs from being committed. |
| `.env.example` | Safe template showing environment variable names for future approved API keys. Users copy this to `.env` locally. Actual `.env` files must never be committed. |

---

## Python Project and Setup Files

| File | Job |
|---|---|
| `requirements.txt` | Pinned Python dependency list for simple setup. Currently includes `youtube-transcript-api==1.2.4`. |
| `pyproject.toml` | Python project metadata and dependency declaration for `uv`. Keeps setup modern and repeatable. |

---

## Config Files

| File | Job |
|---|---|
| `config/sources.yaml` | Defines trend sources: X/Twitter queries, monitored accounts, Reddit subreddits, tech news sites, and Product Hunt topics. Used by Trend Radar. |
| `config/scoring.yaml` | Defines all scoring weights and thresholds for Trend Radar, Source Hunter, Moment Finder, and clip length rules. |
| `config/content-sources.yaml` | Defines YouTube channels, Instagram accounts, hashtags, and topic query patterns used by Source Hunter. |
| `config/competitors.yaml` | Empty competitor template. Later, approved competitors can be added here for Competitor Scout. |
| `config/security.yaml` | Machine-readable security policy: public-only sources, API key rules, rate limits, human review requirements, and retention defaults. |
| `config/integrations.yaml` | Optional integration registry. Lists required environment variables and keeps all social/API integrations disabled until approved. |

---

## Skill Files

| File | Job |
|---|---|
| `skills/orchestrator/SKILL.md` | Main pipeline driver. Runs Trend Radar, Source Hunter, Moment Finder, and the human approval gate when the user says `run full scan`. |
| `skills/trend-radar/SKILL.md` | Layer 1 research skill. Finds and scores trending AI stories from public sources. |
| `skills/source-hunter/SKILL.md` | Layer 2 research skill. Finds YouTube and Instagram source material for a trend or known topic. |
| `skills/moment-finder/SKILL.md` | Layer 3 extraction skill. Finds quotable 15-60 second clip moments from transcripts and creates clip briefs. |
| `skills/competitor-scout/SKILL.md` | Standalone competitor/campaign research skill. Tracks public pricing, features, messaging, and market activity. |

---

## Script Files

| File | Job |
|---|---|
| `scripts/setup.sh` | One-command local setup script. Creates `.venv` and installs approved Python dependencies. |
| `scripts/check_secrets.py` | Local secret scanner. Checks for accidental API keys, tokens, webhooks, or credentials before sharing or pushing. |
| `scripts/get_youtube_transcript.py` | Pulls public YouTube captions/transcripts with timestamps. Used by Moment Finder for clip research. |
| `scripts/extract_clip.py` | Validates video URLs and clip boundaries, then returns clean timestamped clip metadata. |
| `scripts/score_engagement.py` | Calculates engagement velocity and returns a normalized score for trend/source scoring. |

---

## Template Files

| File | Job |
|---|---|
| `templates/trend-report.md` | Standard output format for daily AI trend reports. |
| `templates/clip-brief.md` | Standard output format for clip briefs with timestamps, transcript excerpt, hook, caption, format, hashtags, and approval status. |
| `templates/content-brief.md` | Standard output format for broader content planning based on a trend, source material, angle, hook, platform, and next steps. |
| `templates/competitor-report.md` | Standard output format for competitor intelligence reports covering pricing, features, marketing, social activity, and recommended response. |

---

## Memory Files

| File | Job |
|---|---|
| `memory/trend-history.md` | Stores previous trend scan results for deduplication and future review. Starts empty with an example format. |
| `memory/competitor-snapshots.md` | Stores competitor snapshots over time so future scans can detect changes. Starts empty with an example format. |
| `memory/content-performance.md` | Stores notes on how approved content performed after posting. Used later to improve scoring decisions. |

---

## Vault Folders

| Path | Job |
|---|---|
| `vault/intake/.gitkeep` | Keeps the raw intake folder in Git. Actual raw intake files are local outputs and are ignored. |
| `vault/briefs/.gitkeep` | Keeps the approved briefs folder in Git. Actual approved briefs are local outputs and are ignored unless intentionally approved. |
| `vault/reports/.gitkeep` | Keeps the approved reports folder in Git. Actual competitor reports are local outputs and are ignored unless intentionally approved. |

---

## Test Files

| File | Job |
|---|---|
| `tests/test_scripts.py` | Offline unit tests for clip extraction, transcript input validation, and engagement scoring safety behavior. |

---

## What Should Not Appear in GitHub

These may exist locally, but they should not be committed:

| Local Path | Why Not Committed |
|---|---|
| `.venv/` | Local Python environment. Recreated by `scripts/setup.sh`. |
| `.env` | Local secrets file. Must stay private. |
| `__pycache__/` | Python cache output. Not useful for source control. |
| `vault/intake/*` | May contain raw research output or sensitive notes. |
| `vault/briefs/*` | May contain unpublished content briefs. |
| `vault/reports/*` | May contain internal competitor intelligence. |
| `*.log` | May contain local runtime details or sensitive data. |
