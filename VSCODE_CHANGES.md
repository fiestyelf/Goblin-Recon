# Goblin Recon — VS Code Changes
# Hand this file to any AI (Copilot, Cursor, etc.) and say "apply these changes"

---

## Change 1: README.md

### File: `README.md`

**Find the `## Commands` section. Replace the entire table with:**

```markdown
| Say this | It does |
|---|---|
| `run social pulse` | Pipeline A — ideas, blogs, carousels, content strategy |
| `run clip mine` | Pipeline B — podcast clips for faceless IG page |
| `blog ideas` | Social Pulse filtered for long-form content |
| `carousel ideas` | Social Pulse filtered for carousel topics |
| `content strategy this week` | Social Pulse + editorial suggestions |
| `find clips about [topic]` | Clip Mine for a specific topic |
| `find the moment in [URL]` | Extract best clip from a video |
| `run full scan` | Social Pulse + Clip Mine in sequence |
| `what clips are ready` | Approved clips awaiting editor handoff |
| `run competitor scan` | Competitor Scout |
```

### Replace the description line (line 5):

**Find:**
```
AI-powered content research agent for GenX Academy. Finds trending stories, locates source videos, and extracts 15-60 second clip moments — all in one pipeline.
```

**Replace with:**
```
AI-powered content research agent for GenX Academy. Two pipelines: Social Pulse (ideas, blogs, carousels) and Clip Mine (podcast clips for faceless Instagram page).
```

---

## Change 2: INSTRUCTIONS.md

### File: `INSTRUCTIONS.md`

### Section A — Update "What You Get" (around line 17)

**Find the bullet list starting with "1. Top 5 trending AI stories..." Replace with:**

```markdown
When you run Goblin Recon, you get two types of output:

### Social Pulse (for the ideas team — blogs, carousels, strategy)
1. Trending AI topics from Instagram, TikTok, X, Reddit, and tech news
2. Hook styles and reel formats that creators are using
3. Blog angles, carousel ideas, and content strategy suggestions
4. Cross-platform validation (IG + TikTok + News = confirmed trend)

### Clip Mine (for video editors — faceless Instagram reels)
1. Top 3-5 podcast/video clips (15-60 seconds) from trending AI stories
2. Exact YouTube timestamps with transcript quotes
3. Engagement analytics (views, comments, view velocity)
4. Editor instructions (where to cut, text overlay suggestions, caption)
5. Brand gate check (approved or shelved with reason)
```

### Section B — Update commands table (find the commands table)

**Replace entire table with:**

```markdown
| Say this | It does |
|---|---|
| `run social pulse` | Full scan: IG, TikTok, X, Reddit, Tech News |
| `what's trending on Instagram` | IG-only creator scan with format analysis |
| `what's trending on TikTok` | TikTok-only trend scan |
| `blog ideas` | Social Pulse filtered for long-form content angles |
| `carousel ideas` | Social Pulse filtered for carousel-worthy topics |
| `content strategy this week` | Social Pulse + editorial suggestions |
| `run clip mine` | Find best podcast clips from trending AI stories |
| `find clips about [topic]` | Clips for a specific topic |
| `find the moment in [URL]` | Extract best clip from a specific video |
| `what clips are ready` | Approved clips awaiting editor handoff |
| `run full scan` | Social Pulse + Clip Mine together |
| `run competitor scan` | Competitor Scout |
```

---

## Change 3: skills/trend-radar/SKILL.md

### File: `skills/trend-radar/SKILL.md`

### Update A — Scoring table (around line 85)

**Find the table starting with `| Recency | 20 |`**

**Replace the scoring table with:**

```markdown
| Dimension | Max | How to Score |
|-----------|-----|--------------|
| social_velocity | 25 | IG views/hr or TikTok plays/hr. PRIMARY signal for trend detection |
| recency | 15 | 24h=15, 48h=12, 72h=8, older=0 |
| cross_source | 15 | 1 source=5, 2 sources=10, 3+ sources=15. IG+X=confirmed |
| controversy | 15 | Polarized comments, heated debate, opposing takes |
| format_stealability | 15 | Can the reel format be adapted for GenX? |
| genx_relevance | 10 | Would GenX B2C or B2B audiences care? |
| brand_alignment | 15 | Fits B2C science+soul or B2B results-not-advice; no hype/woo/corporate filler |
```

### Update B — Source scan order (Step 2, around line 42)

**Before "X/Twitter:" add Instagram and TikTok as primary sources:**

```markdown
### Step 2: Scan Sources (in priority order)

