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

Full setup guide → [`docs/ops/getting-started.md`](docs/ops/getting-started.md)

## Commands

Full command guide with plain-language descriptions → [`COMMANDS.md`](COMMANDS.md)

| Say this | It does |
|---|---|
| `run fast scan` | Quick daily trend check. |
| `run deep social scan` | Deeper Instagram and TikTok trend check. |
| `run signal scan` | Find early AI signals before they are mainstream. |
| `manual scan this [URL/screenshot/caption]` | Score something you paste in. |
| `run social pulse` | Find content ideas, blog angles, and hooks. |
| `run clip mine` | Find short video clip ideas. |
| `blog ideas` | Get article ideas from current trends. |
| `carousel ideas` | Get swipe-post ideas from current trends. |
| `content strategy this week` | Get a simple weekly posting plan. |
| `find clips about [topic]` | Find clips about one topic. |
| `find the moment in [URL]` | Pick the best short clip from one video. |
| `run full scan` | Find trends, then find clips for the best ones. |
| `run full autonomous scan` | Run the whole approved workflow without asking at each step. |
| `what clips are ready` | Show approved clips ready for editors. |
| `run competitor scan` | Check competitors and suggest next moves. |
| `run brand check on [content]` | Check copy against brand rules before posting. |
| `write email hooks for [offer/audience]` | Write and score email subject lines and openers. |

## Architecture

Goblin Recon uses a professional semi-autonomous agent structure:

```text
Router -> Workflow -> Tools -> Normalized Data -> Score/Gate -> Human Gate -> Memory
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

Every file explained → [`docs/ops/file-descriptions.md`](docs/ops/file-descriptions.md)

---

**Goblin Bureau** — *"You trigger. It hunts."*
