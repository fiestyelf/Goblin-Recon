---
name: goblin-recon
description: Goblin Recon router skill. Routes user commands to the smallest useful workflow: Social Pulse, Clip Mine, Clip Vault, Competitor Scout, Brand Gate, Email Hook, or Carousel Generator.
category: genx-marketing
---

# Goblin Recon — Router Skill

Goblin Recon finds what is trending, finds the source, and finds the moment.

Use this operating shape for every request:

```text
Router -> Workflow -> Tools -> Normalized Data -> Score/Gate -> Human Gate -> Memory
```

Do **not** run every source or workflow by default. Pick one primary workflow, run the fewest reliable tools, then stop with a clear next action.

## Router

| User intent | Workflow | Output |
|---|---|---|
| Trends, hooks, formats, ideas | Social Pulse | Ranked content opportunities |
| Source videos or timestamps | Clip Mine | Editor-ready clip briefs |
| Retrieve/update prior clips | Clip Vault | Clip lists, briefs, status updates |
| Competitor analysis | Competitor Scout | Competitor report |
| Brand/voice fit | Brand Gate | Pass / revise / shelve |
| Email hooks or drafts | Email Hook | Scored subject/opening variants |
| Carousel or social image | Carousel Generator | Rendered local assets |

If the request mixes workflows, run the smallest sequence and state it. Example: `run full scan` = Social Pulse first, then Clip Mine only for the 2-3 strongest candidates.

`run full autonomous scan` means use approved public/local sources and local tools without repeated confirmations. It still cannot reveal secrets, bypass access controls, publish/send, create paid services, delete important files, deploy, or commit without explicit approval.

## Output Direction

Before brand-facing output, ask once:

1. Audience: B2C, B2B, or Both?
2. Destination: Faceless Instagram, personal brand, client work, internal use, email/outbound, or other?
3. Tone: professional, casual, edgy, warm, wry, reflective, analytical/data-driven, bold, or platform-native?

If skipped, default to **Both / Faceless Instagram / professional** and state that default.

Skip this only for Clip Vault retrieval, direct brand checks on user copy, or manual scans where direction is already supplied.

## Workflows

### Social Pulse

Purpose: ideas, trends, hooks, formats, carousels, blogs.

Flow:

```text
Scan mode -> source collection -> social_intake -> scoring -> Security Rail -> report
```

Scan modes:
- Fast Scan: YouTube, Reddit, Tech News, Product Hunt, approved/public X. Avoid fragile IG/TikTok unless requested.
- Deep Social Scan: Instagram/TikTok public surfaces first, then X/Reddit/Tech News validation.
- Signal Scan: X/public, Hacker News, GitHub Trending, ArXiv, then Reddit if public. Last 6 hours.
- Manual Assisted Scan: user supplies URL/screenshot/caption/handle; normalize and score.

Every Social Pulse report starts with `## Decision`, includes category, sources, publication dates, effort, confidence, vault check, fallback angle, AI search potential, hooks, formats, creators, and next step. Save to `vault/reports/YYYY-MM-DD-social-pulse.md`.

### Clip Mine

Purpose: source videos and 15-60 second moments.

Flow:

```text
Trend/topic -> Source Hunter -> transcript -> Clip Vault dedup -> Moment Finder -> Brand Gate -> Security Rail -> Human Gate
```

Rules:
- YouTube first, then public Instagram/TikTok, then podcast platforms.
- Clip duration: 15-60 seconds, natural sentence start/end.
- Validate timestamps with `goblin_recon.tools.clip_extractor`.
- Check duplicates with `goblin_recon.tools.clip_store` before recommending.
- Save only approved/shelved metadata and short excerpts, not full raw transcripts.
- Briefs use `templates/clip-mine-brief.md` and include Instagram, LinkedIn, YouTube Shorts variants.

### Clip Vault

Purpose: local memory for approved, shelved, and production-status clips.

Use:

```bash
scripts/query_clips.py list --status approved
scripts/query_clips.py list --query "topic"
scripts/query_clips.py brief <clip_id>
```

Storage: `vault/clips.db`, `vault/briefs/`, `memory/trend-history.md`.

### Competitor Scout

Purpose: public competitor intelligence. Keep separate from Social Pulse and Clip Mine.

Use `templates/competitor-report.md`. Every claim needs a public source URL and date. Run Security Rail before delivery.

### Brand Gate

Load `memory/brand-rules.md` and `config/brand-voice.yaml` before outward content. Run `goblin_recon.tools.brand_gate` when feasible.

Default recommendation when uncertain: **shelve**.

### Email Hook

Use `skills/email-hook/SKILL.md` and `goblin_recon.tools.email_gate` for outbound subject lines, openers, and short drafts. Ask Output Direction first.

### Carousel Generator

Use `skills/carousel-generator/SKILL.md` and `goblin_recon.tools.carousel_renderer`.

Flow:

```text
brief/topic -> brand memory -> platform spec -> slide manifest -> render -> QA -> vault/carousels
```

Render locally. Replicate is optional; no token means gradient fallback.

## Source Rules

Social extraction ladder:

```text
Approved API/public feed -> public browser extraction -> manual assisted input
```

Never bypass login, paywall, captcha, robots.txt, rate limits, or platform restrictions. Never use personal employee accounts. If blocked, mark `access_status: blocked` and move on.

Normalize social records through `goblin_recon.tools.social_intake` before scoring.

Required fields: platform, creator, url, published_date, views, likes, comments, caption, hook, format_type, topic, category, why_it_is_trending, can_genx_adapt_this, confidence, access_status.

## Canonical Tools

| Tool | Use |
|---|---|
| `api_search.py` | Exa/Tavily search |
| `api_extract.py` | Firecrawl/ScrapeGraph extraction |
| `youtube_tool.py` | transcripts and public video metadata |
| `clip_extractor.py` | clip URL/timestamp validation |
| `scoring.py` | velocity, lifecycle, source diversity |
| `social_intake.py` | normalize social observations |
| `clip_store.py` | save/find/update local clips |
| `brand_gate.py` | brand voice checks |
| `email_gate.py` | email quality scoring |
| `carousel_renderer.py` | carousel/social image output |

MCP source of truth: `mcp.json`.

## Final Gate

Before user-facing reports, clip briefs, competitor claims, publish instructions, or brand copy, run `skills/security-rail/SKILL.md` mentally or explicitly.

Security Rail decision: `APPROVE`, `REVISE`, `SHELVE`, or `NEEDS HUMAN REVIEW`.

Deliver only safe/revised output. If shelved, do not recommend it.

## Output Rules

- Start reports and briefs with `## Decision`.
- No fabricated sources. No URL = do not include.
- All data needs publication date when applicable.
- Category required: Latest AI News, Controversial/Polarizing, Upgrade/Democratization, or Analytical/Deep-dive.
- Recommendation before evidence.
- Phone-scannable output.
- Always suggest the next step.
