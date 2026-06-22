---
name: source-hunter
description: Find public source videos/pages for a trend and prepare candidates for Moment Finder.
category: genx-marketing
version: 1.1.0
---

# Source Hunter

Goal: find real source URLs for a trend. No URL, no recommendation.

## Inputs

- trend/topic/headline
- category
- desired audience angle
- source priority, if any

## Source Priority

1. YouTube podcasts/interviews/keynotes
2. Public Instagram Reels
3. Public TikTok
4. Podcast platforms
5. Tech/news source for validation

Stop if a platform blocks access. Do not bypass login, captcha, paywall, robots.txt, or rate limits.

## Flow

```text
trend -> queries -> source URLs -> metadata/transcript status -> score -> pass selected sources to moment-finder
```

## Score

0-100:
- source relevance: 25
- speaker/source credibility: 20
- transcript or caption access: 20
- clip potential: 20
- recency/engagement: 15

Advance threshold: 65.

## Output

For each source:
- title
- speaker/channel
- URL
- publication date
- access status
- transcript/caption status
- engagement metrics if public
- why this source matters
- score
- pass/shelve decision

Pass only the best 1-3 viable sources to Moment Finder.
