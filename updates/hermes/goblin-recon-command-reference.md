# Goblin Recon — Command Reference

> v1.0 — June 15, 2026
> 33 commands across 6 workflows

---

## Overview

Goblin Recon exposes 33 commands organized into 6 workflows. Every command routes through the orchestrator, which selects the appropriate skill chain, scan mode, and stop condition.

Commands are case-insensitive. Parameters in `[brackets]` are required. Parameters in `(parentheses)` are optional.

---

## 1. Social Pulse — Trend Discovery

Social Pulse finds trending AI stories, hooks, formats, and content angles. It is intelligence, not production — it does not produce editor-ready clips.

### Scan Commands

| Command | Description | Scan Mode | Sources |
|---------|------------|-----------|---------|
| `run social pulse` | Full trend scan across all platforms | Deep Social | IG → TikTok → X → Reddit → Tech News |
| `run fast scan` | Daily low-stress discovery | Fast | YouTube, Reddit, Tech News, Product Hunt |
| `run deep social scan` | Weekly social-native deep dive | Deep Social | IG/TikTok first, then X/Reddit/News |
| `run signal scan` | First-mover early-signal scan | Signal | X, Hacker News, GitHub, ArXiv (6h window) |
| `manual scan [URL]` | Normalize human-provided material | Manual Assisted | User-supplied URLs, screenshots, or captions |

### Platform-Specific Scans

| Command | Description |
|---------|------------|
| `trending on Instagram` | Scan IG creator accounts (@therundownai, @rowancheung, @inflecta.ai, @ankitgupta.ai) |
| `trending on TikTok` | Scan TikTok hashtags (#ainews, #artificialintelligence, #aiexplained) |

### Content Strategy

| Command | Description |
|---------|------------|
| `blog ideas` | Trending stories filtered for long-form content angles |
| `carousel ideas` | Trending stories filtered for carousel-worthy topics |
| `content strategy` | Social Pulse results with editorial calendar recommendations |
| `trending formats` | Current winning reel formats and hook styles |

---

## 2. Clip Mine — Video Clip Production

Clip Mine finds source videos and extracts 15–60 second editor-ready moments. Output goes directly to editors for reel production.

### Core Commands

| Command | Description | Layers Run |
|---------|------------|------------|
| `run clip mine` | Full pipeline from trending stories | Trend Radar → Source Hunter → Moment Finder |
| `find clips about [topic]` | Source hunt + moment extraction for a specific topic | Source Hunter → Moment Finder |
| `find the moment in [URL]` | Extract the best clip from a specific video | Moment Finder only |

### Combined Scan

| Command | Description |
|---------|------------|
| `run full scan` | Social Pulse first, then Clip Mine for the top 2–3 candidates |

---

## 3. Clip Vault — Persistent Storage

Clip Vault retrieves and manages stored clips across sessions. Storage backend: `vault/clips.db` + `vault/briefs/`.

| Command | Description |
|---------|------------|
| `clips ready` | List all approved clips awaiting editor handoff |
| `search clips [query]` | Full-text search by topic, source, summary, or caption |
| `show clip [id]` | Display a single clip record with full metadata |
| `update clip [id] status [status]` | Move a clip through: `approved` → `in_production` → `scheduled` → `posted` → `shelved` |

---

## 4. Competitor Scout — Market Intelligence

Competitor Scout monitors competitor pricing, features, positioning, and marketing activity. It runs standalone — not chained into Social Pulse or Clip Mine.

| Command | Description | Depth |
|---------|------------|-------|
| `run competitor scan` | Standard change detection against last saved snapshot | Homepage + key pages |
| `check competitors` | Quick pulse — surface-level changes only | Homepage only |
| `competitor deep scan` | Full-site scrape of all sub-pages | All pages (events, blog, press, podcast, pricing, about) |
| `competitor gap analysis` | Side-by-side comparison of competitor vs GenX Academy | Both sites, all dimensions |
| `competitor gap reverse [name]` | What GenX is missing compared to a specific competitor | GenX site audit |
| `compare SEO` | Indexable page count, backlinks, blog volume, meta tags | Both sites |

---

## 5. Email Hook — Outbound Email Generation

Email Hook generates and validates subject lines, openers, and short email drafts. All output passes through `email_gate` before delivery.

| Command | Description |
|---------|------------|
| `write email hooks for [offer]` | Generate 5 subject + opener variants for an outbound campaign |
| `write subject lines for [campaign]` | Subject-only variant generation |
| `validate this email` | Run the email quality gate on existing copy |

---

## 6. System Commands

| Command | Description |
|---------|------------|
| `register all skills` | Re-register every skill with the Hermes skill registry |
| `sync from github` | Pull latest repository changes and copy all files to the profile |

---

## Intent Routing Map

The orchestrator classifies every command into one primary workflow before tool invocation begins.

| User Says | Routes To | Chains |
|-----------|-----------|--------|
| `run social pulse`, `run fast scan`, `run deep social scan`, `run signal scan`, `manual scan [URL]`, `trending on Instagram`, `trending on TikTok` | Social Pulse | trend-radar → report → auto-save |
| `blog ideas`, `carousel ideas`, `content strategy`, `trending formats` | Social Pulse (filtered) | trend-radar → filter → report |
| `run clip mine`, `run full scan` | Clip Mine | trend-radar → source-hunter → moment-finder → brand-gate → human-gate |
| `find clips about [topic]` | Clip Mine | source-hunter → moment-finder → brand-gate → human-gate |
| `find the moment in [URL]` | Clip Mine | moment-finder → brand-gate → human-gate |
| `clips ready`, `search clips [query]`, `show clip [id]`, `update clip [id] status [status]` | Clip Vault | query vault → present |
| `run competitor scan`, `check competitors`, `competitor deep scan`, `competitor gap analysis`, `competitor gap reverse`, `compare SEO` | Competitor Scout | scrape → diff → report → auto-save |
| `write email hooks for [offer]`, `write subject lines for [campaign]`, `validate this email` | Email Hook | campaign select → generate → email-gate → present |
| `register all skills`, `sync from github` | System | execute → confirm |

---

## Output Auto-Save Policy

Every report is automatically saved after generation. The user does not need to request a save.

| Workflow | Save Path |
|----------|----------|
| Social Pulse | `vault/reports/YYYY-MM-DD-social-pulse.md` |
| Clip Mine (approved clips) | `vault/briefs/[date]-[headline].md` |
| Competitor Scout | `vault/reports/YYYY-MM-DD-competitor-scan.md` |
| Email Hook | Not auto-saved (tactical output, not a report) |
| Clip Vault | Not auto-saved (retrieval, not new content) |

---

## Scan Mode Reference

| Mode | Use Case | Primary Sources | Skip |
|------|----------|----------------|------|
| **Fast Scan** | Daily low-stress | YouTube, Reddit, Tech News, Product Hunt | IG/TikTok (fragile) |
| **Deep Social Scan** | Weekly or launch days | IG/TikTok first, then X, Reddit, News | None — but downgrade blocked sources |
| **Signal Scan** | First-mover discovery | X, Hacker News, GitHub, ArXiv | Anything older than 6 hours |
| **Manual Assisted** | Human provides material | User-supplied URLs, screenshots, captions | All automated sources |

---

## Category Tags

Every Social Pulse item and Clip Mine clip is tagged with one of four categories:

| Tag | Meaning |
|-----|---------|
| `Latest AI News` | Breaking developments, product launches, policy changes |
| `Controversial` | Debates, backlash, hot takes |
| `Upgrade` | Tool tutorials, barrier collapsing, democratization |
| `Analytical` | Strategic insights, economic analysis, predictions |
