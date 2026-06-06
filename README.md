# Goblin Recon

*You trigger. It hunts.*

AI-powered content research agent for GenX Academy. Finds trending stories, locates source videos, and extracts 15-60 second clip moments — all in one pipeline.

---

## One-Line Setup

```bash
bash scripts/setup.sh                    # install dependencies
hermes profile create goblin-recon       # create Hermes profile
hermes -p goblin-recon                   # launch
```

Full setup guide → [`GETTING_STARTED.md`](GETTING_STARTED.md)

## Commands

| Say this | It does |
|---|---|
| `find trending AI stories` | Layer 1 — Trend Radar |
| `find sources for [topic]` | Layer 2 — Source Hunter |
| `find the moment in [URL]` | Layer 3 — Moment Finder |
| `run full scan` | All 3 layers |
| `run competitor scan` | Competitor Scout |
| `run brand check on [content]` | Brand gate validation |

## File Guide

Every file explained → [`FILE_DESCRIPTIONS.md`](FILE_DESCRIPTIONS.md)

---

**Goblin Bureau** — *"You trigger. It hunts."*
