# Source Hunter — Layer 2

## Purpose
Find YouTube videos and Instagram content discussing each trending story from Layer 1.

## Triggers
- "run clip mine" — Find best podcast clips from trending stories
- "find clips about [topic]" — Specific topic source hunt
- "find the moment in [URL]" — Extract from a specific video
- "what clips are ready" — Approved clips awaiting editors
- "run full scan" — Social Pulse + Clip Mine

## Tools Required
- browser (for YouTube, Instagram search)
- web_search
- config/content-sources.yaml
- config/scoring.yaml
- config/brand-voice.yaml
- memory/brand-rules.md
- goblin_recon.tools.youtube_tool

## Optional Helpers
- MCP Fetch: extract approved public source pages when standard web_extract is weak
- GPT Researcher: optional deep-research helper only when sources are thin or the topic is complex
- MCP Memory: compare candidate sources with previously approved/shelved source patterns

## Execution Flow

### Step 0: Security Preflight
- Read config/security.yaml
- Search public YouTube and public Instagram surfaces only
- Do not use personal social accounts for automation
- Do not bypass login gates, captchas, paywalls, or platform restrictions
- If Instagram access requires login-only browsing, mark source as unavailable unless approved

### Step 1: Read Configuration
```
Load config/content-sources.yaml for channels and accounts
Load config/scoring.yaml for scoring weights
Load config/brand-voice.yaml for creator/source voice fit
Load memory/brand-rules.md for B2C/B2B brand positioning
```

### Step 2: For Each Trending Story

**YouTube Search:**
```
For each story from Layer 1:
  1. Extract keywords from headline
  2. Run search queries:
     - "[keywords] podcast 2026"
     - "[keywords] interview"
     - "[keywords] explained"
     - "[keywords] debate"
  3. Filter: uploaded in last 7 days
  4. Sort by: view count (engagement velocity)
  5. Result: top 5-8 videos
```

**Instagram Search:**
```
For each story from Layer 1:
  1. Search tags from config/content-sources.yaml
  2. Check tech_accounts from config for relevant posts
  3. Filter: posted in last 3 days
  4. Result: top 3-5 reels
```

**Optional Deep Research Helper:**
```
Use GPT Researcher only if:
  - normal search finds fewer than 2 credible sources, or
  - the topic is high-value but technically complex, or
  - source credibility is unclear.

Rules:
  - Treat GPT Researcher output as leads, not final evidence.
  - Verify every source URL and publication date yourself.
  - Do not replace Source Hunter scoring or brand_voice_fit.
```

### Step 3: Score Each Source

For each video/reel, calculate score (0-100):

| Dimension | Max | How to Score |
|-----------|-----|--------------|
| topic_match | 20 | Title + description match story keywords |
| recency | 15 | Last 7 days=15, 14 days=10, 30 days=5 |
| credibility | 20 | Channel size + authority + consistency |
| clip_potential | 15 | Does it have quotable moments? Soundbites? |
| engagement_ratio | 10 | Views per hour since publish |
| brand_voice_fit | 15 | Creator tone aligns with GenX; penalize hype, fake urgency, woo |
| format_reusability | 5 | Can the format/clip style be adapted for our page? |

**Threshold:** 65/100 to advance. Below = skip.

**Brand source filter:**
- Prefer creators with earned authority, clarity, substance, and non-hype delivery.
- Penalize manufactured urgency, empty promises, hustle-bro tone, woo, and generic advice content.
- Flag sources that are useful for market context but off-brand for direct repurposing.
- If brand_voice_fit < 8/15, skip unless the source is needed only as supporting evidence.

**Competitor overlap check:**
- Check whether the source angle is already heavily owned by competitors from config/competitors.yaml or known competitor positioning.
- If competitors are already using the same angle, either find a more ownable source moment or mark the source as context-only.
- Prefer sources that allow GenX to say something competitors are missing.

**Voice calibration anchors:**
- Prefer grounded proof, lived experience, operator detail, precise language, and emotionally true observations.
- Penalize generic motivation, guru certainty, corporate filler, empty transformation language, and advice without implementation.

### Step 4: Select Top Sources
- Must score >= 65/100
- At least 1 YouTube + 1 Instagram per story (when available)
- Maximum 5 sources per story

### Step 5: Pull Transcripts (YouTube Only)
```
For each selected YouTube video:
  1. Run: python -m goblin_recon.tools.youtube_tool <video_id>
  2. Use transcript locally to identify candidate moments
  3. Store only source URL, timestamps, and short excerpts by default
  4. If transcript unavailable, flag as "no transcript"
```

### Step 6: Generate Source Report

For each story, output:
```
STORY: [headline]
Trend Score: [score]/100

SOURCES FOUND:
1. [YouTube] "[video title]"
   Channel: [name] | Views: [count] | Posted: [date]
   Score: [score]/100
   Brand Voice Fit: [score]/15 | Brand Angle: [B2C/B2B/Both]
   Competitor Overlap: [low/medium/high]
   Voice Calibration: [strong/medium/weak]
   Blacklist Flags: [none/list]
   URL: [link]
   Transcript excerpt: [short excerpt available/not available]

2. [Instagram] "[reel caption]"
   Account: [name] | Likes: [count] | Posted: [date]
   Score: [score]/100
   Brand Voice Fit: [score]/15 | Brand Angle: [B2C/B2B/Both]
   Competitor Overlap: [low/medium/high]
   Voice Calibration: [strong/medium/weak]
   Blacklist Flags: [none/list]
   URL: [link]
   Transcript: [available/not available]

SUMMARY:
- YouTube sources: [count]
- Instagram sources: [count]
- Transcript excerpts available: [count]
```

### Step 7: Chain to Layer 3
- Pass selected sources to moment-finder
- Include source URL, candidate timestamps, and short transcript excerpts for videos that have them
- Note videos without transcripts (skip in Layer 3)

## Output
- Source list per story with URLs, channel names, and engagement data
- Short transcript excerpts for YouTube videos when needed for moment selection
- Clear indication of which sources have transcript access

## Error Handling
- If YouTube search returns no results, note "No YouTube sources found"
- If Instagram search returns no results, note "No Instagram sources found"
- If transcript pull fails, flag video and continue with next
- If no sources pass threshold, report "No viable sources found for this story"

## Quality Checks
- [ ] Sources are public or approved
- [ ] All sources have URLs
- [ ] All sources have publication dates
- [ ] Transcript access checked for YouTube videos; only short excerpts retained by default
- [ ] No sources older than 30 days
- [ ] Scores calculated correctly
- [ ] Brand Voice Fit scored for every source
- [ ] Competitor overlap checked before advancing a source
- [ ] Voice calibration anchors checked for every source
- [ ] Off-brand hype/woo/advice-merchant sources are skipped or clearly flagged
- [ ] Blacklist scan completed for source titles/captions
- [ ] No personal account cookies, tokens, or private data used
