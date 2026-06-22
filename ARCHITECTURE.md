# Goblin Recon Architecture

Goblin Recon is a narrow content-intelligence agent. It routes one request to one useful workflow, uses public/approved sources only, scores the result, gates it, then stores only useful memory.

```text
User Command
  -> Intent Router
  -> Primary Workflow
  -> Canonical Tools
  -> Normalized Record
  -> Score / Gate
  -> Human Decision
  -> Vault / Memory / Report
```

## Router

| Intent | Workflow | Output |
|---|---|---|
| Trends, hooks, formats, ideas | Social Pulse | Ranked content opportunities |
| Source videos, timestamps | Clip Mine | Editor-ready clip briefs |
| Prior clips/status | Clip Vault | Saved clips, briefs, status |
| Competitor analysis | Competitor Scout | Competitor report |
| Brand/voice fit | Brand Gate | Pass / revise / shelve |
| Email hooks/drafts | Email Hook | Scored subject/opening variants |
| Carousel/social image | Carousel Generator | Local rendered assets |

Rule: pick one primary workflow. If mixed, run the smallest sequence and state it.

## Workflows

### Social Pulse

```text
Scan mode -> collect public signals -> social_intake -> scoring -> Security Rail -> report
```

Use for ideas, blogs, carousels, hooks, formats, and weekly strategy. Not for final clip production.

### Clip Mine

```text
Trend/topic -> source search -> transcript -> vault dedup -> moment selection -> Brand Gate -> Security Rail -> Human Gate
```

Use for 15-60 second clip briefs. Store metadata and short excerpts only, not full raw transcripts.

### Clip Vault

```text
clips.db -> search/get/update -> regenerate brief -> production status
```

Use before new clip work to avoid duplicates.

### Competitor Scout

```text
public sources -> normalized claims -> Security Rail -> report
```

Every claim needs source URL and date.

### Email Hook

```text
output direction -> campaign fit -> email_gate -> Security Rail -> ranked variants
```

Use for subject lines, openers, and short outbound drafts.

### Carousel Generator

```text
reference/template -> memory -> slide plan -> human approval -> Replicate visual layers -> Pillow renderer -> QA -> vault/carousels
```

Render final text locally with Pillow. Replicate is for visual/background layers only; gradient fallback is valid when the token is missing or generation fails. The Replicate MCP is for agent/tool calls; `carousel_renderer.py` uses `REPLICATE_API_TOKEN` directly for local render jobs. QA checks readability, platform dimensions, page/account fit, claim safety, visual consistency, exports, and human approval.

## Canonical Tools

| Tool | Job |
|---|---|
| `api_search.py` | Exa/Tavily search |
| `api_extract.py` | Firecrawl/ScrapeGraph extraction |
| `env.py` | local/profile env lookup |
| `youtube_tool.py` | transcripts and public metadata |
| `clip_extractor.py` | timestamp/URL validation |
| `scoring.py` | velocity, lifecycle, source diversity |
| `social_intake.py` | normalize social observations |
| `clip_store.py` | clip memory and brief rendering |
| `brand_gate.py` | brand voice checks |
| `email_gate.py` | email quality scoring |
| `carousel_renderer.py` | carousel/social image output |

MCP source of truth: `mcp.json`.

## Data Contracts

### Social Signal

```text
platform, creator, url, published_date, views, likes, comments,
caption, hook, format_type, topic, category,
why_it_is_trending, can_genx_adapt_this, confidence, access_status
```

### Clip

```text
source_url, source_title, source_channel_or_account,
start_sec, end_sec, duration_seconds,
moment_summary, why_post, suggested_caption,
brand_angle, brand_alignment_score, status
```

### Carousel

```text
job, reference, memory_applied, layout, approvals, slides, paths, qa, revision_history
```

Each slide stores role, kicker, headline, body, CTA, image_prompt, background asset path, export path, and revision notes.

## Gates

```text
Trend score -> Source score -> Moment score -> Brand Gate -> Security Rail -> Human Gate
```

Security Rail decisions:

```text
APPROVE -> deliver
REVISE -> fix then deliver
SHELVE -> do not recommend
NEEDS HUMAN REVIEW -> label clearly
```

Default when uncertain: **shelve**.

## Source Policy

```text
Approved API/public feed -> public browser extraction -> manual assisted input
```

Never bypass login, paywall, captcha, robots.txt, rate limits, or platform restrictions. Never use personal employee accounts. If blocked, mark `access_status: blocked` and move on.

## Memory

| Path | Use |
|---|---|
| `vault/clips.db` | clip records and dedup |
| `vault/briefs/` | generated clip briefs |
| `vault/reports/` | scan/report outputs |
| `vault/carousels/` | rendered carousel assets |
| `memory/trend-history.md` | trend memory |
| `memory/carousel/` | brand/platform carousel memory |

## Final Rule

The agent gathers, structures, scores, and recommends. Humans approve publishing, sensitive claims, external actions, and editor production.
