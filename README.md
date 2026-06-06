# Goblin Recon

*You trigger. It hunts.*

AI-powered content research agent for GenX Academy. Two pipelines: Social Pulse (ideas, blogs, carousels) and Clip Mine (podcast clips for faceless Instagram page).

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
| `run social pulse` | Pipeline A — ideas, blogs, carousels, content strategy |
| `run clip mine` | Pipeline B — podcast clips for faceless IG page |
| `blog ideas` | Social Pulse filtered for long-form content |
| `carousel ideas` | Social Pulse filtered for carousel topics |
| `content strategy this week` | Social Pulse + editorial suggestions |
| `find clips about [topic]` | Clip Mine for a specific topic |
| `find the moment in [URL]` | Extract best clip from a video |
| `run full scan` | Social Pulse + Clip Mine in sequence |
| `what clips are ready` | Approved clips awaiting editor handoff |
| `run competitor scan` | Competitor Scout |

## File Guide

Every file explained → [`FILE_DESCRIPTIONS.md`](FILE_DESCRIPTIONS.md)

---

**Goblin Bureau** — *"You trigger. It hunts."*
