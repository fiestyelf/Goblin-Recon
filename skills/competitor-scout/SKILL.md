---
name: competitor-scout
description: Public competitor scan that turns sourced observations into cell-ready moves. Triggers on "run competitor scan", "check competitors", "competitor deep scan".
category: genx-marketing
version: 2.1.0
---

# Competitor Scout

Goal: find what competitors are visibly doing, what changed, and what GenX should do next. Use public/approved sources only.

## Inputs

Ask only if missing:
- competitors or category
- audience: B2B, B2C, or Both
- destination: content, sales, product/offer, internal
- scan depth: fast or deep

Default: configured competitors in `config/competitors.yaml`, Both, internal, fast.

## Source Rules

- Public source URL + publication/access date required for every claim.
- No login/paywall/captcha/rate-limit bypass.
- If blocked, mark `access_status: blocked` and move on.
- Prefer home/pricing/changelog/blog/docs/events/jobs/press pages from `config/competitors.yaml`.

## Flow

```text
competitor list -> public pages -> observations -> claims -> score -> Cell-Ready Moves -> Step 6.5 — Security Rail -> report
```

## Scoring

Use 1-5 for each:
- relevance to GenX audience
- recency
- proof quality
- differentiation opportunity
- effort to respond

Advance only if proof quality is at least 3. When unsure, shelve.

## Output

Use `templates/competitor-report.md`.

Required sections:
- `## Decision`
- `## Key Changes`
- `## Evidence Ledger`
- `## Cell-Ready Moves`
- `## Security Rail Result`

Cell-Ready Moves must include:
- Content Cell
- Sales Cell
- Product/Offer Cell

Each move needs: action, why now, source, effort, confidence, risk, next owner.

## Step 6.5 — Security Rail

Security Rail is mandatory before delivery. Run `skills/security-rail/SKILL.md` on the final report.

Decision handling:
- `APPROVE` -> deliver
- `REVISE` -> fix and deliver revised version
- `SHELVE` -> do not recommend the move
- `NEEDS HUMAN REVIEW` -> label clearly

## Memory

Save useful approved reports to `vault/reports/YYYY-MM-DD-competitor-scan.md`. Do not store private data, secrets, or raw scraped dumps.
