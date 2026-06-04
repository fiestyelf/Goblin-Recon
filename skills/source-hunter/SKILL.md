# Source Hunter — Layer 2

## Purpose
Find YouTube videos and Instagram content discussing each trending story from Layer 1.

## Triggers
- Automatic chain from Layer 1 (trend-radar)
- "find sources for [topic]"
- "where are people talking about this"

## Tools Required
- browser (for YouTube, Instagram search)
- web_search
- config/content-sources.yaml
- config/scoring.yaml
- scripts/get_youtube_transcript.py

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

### Step 3: Score Each Source

For each video/reel, calculate score (0-100):

| Dimension | Max | How to Score |
|-----------|-----|--------------|
| Topic match | 30 | Title + description match story keywords? |
| Recency | 20 | Last 7 days = 20, 14 days = 15, 30 days = 10 |
| Credibility | 20 | Channel size + authority + consistency |
| Clip potential | 15 | Does it have quotable moments? |
| Engagement ratio | 15 | Views / hours since publish |

**Threshold:** 65/100 to advance. Below = skip.

### Step 4: Select Top Sources
- Must score > 65/100
- At least 1 YouTube + 1 Instagram per story (when available)
- Maximum 5 sources per story

### Step 5: Pull Transcripts (YouTube Only)
```
For each selected YouTube video:
  1. Run: python scripts/get_youtube_transcript.py <video_id>
  2. Save transcript to memory
  3. If transcript unavailable, flag as "no transcript"
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
   URL: [link]
   Transcript: [available/not available]

2. [Instagram] "[reel caption]"
   Account: [name] | Likes: [count] | Posted: [date]
   Score: [score]/100
   URL: [link]
   Transcript: [available/not available]

SUMMARY:
- YouTube sources: [count]
- Instagram sources: [count]
- Transcripts available: [count]
```

### Step 7: Chain to Layer 3
- Pass selected sources to moment-finder
- Include transcripts for videos that have them
- Note videos without transcripts (skip in Layer 3)

## Output
- Source list per story with URLs, channel names, and engagement data
- Transcripts for YouTube videos
- Clear indication of which sources have transcripts

## Error Handling
- If YouTube search returns no results, note "No YouTube sources found"
- If Instagram search returns no results, note "No Instagram sources found"
- If transcript pull fails, flag video and continue with next
- If no sources pass threshold, report "No viable sources found for this story"

## Quality Checks
- [ ] Sources are public or approved
- [ ] All sources have URLs
- [ ] All sources have publication dates
- [ ] Transcripts pulled for YouTube videos
- [ ] No sources older than 30 days
- [ ] Scores calculated correctly
- [ ] No personal account cookies, tokens, or private data used