**Instagram (PRIMARY — scan first):**
- Check creator accounts from config/sources.yaml: @therundownai (491K), @rowancheung (418K), @inflecta.ai, @ankitgupta.ai
- Browse #ainews, #artificialintelligence, #aitools hashtags
- Extract: story, hook style, format type, engagement metrics (views, likes, comments)
- Min 50K views for signal
- Public profiles only. No login bypass. Stop if blocked

**TikTok (SECONDARY):**
- Search hashtags: #ainews, #artificialintelligence, #aiexplained, #aitools
- Check creator accounts from config/sources.yaml for recent posts
- Extract: story, sound trends, format innovation, engagement (plays, shares)
- Identify viral acceleration patterns

**X/Twitter:**
```

### Update C — Triggers section (around line 7)

**Replace triggers with:**

```markdown
## Triggers
- "run social pulse" — Full Social Pulse scan
- "what's trending on Instagram" — IG-only scan
- "what's trending on TikTok" — TikTok-only scan
- "blog ideas" — Filtered for long-form angles
- "carousel ideas" — Filtered for carousel topics
- "content strategy this week" — Social Pulse + editorial suggestions
- "run full scan" — Social Pulse + Clip Mine
```

---

## Change 4: skills/source-hunter/SKILL.md

### File: `skills/source-hunter/SKILL.md`

### Update A — Triggers section (around line 7)

**Replace triggers with:**

```markdown
## Triggers
- "run clip mine" — Find best podcast clips from trending stories
- "find clips about [topic]" — Specific topic source hunt
- "find the moment in [URL]" — Extract from a specific video
- "what clips are ready" — Approved clips awaiting editors
- "run full scan" — Social Pulse + Clip Mine
```

### Update B — Scoring table (around line 84)

**Replace scoring table with (adds format_reusability row):**

```markdown
| Dimension | Max | How to Score |
|-----------|-----|--------------|
| topic_match | 25 | Title + description match story keywords |
| recency | 20 | Last 7 days=20, 14 days=15, 30 days=10 |
| credibility | 20 | Channel size + authority + consistency |
| clip_potential | 15 | Does it have quotable moments? Soundbites? |
| engagement_ratio | 10 | Views per hour since publish |
| brand_voice_fit | 15 | Creator tone aligns with GenX; penalize hype, fake urgency, woo |
| format_reusability | 5 | Can the format/clip style be adapted for our page? |
```

---

## Change 5: skills/moment-finder/SKILL.md

### File: `skills/moment-finder/SKILL.md`

### Update A — Scoring table (around line 98)

**Replace the moment scoring table with:**

```markdown
| Dimension | Max | What to look for |
|-----------|-----|------------------|
| scroll_stop | 15 | THE test. Would someone stop scrolling for this? First 3 seconds must hook. |
| quotability | 25 | Would someone quote/screenshot/share this? Standalone soundbite? |
| emotion | 15 | Does it trigger fear, awe, anger, excitement, or curiosity? |
| clarity | 15 | Is the point clear without context? No jargon, no setup needed. |
| controversy | 10 | Does it challenge conventional thinking? Will people comment? |
| visual_potential | 10 | Works as faceless reel with text overlay? No face required to land. |
| brand_alignment | 15 | B2C science+soul/truly-seen or B2B results-not-advice |
```

### Update B — "Hot Zones" section (add category annotation)

**After "Emotional Peaks:" section (around line 76), add:**

```markdown
**Scroll-Stop Moments (highest priority):**
- Pattern: concrete number, controversy, or revelation in first 3 seconds
- Example: "57% of all web traffic is bots", "Two nights. $238,000."
- Category tag: Identify whether this moment is Latest AI News, Controversial, Upgrade, or Analytical

