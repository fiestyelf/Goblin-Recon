# Goblin Recon — Command Reference

> v1.1 — June 21, 2026
> 35 commands across 7 workflows

---

## Overview

Goblin Recon has 33 simple commands across 6 workflows. You type the command in plain English, and Goblin Recon picks the right workflow.

Commands are not case-sensitive. Words in `[brackets]` mean you add your own topic, URL, or ID.

---

## 1. Social Pulse — Trend Discovery

Social Pulse finds trending AI stories, hooks, formats, and content angles. It is intelligence, not production — it does not produce editor-ready clips.

### Scan Commands

| Command | Description | Scan Mode | Sources |
|---------|------------|-----------|---------|
| `run social pulse` | Find content ideas, blog angles, and hooks | Deep Social | IG → TikTok → X → Reddit → Tech News |
| `run fast scan` | Quick daily trend check | Fast | YouTube, Reddit, Tech News, Product Hunt |
| `run deep social scan` | Deeper Instagram and TikTok trend check | Deep Social | IG/TikTok first, then X/Reddit/News |
| `run signal scan` | Find early AI signals before they are mainstream | Signal | X, Hacker News, GitHub, ArXiv |
| `manual scan this [URL/screenshot/caption]` | Score something you paste in | Manual | Your URL, screenshot, caption, or notes |

### Platform-Specific Scans

| Command | Description |
|---------|------------|
| `trending on Instagram` | Find Instagram trends and creator hooks |
| `trending on TikTok` | Find TikTok trends, sounds, and formats |

### Content Strategy

| Command | Description |
|---------|------------|
| `blog ideas` | Get article ideas from current trends |
| `carousel ideas` | Get swipe-post ideas from current trends |
| `content strategy` | Get a simple weekly posting plan |
| `trending formats` | See reel and carousel formats working now |

---

## 2. Clip Mine — Video Clip Production

Clip Mine finds source videos and extracts 15–60 second editor-ready moments. Output goes directly to editors for reel production.

### Core Commands

| Command | Description | Layers Run |
|---------|------------|------------|
| `run clip mine` | Find short video clip ideas from trends | Trend → source → moment |
| `find clips about [topic]` | Find clips about one topic | Source → moment |
| `find the moment in [URL]` | Pick the best short clip from one video | Moment only |

### Combined Scan

| Command | Description |
|---------|------------|
| `run full scan` | Find trends, then clips for the best ones |

---

## 3. Clip Vault — Persistent Storage

Clip Vault retrieves and manages stored clips across sessions. Storage backend: `vault/clips.db` + `vault/briefs/`.

| Command | Description |
|---------|------------|
| `clips ready` | Show approved clips ready for editors |
| `search clips [query]` | Search saved clips by topic |
| `show clip [id]` | Show one saved clip |
| `update clip [id] status [status]` | Change a saved clip status |

---

## 4. Competitor Scout — Market Intelligence

Competitor Scout monitors competitor pricing, features, positioning, and marketing activity. It runs standalone — not chained into Social Pulse or Clip Mine.

| Command | Description | Depth |
|---------|------------|-------|
| `run competitor scan` | Check competitors and suggest next moves | Homepage + key pages |
| `check competitors` | Quick competitor check | Homepage only |
| `competitor deep scan` | Check more competitor pages | All key public pages |
| `competitor gap analysis` | Compare competitors with GenX Academy | Both sites |
| `competitor gap reverse [name]` | Show what GenX may be missing | GenX site check |
| `compare SEO` | Compare basic SEO signals | Both sites |

---

## 5. Email Hook — Outbound Email Generation

Email Hook generates and validates subject lines, openers, and short email drafts. All output passes through `email_gate` before delivery.

| Command | Description |
|---------|------------|
| `write email hooks for [offer]` | Write and score five subject lines and openers |
| `write subject lines for [campaign]` | Write subject lines for one campaign |
| `validate this email` | Check if an email is ready or needs changes |

---

## 6. System Commands

| Command | Description |
|---------|------------|
| `register all skills` | Refresh the skills list |
| `sync from github` | Pull the latest repo files into the profile |

---

## Intent Routing Map

The orchestrator classifies every command into one primary workflow before tool invocation begins.

| User Says | Routes To | Chains |
|-----------|-----------|--------|
| `run social pulse`, `run fast scan`, `run deep social scan`, `run signal scan`, `manual scan this [URL/screenshot/caption]`, `trending on Instagram`, `trending on TikTok` | Social Pulse | Find trends and save a report |
| `blog ideas`, `carousel ideas`, `content strategy`, `trending formats` | Social Pulse | Find trends and turn them into the requested format |
| `run clip mine`, `run full scan` | Clip Mine | Find trends, sources, and clip moments |
| `find clips about [topic]` | Clip Mine | Find sources and clip moments for one topic |
| `find the moment in [URL]` | Clip Mine | Find the best clip moment from one video |
| `clips ready`, `search clips [query]`, `show clip [id]`, `update clip [id] status [status]` | Clip Vault | Search or update saved clips |
| `run competitor scan`, `check competitors`, `competitor deep scan`, `competitor gap analysis`, `competitor gap reverse`, `compare SEO` | Competitor Scout | Check competitors and save a report |
| `write email hooks for [offer]`, `write subject lines for [campaign]`, `validate this email` | Email Hook | Write or check email copy |
| `register all skills`, `sync from github` | System | Run the system task and confirm it finished |

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
| Carousel Generator | `vault/carousels/YYYY-MM-DD-{topic}-{brand_slug}/` |

---

## 7. Carousel Generator — Social Image Production

Carousel Generator builds multi-slide carousels and single social images. Asks 3 questions, renders editable layer files, exports to `vault/carousels/`.

| Command | Description |
|---------|------------|
| `run carousel generator` | Build a multi-slide carousel for Instagram or Facebook |
| `generate single post` | Make one social image for a topic |

---

## Scan Mode Reference

| Mode | Use Case | Primary Sources | Skip |
|------|----------|----------------|------|
| **Fast Scan** | Quick daily check | YouTube, Reddit, Tech News, Product Hunt | IG/TikTok if blocked |
| **Deep Social Scan** | Deeper social check | IG/TikTok first, then X, Reddit, News | Nothing by default |
| **Signal Scan** | Early idea check | X, Hacker News, GitHub, ArXiv | Older items |
| **Manual Assisted** | User gives the material | URLs, screenshots, captions, notes | Automated source hunting |

---

## Category Tags

Every Social Pulse item and Clip Mine clip is tagged with one of four categories:

| Tag | Meaning |
|-----|---------|
| `Latest AI News` | Breaking developments, product launches, policy changes |
| `Controversial` | Debates, backlash, hot takes |
| `Upgrade` | Tool tutorials, barrier collapsing, democratization |
| `Analytical` | Strategic insights, economic analysis, predictions |
