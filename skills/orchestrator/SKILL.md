---
name: orchestrator
description: Route Goblin Recon requests to one primary workflow and run the smallest useful sequence.
category: genx-marketing
version: 1.1.0
---

# Orchestrator

Purpose: choose the workflow, set the stop condition, and avoid tool sprawl.

Core shape:

```text
Router -> Workflow -> Tools -> Normalized Data -> Score/Gate -> Human Gate -> Memory
```

## Triggers

- `run fast scan`
- `run deep social scan`
- `run signal scan`
- `manual scan this ...`
- `run social pulse`
- `run clip mine`
- `find clips about ...`
- `find the moment in ...`
- `what clips are ready`
- `run competitor scan`
- `write email hooks ...`
- `run carousel generator`
- `run full scan`
- `run full autonomous scan`

## Step 0 — Route

| Intent | Workflow | Stop when |
|---|---|---|
| Trends/hooks/formats/ideas | Social Pulse | ranked opportunities exist or sources fail |
| Source videos/timestamps | Clip Mine | 1-3 viable briefs or no safe source |
| Prior clips/status | Clip Vault | requested records shown/updated |
| Competitors | Competitor Scout | sourced report complete |
| Brand fit | Brand Gate | pass/revise/shelve returned |
| Email hooks/drafts | Email Hook | scored variants returned |
| Carousel/social image | Carousel Generator | local assets rendered |

If mixed, use the smallest chain. `run full scan` = Social Pulse, then Clip Mine for only the strongest 2-3 candidates.

`run full autonomous scan` = Social Pulse + limited Clip Mine + optional competitor/caption packaging from approved public/local sources. Still stop for secrets, paid setup, login/paywall/captcha bypass, publishing/sending, destructive deletes, deploys, or commits.

State selected workflow and scan mode before collecting data.

## Step 1 — Safety Preflight

- Public or explicitly approved sources only.
- No keys/tokens/cookies in chat.
- No personal social accounts.
- No bypassing login, paywall, captcha, robots.txt, rate limits, or platform restrictions.
- Human review required before publishing clips, claims, emails, or social posts.

## Step 2 — Direction

Before brand-facing output ask once:

```text
Audience? B2C / B2B / Both
Destination? Faceless Instagram / personal brand / client work / internal / email / other
Tone? professional / casual / edgy / warm / wry / reflective / analytical / bold / platform-native
```

If skipped: default to Both / Faceless Instagram / professional.

## Step 3 — Workflow Execution

### Social Pulse

```text
scan mode -> collect sources -> social_intake -> scoring -> Security Rail -> report
```

Use `skills/trend-radar/SKILL.md`. Save final report to `vault/reports/`.

### Clip Mine

```text
trend/topic -> source-hunter -> transcript -> clip_store dedup -> moment-finder -> brand_gate -> Security Rail -> Human Gate
```

Use:
- `skills/source-hunter/SKILL.md`
- `skills/moment-finder/SKILL.md`
- `goblin_recon.tools.youtube_tool`
- `goblin_recon.tools.clip_extractor`
- `goblin_recon.tools.clip_store`

Clip duration: 15-60 seconds. No full raw transcript storage.

### Clip Vault

Query `vault/clips.db` first. Do not run trend/source collection.

Useful commands:

```bash
scripts/query_clips.py list --status approved
scripts/query_clips.py list --query "topic"
scripts/query_clips.py brief <clip_id>
```

### Competitor Scout

Use `skills/competitor-scout/SKILL.md`. Every claim needs public URL + date. Run Security Rail.

### Email Hook

Use `skills/email-hook/SKILL.md` and `goblin_recon.tools.email_gate`. Run Security Rail before delivery.

### Carousel Generator

Use `skills/carousel-generator/SKILL.md` and `goblin_recon.tools.carousel_renderer`. Render locally; Replicate is optional fallback enhancement, not required.

## Step 4 — Final Gate

Before user delivery, run `skills/security-rail/SKILL.md` on reports, briefs, claims, copy, and recommendations.

Decision handling:

```text
APPROVE -> deliver
REVISE -> deliver revised safe version
SHELVE -> do not recommend
NEEDS HUMAN REVIEW -> label clearly
```

## Output Contract

Every report/brief starts with `## Decision` and includes:

- recommendation
- category when content-related
- source URLs and dates
- effort
- confidence
- vault check
- fallback angle
- AI search potential when relevant
- next step

No fabricated sources. When uncertain, shelve.
