---
name: trend-radar
description: Find and score current AI/social content signals for Social Pulse and Clip Mine.
category: genx-marketing
version: 1.1.0
---

# Trend Radar

Goal: identify current, source-backed content opportunities. No fabricated sources.

## Inputs

- topic or scan mode
- audience: B2C, B2B, Both
- destination: social, blog, carousel, clip mining
- time window: default last 24-72h; Signal Scan last 6h

## Source Order

Fast Scan: YouTube, Reddit, Tech News, Product Hunt, approved/public X.
Deep Social Scan: Instagram/TikTok public surfaces, then X/Reddit/Tech News.
Signal Scan: X/public, Hacker News, GitHub Trending, ArXiv, Reddit if public.
Manual Assisted Scan: user-provided URL/screenshot/caption/handle.

Respect access limits. If blocked, mark `access_status: blocked` and move on.

## Normalize

Every signal must map to:

```text
platform, creator, url, published_date, views, likes, comments,
caption, hook, format_type, topic, category,
why_it_is_trending, can_genx_adapt_this, confidence, access_status
```

Use `goblin_recon.tools.social_intake` before scoring when feasible.

## Score

Score 0-100:
- velocity/recency: 30
- source proof: 20
- audience fit: 20
- format usefulness: 15
- differentiation: 15

Advance threshold: 60. If below, shelve.

Categories:
- Latest AI News
- Controversial/Polarizing
- Upgrade/Democratization
- Analytical/Deep-dive

## Output

Start with `## Decision`.

For each opportunity include:
- recommendation: approve / monitor / shelve
- category
- source URLs and publication dates
- hook and format
- creator/source driving it
- effort
- confidence
- vault check
- fallback angle
- AI search potential
- next step

Save Social Pulse reports to `vault/reports/YYYY-MM-DD-social-pulse.md`.
