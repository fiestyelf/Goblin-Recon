# Launch Preparation — Competitor Intelligence Pipeline

Goblin Recon's competitive intelligence system for launch positioning. Run it manually before major positioning decisions, and optionally schedule it after credentials and delivery rules are approved.

---

## What it does

Competitor Scout monitors public competitor pages, detects strategic changes, and turns the result into decision-ready GenX actions:

- pricing and offer changes
- positioning and homepage changes
- blog, docs, changelog, jobs, events, and press signals
- semantic diffing against previous snapshots
- source-quality review through Security Rail
- cell-ready moves for content, sales, and product/offer follow-up

---

## One-time setup

```bash
# 1. Install local tooling and skills
bash scripts/setup.sh

# 2. Review source-typed competitors
$EDITOR config/competitors.yaml

# 3. Add optional extraction keys only after approval
cp .env.example .env
```

Real keys stay in `.env` or an approved secret manager. Do not paste keys into Markdown, YAML, prompts, Slack, or screenshots.

---

## Competitor config

Competitors use source-typed pages so the scout knows what each URL means and how important it is:

```yaml
competitors:
  - name: "Example"
    domain: "example.com"
    website: "https://www.example.com"
    pricing_page: "https://www.example.com/pricing"
    category: "agent-platform"
    sources:
      - url: "https://www.example.com"
        kind: homepage
        label: "Main landing page"
      - url: "https://www.example.com/pricing"
        kind: pricing
        label: "Pricing page"
      - url: "https://www.example.com/blog"
        kind: blog
        label: "Company blog"
    rss_feed: ""
```

Supported kinds: `homepage`, `pricing`, `blog`, `changelog`, `jobs`, `docs`, `about`, `events`, `press`, `podcast`, `other`.

---

## Manual scan workflow

In Hermes, use one of these commands:

| Command | Use |
|---|---|
| `check competitors` | Quick pulse: homepage/key-signal check only. |
| `run competitor scan` | Standard weekly-style scan. |
| `competitor deep scan` | Full source-typed crawl and semantic diff. |
| `competitor gap analysis` | Compare competitor positioning against GenX. |
| `discover competitors` | Monthly candidate discovery; requires approved search provider. |

Expected flow:

```text
Load config/competitors.yaml
→ scrape approved public sources
→ hash and compare with memory/competitor-snapshots.md
→ semantic diff strategic changes only
→ produce competitor report from templates/competitor-report.md
→ run skills/security-rail/SKILL.md
→ output report + Cell-Ready Moves
→ save report to vault/reports/
```

---

## Storage structure

```text
vault/
├── competitor-data/                 ← local-only scraped JSON or markdown snapshots
└── reports/
    └── YYYY-MM-DD-competitor-scan.md

memory/
└── competitor-snapshots.md           ← cumulative hashes and strategic-change notes
```

`vault/competitor-data/*` and generated reports are ignored by Git because they may contain unpublished competitor analysis.

---

## What to track for launch

| Signal | Why it matters |
|---|---|
| New feature added | Competitor reacting to a gap; possible content or offer angle. |
| Feature removed | They may be retreating from a promise; possible positioning opening. |
| Pricing change | Possible target-market or packaging shift. |
| New competitor appears | Add to config quickly; do not get blindsided. |
| Messaging shift | They changed what they want to be known for. |
| Hiring page changes | Hiring patterns can reveal growth direction. |
| Docs/changelog changes | Product capability shifts often appear here before marketing pages. |

---

## Deployment and automation notes

There is no safe default cron until credentials, budget, and delivery channel are approved.

Before deploying or scheduling:

1. Confirm approved extraction providers and rate limits.
2. Store keys in the deployment secret manager, not files.
3. Run `bash scripts/dev_check.sh` locally.
4. Run `scripts/check_secrets.py --include-local-env` only on the machine that owns the local `.env`.
5. Confirm generated reports go to a private `vault/` or approved destination.
6. Keep `[SILENT]` behavior for zero-change scheduled scans.
7. Require Security Rail and human review for competitor claims, pricing claims, or publish-ready cells.

---

## Anti-bot and access fallback

Use only public or approved sources.

1. Prefer approved public extraction/API providers.
2. If a public page blocks access, retry once with an approved fallback.
3. If still blocked, mark `access_status: blocked` and move on.
4. Do not bypass login walls, paywalls, captchas, robots.txt, rate limits, or platform restrictions.
5. Do not use personal accounts for automation.

---

*Part of Goblin Recon launch preparation. Update this doc as new competitors, sources, or deployment rules are approved.*
