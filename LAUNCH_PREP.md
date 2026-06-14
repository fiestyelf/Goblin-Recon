# Launch Preparation — Data Extraction Pipeline

Goblin Recon's competitive intelligence system for launch positioning. Run this weekly leading up to launch, then ongoing afterward.

---

## What it does

Extracts structured data from competitor websites using ScrapeGraph v2, stores JSON snapshots, diffs week-over-week, and finds positioning gaps GenX can own.

---

## One-time setup

```bash
# 1. Add competitors to config/competitors.yaml
# 2. Run setup (ensures .env has SCRAPEGRAPH_API_KEY)
bash scripts/setup.sh
```

---

## Manual extraction (any time)

```bash
# Extract features from a competitor homepage
.venv/bin/python -m goblin_recon.tools.api_extract \
  --scrapegraph "https://competitor.com" \
  --schema features --json > vault/competitor-data/competitor-2026-06-13.json

# Extract pricing from their pricing page
.venv/bin/python -m goblin_recon.tools.api_extract \
  --scrapegraph "https://competitor.com/pricing" \
  --schema pricing --json > vault/competitor-data/competitor-pricing-2026-06-13.json

# Extract positioning from their homepage
.venv/bin/python -m goblin_recon.tools.api_extract \
  --scrapegraph "https://competitor.com" \
  --schema article --json > vault/competitor-data/competitor-positioning-2026-06-13.json
```

## Available schemas

| Schema | Use for | Extracts |
|---|---|---|
| `features` | Product pages, homepages | Feature name + description list |
| `pricing` | Pricing pages | Plans with name, price, features |
| `competitor` | Any company page | Company name, products, pricing, key features |
| `article` | Homepages, about pages | Title, main content, author, date |

---

## Then feed to Goblin Recon

After extracting, say:
> "Here's competitor data for CrewAI and LangChain. Find the positioning gap for GenX Academy."

Goblin Recon produces:
- Feature matrix (what they have vs what we have)
- Positioning gap (what they say vs what we can own)
- Voice differentiation (where their tone overlaps and where we're unique)
- Content angles (stories GenX can tell that they structurally cannot)

---

## Weekly automated scan

Cron job runs every Monday 9am. Reads `config/competitors.yaml`. Extracts every competitor. Diffs against last week. Reports changes.

**To add a competitor:** Edit `config/competitors.yaml` — that's it.

---

## Storage structure

```
vault/
├── competitor-data/
│   ├── crewai-2026-06-13.json
│   ├── crewai-2026-06-20.json          ← next week's diff
│   ├── langchain-2026-06-13.json
│   └── langchain-2026-06-20.json
└── reports/
    └── 2026-06-13-competitor-scan.md   ← gap analysis

memory/
└── competitor-snapshots.md              ← cumulative record
```

---

## What to track for launch

| Signal | Why it matters |
|---|---|
| New feature added | Competitor reacting to a gap — content angle |
| Feature removed | They're retreating from something — opportunity |
| Pricing change | Positioning shift — adjust GenX pricing messaging |
| New competitor appears | Add to list immediately — don't get blindsided |
| Messaging shift | They changed how they describe themselves — reposition |
| Hiring page changes | They're scaling a specific area — future feature signal |

---

## Anti-bot fallback

If ScrapeGraph returns 403 (blocked):
1. Retry with Firecrawl: `--firecrawl "URL" --json`
2. Retry with Hermes browser: `browser_navigate` in-chat
3. Fallback: ghost-browser MCP (real Chrome fingerprint)

---

*Part of Goblin Recon launch preparation. Update this doc as new competitors enter the space.*
