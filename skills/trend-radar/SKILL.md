# Trend Radar — Layer 1

## Purpose
Find today's top 5 trending AI stories from multiple sources.

## Triggers
- "find trending stories"
- "what's buzzing"
- "daily scan"
- "trending AI"

## Tools Required
- web_search
- web_extract
- browser (for Reddit, Product Hunt)
- config/sources.yaml
- config/scoring.yaml
- config/brand-voice.yaml
- memory/brand-rules.md

## Optional Helpers
- MCP Memory: store approved/shelved trend patterns after human review
- MCP Fetch: cleaner extraction from approved public pages
- TrendRadar-style inputs: RSS feeds, keyword filters, and multi-platform alerts as extra signals only

## Execution Flow

### Step 0: Security Preflight
- Read config/security.yaml
- Use public sources only
- Do not use private accounts, personal cookies, paywall bypasses, or captcha bypasses
- Stop scanning a source if access is denied or rate-limited

### Step 1: Read Configuration
```
Load config/sources.yaml for source list
Load config/scoring.yaml for scoring weights
Load config/brand-voice.yaml for brand gate and blacklist
Load memory/brand-rules.md for B2C/B2B positioning
```

### Step 2: Scan Sources (Parallel)

**X/Twitter:**
- Search each query from sources.yaml
- Monitor accounts_to_monitor for new posts
- Collect: URL, text, timestamp, engagement (likes, retweets, replies)
- Calculate velocity: engagement / hours_since_post

**Reddit:**
- Visit each subreddit from sources.yaml
- Sort by: hot
- Filter: min_upvotes from config
- Collect: URL, title, subreddit, score, comment count, timestamp

**Tech News Sites:**
- web_extract each site URL from config
- Scan headlines for AI-related stories
- Collect: URL, headline, publication date

**Product Hunt:**
- Visit AI topic page
- Filter: last 24 hours
- Collect: URL, product name, tagline, upvotes

**Hacker News:**
- web_extract front page
- Filter: AI-related stories
- Collect: URL, title, score, comments

**Optional RSS / Alert Inputs:**
- If configured, read approved RSS feeds or TrendRadar-style alert outputs as another public signal source.
- Treat these as leads, not truth. Every item still needs URL, publication date, and normal Goblin Recon scoring.
- Do not let external trend tools replace this skill's brand gate or scoring logic.

### Step 3: Deduplicate Stories
- Group stories that cover the same topic
- A story is "same" if 2+ sources report it
- Keep the best URL for each story (prefer primary source)

### Step 4: Score Each Story

For each unique story, calculate score (0-100):

| Dimension | Max | How to Score |
|-----------|-----|--------------|
| Recency | 20 | 24h = 20, 48h = 15, 72h = 10, older = 0 |
| Velocity | 20 | Use scripts/score_engagement.py |
| Cross-source | 15 | 1 source = 5, 2 sources = 10, 3+ = 15 |
| Controversy | 15 | Polarized comments, opposing takes |
| Visual potential | 15 | Can this be a faceless reel? |
| GenX relevance | 10 | Would GenX B2C/B2B audiences care? |
| Brand alignment | 15 | Fits B2C science+soul or B2B results-not-advice positioning; no hype/woo/corporate filler |

**Threshold:** 60/100 to advance. Below = auto-shelve.

**Brand gate:**
- Assign Brand Angle: B2C, B2B, or Both.
- Score brand_alignment out of 15.
- If brand_alignment < 8/15, shelve even if engagement is high.
- If headline or GenX-written summary uses blacklisted language from config/brand-voice.yaml, rewrite it before reporting or shelve if it cannot be made on-brand.
- Do not guess open founder decisions; flag them.

**Audience resonance check:**
- B2C: Does this speak to the successful-on-paper person who has lost spark, not beginners seeking generic motivation?
- B2B: Does this speak to burnt-out SME operators who need implementation and results, not abstract thought leadership?
- If neither audience has a clear reason to care, shelve even if the trend is viral.

**Mission-spine check:**
- Ask: does this trend connect to finding the unknown factor, removing what is blocking performance, or making a person/business work again?
- If the connection requires hype, jargon, or forced metaphors, shelve or mark as weak fit.

### Step 5: Rank and Select
- Sort stories by score (highest first)
- Select top 5 stories
- If fewer than 5 pass threshold, report what you have

### Step 6: Generate Trend Report

Use template: templates/trend-report.md

For each story include:
- Headline
- Score (X/100)
- Sources (with URLs)
- Publication dates
- Why it's trending
- Visual potential assessment
- Brand Angle: B2C, B2B, or Both
- Brand alignment score and reasoning
- Audience resonance: B2C/B2B reason to care
- Mission-spine fit: strong/medium/weak with one-line reason
- Blacklist flags: none or list violations
- Recommended next step

### Step 7: Save to Memory
- Append today's trends to memory/trend-history.md
- Format: date, headline, score, sources
- Used for dedup in future runs

## Output
- Trend report with 5 scored stories
- Each story has URLs, dates, scores, and reasoning
- Stories below 60/100 are listed as "shelved" with reason

## Error Handling
- If a source is unreachable, skip it and note in report
- If no stories pass threshold, report "No trending stories found today"
- If fewer than 5 pass, report what you have with explanation

## Quality Checks
- [ ] Sources are public or approved
- [ ] All stories have at least 1 URL
- [ ] All stories have publication date
- [ ] No story older than 72 hours
- [ ] No fabricated sources
- [ ] Scores calculated correctly
- [ ] Brand Angle included for every story
- [ ] Brand alignment score is at least 8/15 for advancing stories
- [ ] Audience resonance check completed for B2C, B2B, or Both
- [ ] Mission-spine fit is explicit and not forced
- [ ] Blacklist scan completed against config/brand-voice.yaml
- [ ] No API keys, cookies, or private account data in report