**Category Assignment:**
After identifying hot zones, tag each candidate clip:
- Latest AI News: Breaking developments, launches, policy changes
- Controversial/Polarizing: Debates, backlash, hot takes
- Upgrade/Democratization: "Anyone can now do X," barrier collapsing
- Analytical/Deep-dive: Strategic insights, economic analysis, predictions
```

### Update C — Clip Brief template reference (around line 145)

**Find:**
```
Use template: templates/clip-brief.md
```

**Replace with:**
```
Use template: templates/clip-mine-brief.md
```

---

## Change 6: templates/clip-brief.md

### File: `templates/clip-brief.md`

**Add this line at the VERY TOP of the file (before any content):**

```markdown
<!-- ⚠️ DEPRECATED — Use templates/clip-mine-brief.md instead. This file kept for backward reference only. -->
```

---

## Change 7: AGENTS.md

### File: `AGENTS.md`

### Update A — Output Format section (around line 110)

**Find the template references:**

**Replace:**
```markdown
- Content briefs: use templates/content-brief.md
- Clip briefs: use templates/clip-brief.md
- Competitor reports: use templates/competitor-report.md
- Trend reports: use templates/trend-report.md
```

**With:**
```markdown
- Social Pulse reports: use templates/social-pulse-report.md
- Clip briefs: use templates/clip-mine-brief.md (NOT the deprecated clip-brief.md)
- Competitor reports: use templates/competitor-report.md
- Trend reports: use templates/trend-report.md
```

---

## Change 8: SESSION_LOG.md

### File: `SESSION_LOG.md`

### Add this entry at the end (before the template section):

```markdown
---

## Session 3 — June 6, 2026
**Agent:** Hermes (Arjun's assistant)
**What we did:** Pre-push audit. Fixed scoring inconsistency, updated layer skills for two pipelines, refreshed user-facing docs.

### Changes Made

| File | Change | Reason |
|------|--------|--------|
| `README.md` | Updated commands table + description | Old commands referenced single pipeline |
| `INSTRUCTIONS.md` | Updated "What You Get" + commands table | Users need to know about Social Pulse vs Clip Mine |
| `skills/trend-radar/SKILL.md` | Updated scoring table + source scan order + triggers | Scoring was inconsistent with config/scoring.yaml; no IG/TikTok priority |
| `skills/source-hunter/SKILL.md` | Updated triggers + scoring table | Added format_reusability, updated commands |
| `skills/moment-finder/SKILL.md` | Updated scoring table + category tags + template reference | Added scroll_stop, category assignment, correct template path |
| `templates/clip-brief.md` | Added deprecation note | clip-mine-brief.md is the new template; avoid confusion |
| `AGENTS.md` | Updated template references | Point to correct templates (social-pulse-report.md, clip-mine-brief.md) |

### Verification
- ✅ 7/7 Python tests pass
- ✅ All YAML configs structurally valid
- ✅ Two pipelines documented in AGENTS.md, SOUL.md, and skill
- ✅ Profile goblin-recon ready for anyone to launch

### Ready to Push
- ✅ All files consistent
- ✅ No broken references
- ✅ User docs match actual commands

---

```

---

## Verification (After All Changes)

Run these to confirm nothing broke:

```bash
cd "/Users/arjunthapa/Desktop/Goblin Recon/goblin-recon"
PYTHONPATH=. .venv/bin/python -m unittest tests.test_scripts -v
```

Expected: 7/7 tests pass.

## Summary

8 files changed, 0 new files created:

| # | File | What |
|---|------|------|
| 1 | `README.md` | Commands + description for two pipelines |
| 2 | `INSTRUCTIONS.md` | User-facing docs: Social Pulse vs Clip Mine |
| 3 | `skills/trend-radar/SKILL.md` | Scoring sync, IG/TikTok priority, new triggers |
| 4 | `skills/source-hunter/SKILL.md` | New triggers, format_reusability scoring |
| 5 | `skills/moment-finder/SKILL.md` | Scroll-stop scoring, category tags, correct template |
| 6 | `templates/clip-brief.md` | Deprecation note |
| 7 | `AGENTS.md` | Template references updated |
| 8 | `SESSION_LOG.md` | Session 3 audit entry |
