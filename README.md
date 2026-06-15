# Goblin Recon

*You trigger. It hunts.*

AI-powered content research agent for GenX Academy. Three core workflows: Social Pulse (ideas, blogs, carousels), Clip Mine (podcast clips for faceless Instagram page), and Clip Vault (persistent approved/shelved clip memory).

---

## One-Command Setup

```bash
cd goblin-recon
bash scripts/setup.sh
hermes -p goblin-recon
```

The setup script installs the Goblin Recon Hermes profile, SOUL.md, bundled skills, profile defaults, Python virtual environment, and dependencies. If no model provider is configured yet, setup will warn and continue so you can configure one later.

Before sharing, deploying, or scheduling automation, run:

```bash
bash scripts/dev_check.sh
```

This runs tests, the secret scanner, and structure checks.

Full setup guide → [`GETTING_STARTED.md`](GETTING_STARTED.md)

## Commands

Full command guide with plain-language descriptions → [`COMMANDS.md`](COMMANDS.md)

| Say this | It does |
|---|---|
| `run fast scan` | Low-stress daily scan using reliable sources first |
| `run deep social scan` | Deeper Instagram/TikTok-first social trend scan |
| `manual scan this [URL/screenshot/caption]` | Normalize and score human-provided social material |
| `run social pulse` | Workflow — ideas, blogs, carousels, content strategy |
| `run clip mine` | Workflow — podcast clips for faceless IG page |
| `blog ideas` | Social Pulse filtered for long-form content |
| `carousel ideas` | Social Pulse filtered for carousel topics |
| `content strategy this week` | Social Pulse + editorial suggestions |
| `find clips about [topic]` | Clip Mine for a specific topic |
| `find the moment in [URL]` | Extract best clip from a video |
| `run full scan` | Social Pulse + Clip Mine in sequence |
| `what clips are ready` | Approved clips awaiting editor handoff |
| `run competitor scan` | Competitor Scout with Security Rail and cell-ready moves |
| `write email hooks for [offer/audience]` | Email Hook variants with quality-gate scores |

## Architecture

Goblin Recon uses a professional semi-autonomous agent structure:

```text
Router -> Workflow -> Tools -> Normalized Data -> Score -> Human Gate -> Memory
```

Full architecture guide → [`ARCHITECTURE.md`](ARCHITECTURE.md)

## Social Intake

All social observations should be normalized before scoring:

```bash
.venv/bin/python -m goblin_recon.tools.social_intake --url "https://www.instagram.com/reel/..." --topic "AI agents" --caption "..."
```

Store local social signals when useful:

```bash
.venv/bin/python -m goblin_recon.tools.social_intake --input vault/intake/social-signal.json --store
```

## File Guide

Every file explained → [`FILE_DESCRIPTIONS.md`](FILE_DESCRIPTIONS.md)

---

**Goblin Bureau** — *"You trigger. It hunts."*
