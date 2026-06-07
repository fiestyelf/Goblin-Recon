---
name: goblin-recon
description: Operate the Goblin Recon agent — GenX Academy's AI-powered content research pipeline. 3-layer architecture (Trend Radar → Source Hunter → Moment Finder) for finding trending AI stories, locating source videos, and extracting 15–60 second clip moments. Trend detection is Instagram-first, TikTok-second. Covers script usage, delegate_task patterns, brand gate application, profile setup (SOUL.md + auto-load + skills), and end-to-end testing workflow.
category: genx-marketing
---

# Goblin Recon — Operational Skill

## What It Is

Goblin Recon is the intelligence division of the Goblin Bureau (GenX's AI agent suite). It runs **two separate pipelines**:

### Pipeline A: Social Pulse
**Purpose:** Content ideas, blogs, carousels, content strategy inspiration.
**Sources:** Instagram → TikTok → X → Reddit → Tech News
**Output:** Trending topics, hook styles, reel formats, carousel angles, blog ideas.
**NOT for:** Direct video clips.

Commands:
| Command | What It Does |
|---------|--------------|
| `run social pulse` | Full scan across IG/TikTok/X/Reddit/News for AI trends |
| `what's trending on Instagram` | IG-only creator account scan |
| `what's trending on TikTok` | TikTok-only trend scan |
| `blog ideas` | Social Pulse filtered for long-form content angles |
| `carousel ideas` | Social Pulse filtered for carousel-worthy topics |
| `content strategy this week` | Social Pulse + editorial calendar suggestions |

### Pipeline B: Clip Mine
**Purpose:** Direct video clips for the faceless Instagram page.
**Sources:** YouTube podcasts → Interviews → Keynotes
**Output:** Timestamped clips (15-60s), transcript quotes, engagement analytics, editor-ready briefs.
**This goes straight to editors.** They download the clip and produce the reel.

Commands:
| Command | What It Does |
|---------|--------------|
| `run clip mine` | Find best podcast clips from trending AI stories |
| `find clips about [topic]` | Source Hunter + Moment Finder for specific topic |
| `find the moment in [URL]` | Extract best clip from a specific video |
| `what clips are ready` | Show all approved clips awaiting editor handoff |

### Categorization (Both Pipelines)
Every item — Social Pulse idea or Clip Mine clip — is tagged by type:

| Category | What It Means |
|----------|--------------|
| **Latest AI News** | Breaking developments, product launches, policy changes |
| **Controversial/Polarizing** | Debates, backlash, hot takes, culture-war adjacent |
| **Upgrade/Democratization** | "Anyone can now do X," tool tutorials, barrier collapsing |
| **Analytical/Deep-dive** | Strategic insights, economic analysis, future predictions |

### General Commands
| Command | What It Does |
|---------|--------------|
| `run full scan` | Social Pulse + Clip Mine in sequence |
| `what formats are working?` | Current winning reel formats from IG/TikTok |
| `run competitor scan` | Competitor Scout |

## Trend Detection Priority (CRITICAL)

**Instagram and TikTok first. Always.** These platforms show what's ACTUALLY engaging — not just what journalists think is important. News sites (TechCrunch, Verge, VentureBeat, Ars Technica) are for **validation** — URLs, dates, journalistic verification. They are NOT the primary trend signal.

Priority order is absolute: **1. Instagram → 2. TikTok → 3. X/Twitter → 4. Reddit → 5. Tech News → 6. Product Hunt**

Instagram creator accounts to scan:
- @therundownai (491K) — carousel news digest
- @rowancheung (418K) — interview clips
- @inflecta.ai — narrative storytelling
- @ankitgupta.ai — AI tool showcases

Extract from Instagram: story, hook style, format type, view count, engagement metrics.
IG rules: public profiles only, no login bypass, stop if blocked. Min 50K views for signal.

## Project Location

The Goblin Recon project lives wherever you clone it. The structure:
```
goblin-recon/
├── SOUL.md          ← your identity file (copy to profile)
├── AGENTS.md        ← agent constitution
├── SESSION_LOG.md   ← changelog
├── config/          ← sources, scoring, brand-voice, security
├── memory/          ← brand-rules, trend/competitor history
├── scripts/         ← Python utilities (transcript, clip, scoring)
├── templates/       ← output templates
└── mcp.json         ← MCP server config (all optional)
```

Key files:
- `SOUL.md` — pre-made identity file. Copy to `~/.hermes/profiles/goblin-recon/SOUL.md`
- `AGENTS.md` — the agent's constitution (personality, rules, scoring, output format, trend priority)
- `SESSION_LOG.md` — every session's changes tracked here
- `config/sources.yaml` — source priority: Instagram → TikTok → X → Reddit → News
- `config/content-sources.yaml` — YouTube channels, IG accounts, TikTok creators
- `config/scoring.yaml` — scoring dimensions (social_velocity, scroll_stop, etc.)
- `config/brand-voice.yaml` — brand voice rules, blacklist, nuance words
- `config/security.yaml` — data collection policies, API key rules, rate limits
- `memory/brand-rules.md` — operational brand memory for the agent
- `scripts/` — Python utilities (transcript extraction, clip validation, engagement scoring)
- `templates/` — output templates (trend-report, clip-brief, competitor-report, content-brief)
- `mcp.json` — MCP server configuration (all optional, see pitfalls)

## Profile Setup (Hermes Desktop)

When a new user creates the goblin-recon profile, use the project setup script as the source of truth:

```bash
cd goblin-recon
bash scripts/setup.sh
```

The script installs the profile, SOUL.md, bundled skills, profile defaults, Python virtual environment, and dependencies.

### 1. SOUL.md Copy

A pre-made SOUL.md lives at the project root. From the project directory:

If setup fails to copy SOUL.md, copy it manually from the project root:
```bash
cp SOUL.md ~/.hermes/profiles/goblin-recon/SOUL.md
```

The SOUL.md contains everything the agent needs:
- Core identity and GenX Academy context (who we are, two brand doors, mission spine)
- Brand voice DNA (B2C/B2B tone, blacklist summary, nuance words)
- Personality and communication rules
- Trend detection philosophy (IG-first priority)
- Output standards (Decision-first, platform variants, phone-scannable)
- Security and compliance rules (compressed)
- Setup instructions for new users
- Maintenance guide (what to edit when things change)

See the file itself for the full content. It's self-documenting.

### 2. Skill Auto-Load
```bash
hermes config set skills.auto_load goblin-recon -p goblin-recon
```
This ensures the goblin-recon operational skill loads every time the profile starts. The agent always knows what it is.

### 3. Cherry-Picked Skills
Copy only the 5 marketing skills Goblin Recon needs (not all 55):
```bash
# From the source profile's desktop skills:
# competitor-profiling, social-content, copywriting, content-strategy, marketing-psychology
cp -r $SOURCE/skills/desktop/<skill> $GOBLIN/skills/desktop/<skill>
```
These cover: competitor research, social platform formats, caption writing, content planning, and engagement psychology. Skip: ad creative, email sequences, pricing, SEO, CRO, launch strategy, etc.

### 4. Model Config

Use whichever provider and model the company has approved. Example:

```bash
hermes -p goblin-recon config set model.provider openai
hermes -p goblin-recon config set model.default gpt-4o
hermes config set agent.max_turns 90 -p goblin-recon
hermes config set terminal.timeout 300 -p goblin-recon
```

Never paste or commit API keys. Store provider keys through Hermes secrets or another approved local secret method.

## How to Run the Pipeline

### Option A: Using delegate_task (Recommended for Speed)

Run Layers 1 and 2 in parallel as subagents, then Layer 3 sequentially:

```
# Layer 1 (Trend Radar): delegate_task with toolsets=["web","browser"]
# PRIORITY: Scan Instagram creator accounts FIRST (@therundownai, @rowancheung)
# Then TikTok hashtags, then X/Twitter, then tech news
# Return top 5-8 stories with: headline, IG views/engagement, format type, hook style
# Include both trending STORIES and trending FORMATS

# Layer 2 (Source Hunter): delegate_task with toolsets=["web","browser"]
# Search YouTube, Instagram, TikTok for videos about top stories
# Return video title, channel, URL, publish date, duration, views, format, captions?

# Layer 3 (Moment Finder): Run sequentially after picking best source
# 1. Use get_youtube_transcript.py to pull transcript
# 2. Analyze transcript for best 15-60s moment (prioritize scroll_stop, quotability)
# 3. Validate with extract_clip.py
```

### Option B: Manual Sequential (for Debugging)

Run each layer yourself using browser_navigate + browser_console for IG/TikTok scraping, then terminal for Python scripts.

## Script Usage

All scripts are in the project's `.venv`. Run from the project root:

```bash
PYTHONPATH=. .venv/bin/python scripts/get_youtube_transcript.py "<video_id_or_url>"
```

### get_youtube_transcript.py
Extracts transcripts with timestamps. Output: JSON array of `{time, duration, text}`.
- Pass video ID or full YouTube URL
- `--languages en,zh-Hans` to try multiple languages (English preferred for GenX)
- Returns `{"error": "...", "recoverable": true}` on failure

### extract_clip.py
Validates clip metadata. Output: JSON with `url_with_timestamp`, `embed_url`, `duration`, `start_time`, `end_time`.
- Usage: `extract_clip.py <video_url> <start_sec> <end_sec>`
- Enforces 15–60 second duration
- Automatically generates YouTube timestamp links

### score_engagement.py
Calculates engagement velocity score (0–20). Output: JSON with `score`, `velocity_per_hour`, `hours_since_post`.
- Usage: `score_engagement.py <platform> <post_url> <ISO_timestamp> <engagement_count>`
- Platforms: twitter, reddit, youtube, instagram
- Platform-specific benchmarks for viral thresholds

### check_secrets.py
Pre-commit security scan. Run before sharing or pushing:
```bash
.venv/bin/python scripts/check_secrets.py
```

## Clip Mine Scoring Criteria (7 Dimensions)

Every clip is scored out of 110 points. The agent applies these when scanning transcripts:

### 1. Scroll-Stop (15 pts) — THE MAIN TEST
"Would someone stop scrolling for this?"
- ✅ Concrete numbers, confrontational claims, revelations, emotional reactions
- ❌ Generic observations, pleasant conversation, "interesting" facts

### 2. Quotability (25 pts)
"Would someone screenshot this and share it?"
- ✅ Standalone soundbites, punchy phrasing, memorable analogies
- ❌ Rambling, needs context, requires knowing the speaker

### 3. Emotion (15 pts)
"Does it trigger a feeling?"
- ✅ Fear, awe, anger, excitement
- ❌ Flat delivery, neutral info, no stakes

### 4. Clarity (15 pts)
"Is the point clear without context?"
- ✅ First sentence tells the argument, no jargon, anyone understands
- ❌ Technical jargon, needs 20 minutes of prior context

### 5. Controversy (10 pts)
"Is this going to get comments?"
- ✅ Challenges conventional wisdom, contrarian strategy, polarizing take
- ❌ Safe takes, echoes the consensus

### 6. Visual Potential (10 pts)
"Can this work as a faceless reel with just text overlay?"
- ✅ Strong quote on screen, works with waveform + text
- ❌ Needs person's face to land, relies on visual demo

### 7. Brand Alignment (15 pts)
"Does this fit GenX Academy's voice?"
- ✅ B2B: Results not advice, operational detail, "here's what happened"
- ✅ B2C: Real science + real soul, truly seen, depth + play
- ❌ Hype language, hustle-bro, guru certainty, generic motivation

### Score Thresholds
| Score | Verdict |
|-------|---------|
| 85+ | 🔥 Killer clip. Ship immediately. |
| 70-84 | ⚡ Strong. Worth producing. |
| 55-69 | 📈 Decent. Produce if nothing better. |
| Below 55 | 🗑️ Skip. Won't land. |

### What the Agent Hunts For
When scanning a transcript, these patterns win:

| Pattern | Example | Category |
|---------|---------|----------|
| Number reveals | "80% of code is now AI-authored" | Latest AI News |
| Strategy contradictions | "Being first is expensive. Being right matters." | Analytical |
| Barrier collapsing | "Two nights with Claude docs, made $238K" | Upgrade |
| Industry callouts | "Companies are poisoning their own AI answers" | Controversial |
| Future predictions | "Today's AI will look like flip phones in 3 years" | Analytical |
| Behind-the-scenes | "The real reason Microsoft walked away" | Controversial |

## Clip Mine: End-to-End Process

### Phase 1: AI Discovers (Goblin Recon)
```
User says: "run clip mine"
         ↓
Goblin Recon:
  ├─ Scans Instagram/TikTok/X for trending AI stories
  ├─ Searches YouTube for podcasts covering those stories
  ├─ Pulls transcripts from the best videos
  ├─ Finds the strongest 30-60 second moments
  └─ Outputs a CLIP BRIEF with:
      - Timestamped URL (youtube.com/watch?v=XXX&t=308)
      - Transcript quote
      - Category tag
      - 7-dimension scores
      - Brand gate result
      - Caption for Instagram
```

### Phase 2: Human Reviews
Editor receives the clip brief. Options: APPROVE → Phase 3, SHELVE → skip, MODIFY → revise.

### Phase 3: Human Produces (Editor Steps)
```
1. Click the timestamped URL → video opens at exact clip start
2. Screen record the clip (QuickTime, OBS, or built-in recorder)
3. Add text overlay (key quote on screen)
4. Add subtitles (auto-generate then tweak)
5. Add visual elements (waveform, dark background, channel credit)
6. Export as vertical reel
7. Post with the caption Goblin Recon wrote
```

### How to Watch the Clip
The clip brief includes a URL like `youtube.com/watch?v=ABC&t=308`. The `&t=308` tells YouTube: "start at 308 seconds." Click it → video plays from the exact moment. No scrubbing. No searching.

### What Goblin Recon Does vs Does NOT Do
| Does | Does NOT Do |
|------|-------------|
| Find what's trending | Download videos |
| Find the best podcast/video | Screen record |
| Find the exact 30-60s moment | Add text overlay |
| Check brand gate | Add subtitles |
| Write the Instagram caption | Export reels |
| Tag by category | Post to Instagram |
| Give cut instructions to editors | |

**Goblin Recon is the brain. The editor is the hands.**

Full process reference: `references/clip-mine-process.md`

## Output Format

Every report MUST lead with `## Decision` — recommended action in the first 3 seconds. Follow templates:
- Trend reports → `templates/trend-report.md`
- Clip briefs → `templates/clip-mine-brief.md`
- Competitor reports → `templates/competitor-report.md`
- Content briefs → `templates/content-brief.md`

### Trend Report Must Include
- What's working on Instagram (formats, hooks, creators)
- What's on TikTok (formats, sounds, viral signals)
- News validation (tech news confirmation with URLs and dates)

### Clip Brief Must Include
- Decision (approve/shelve/modify)
- Video metadata (title, channel, views, URL)
- The moment text with exact timestamps
- Why post
- Scores by dimension (including scroll_stop)
- Brand gate result (angle, alignment score, blacklist violations)
- Platform variants (Instagram Reel, LinkedIn, YouTube Shorts)
- Fallback angle if rejected

## Winning Reel Formats (7 formats identified)

| Format | Hook | Best For |
|--------|------|----------|
| X vs Y comparison | "Which AI is most [X]?" | Model comparisons, tool face-offs |
| Shocking stat | "[N]% of [thing] is now [fact]" | Data stories, industry shifts |
| "They don't want you to know" | "How [group] is secretly [action]" | Exposé, manipulation stories |
| Celebrity controversy | "[Famous person] just [AI action]" | Hollywood, big names |
| Mind-blowing science | "This [thing] has no [X] but can [Y]" | Robotics, breakthroughs |
| Student vs system | "[Person] used [AI] and made [result]" | Democratization, tool tutorials |
| Quote card | "[Authority]: '[provocative quote]'" | CEO interviews, predictions |

## Testing Workflow (End-to-End)

1. **Layer 1** — Browser-based IG creator scan + TikTok hashtags + news sites
2. **Score stories** — Apply social_velocity first, then remaining dimensions. Confirm all >60.
3. **Layer 2** — Browser-based YouTube/IG/TikTok search for top 2–3 stories
4. **Pick best source** — Prioritize podcast/interview, English captions available, high scroll_stop
5. **Layer 3** — Extract transcript, find best moment, validate with extract_clip.py
6. **Brand gate** — Check blacklist, nuance words, brand angle. Score ≥8/15.
7. **Clip brief** — Follow template with platform variants

First test run (June 6, 2026): 5 stories found, 43-second clip extracted, full pipeline ~7 min. See `references/pipeline-test-jun-06-2026.md`.

## Session Discipline

Every session, update `SESSION_LOG.md` in the project root. Format:
```
## Session N — [Date]
### Changes Made
| File | Change | Reason |
### Test Results
| Test | Result |
### Open Items
- [ ] ...
```

## Pitfalls

### English-Only Captions
The `get_youtube_transcript.py` script may return non-English captions. GenX brand rules require English-only outward content. Always check language before committing. Fall back to alternative sources.

### Instagram Scraping Is Fragile
Cookie walls and login gates block some accounts. Works for public profiles but unreliable at scale. The Meta API (disabled in config) would fix this. Until then, accept manual IG monitoring as fallback.

### MCPs Are Optional
The entire pipeline runs on Hermes built-in tools (browser, web, terminal). The MCPs in `mcp.json` (memory, fetch, ghost-browser) are supplementary. The only one worth enabling early is `memory` for persisting brand-gate decisions. Ghost-browser is redundant with Hermes' built-in browser.

### Competitor Config Is Empty
`config/competitors.yaml` has zero entries. `run competitor scan` produces nothing until filled.

### Some YouTube Channel IDs Incomplete
Lex Fridman ID was truncated (fixed in Session 1). AI Exchange and AI Explained still have empty strings.

### delegate_task Subagents Don't Share Context
Pass all necessary context explicitly — source URLs, search queries, story topics, IG creator handles.

### Tests Require PYTHONPATH
```bash
cd goblin-recon  # or wherever you cloned the project
PYTHONPATH=. .venv/bin/python -m unittest tests.test_scripts -v
```

### setup.sh Handles Full Setup
The `scripts/setup.sh` handles the complete setup: profile creation, SOUL.md installation, skill installation, auto-load configuration, Python venv, and verification. One command, done.

### Model Choice Matters
Layer 1 benefits from a capable model for multi-site scraping + scoring. Use the strongest approved provider/model available for full scans; use lighter approved models for bulk drafts.

### Never Hardcode User Paths — This Is Public, Not Personal
Goblin Recon is distributed to other users. Every path in SOUL.md, SKILL.md, AGENTS.md, setup scripts, and config references must be **project-root-relative** or use `~/.hermes/` (the one portable Hermes path).

❌ BANNED: any absolute user-home path, such as a local Desktop, Documents, or home-directory path.
✅ REQUIRED: `goblin-recon/` (relative from project root), `~/.hermes/profiles/goblin-recon/` (portable Hermes path), `./scripts/...`, `SOUL.md` (same directory).

**Test rule:** If a new user clones the repo into `~/Documents/` instead of `~/Desktop/`, every command in every file must still work. Zero find-and-replace-your-name steps. If you add a path to any file, ask: "Would this break if someone cloned this into a different directory?"

This rule was enforced in Session 3 after 6 hardcoded paths were found across SOUL.md and SKILL.md.

## Project Memory Files

Load before producing output:
- `memory/brand-rules.md` — Brand architecture, mission spine, B2C/B2B rules, audience profiles
- `memory/trend-history.md` — Previous trend scan results (avoid repeats)
- `memory/competitor-snapshots.md` — Previous competitor scan results
- `memory/content-performance.md` — Live content performance for scoring improvement

## Related Skills

- `genx-market-researcher` — Market research persona
- `genx-truth-teller` — Quality gate for GenX marketing outputs
- `genx-copy-chief` — Copywriting for GenX Academy (clip captions, platform variants)
- `competitor-profiling` — Cherry-picked for competitor scan research
- `social-content` — Cherry-picked for IG/TikTok platform variants and format analysis
- `copywriting` — Cherry-picked for caption writing
- `content-strategy` — Cherry-picked for weekly content planning
- `marketing-psychology` — Cherry-picked for engagement mechanics

## Reference Files

- `references/soul-md-example.md` — Canonical SOUL.md for goblin-recon profile
- `references/pipeline-test-jun-06-2026.md` — First end-to-end test results
- `references/session-2-bifurcation.md` — Session 2 bifurcation details
- `references/clip-mine-process.md` — Full Clip Mine workflow: AI discovery → scoring → editor production
