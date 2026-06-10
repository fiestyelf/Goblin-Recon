# Goblin Recon Commands

Use these phrases inside the Goblin Recon Hermes profile. Keep prompts simple and direct.

## Daily Scans

| Say this | Use it when | What you get |
|---|---|---|
| `run fast scan` | You want a quick daily check. | Reliable-source trend leads from YouTube, Reddit, tech news, Product Hunt, and public X when available. |
| `run deep social scan` | You want a deeper weekly social scan. | Instagram/TikTok-first trend read with fallback to X, Reddit, and tech news if blocked. |
| `run full scan` | You want ideas and clips in one pass. | Social Pulse first, then Clip Mine for the strongest candidates only. |

## Social Pulse

Use these when you need ideas, blog angles, carousels, hooks, or content strategy.

| Say this | Use it when | What you get |
|---|---|---|
| `run social pulse` | You want current AI content opportunities. | Ranked trend ideas with categories, hooks, formats, evidence, score, and next action. |
| `what's trending on Instagram` | You care about IG formats and creator hooks. | IG-only creator scan with format analysis and blocked-source notes if access fails. |
| `what's trending on TikTok` | You care about TikTok sounds, formats, and viral acceleration. | TikTok-only trend scan with format and sound notes when public access allows. |
| `blog ideas` | You need long-form topics. | Social Pulse filtered into article angles and source-backed outlines. |
| `carousel ideas` | You need swipe-post concepts. | Carousel-worthy topics, slide structure, hook, and fallback angle. |
| `content strategy this week` | You want a simple posting plan. | Weekly content plan with priorities, effort, confidence, and distribution risk. |
| `what formats are working?` | You want format inspiration before creating. | Current reel/carousel formats, hooks, and creators driving the pattern. |

## Clip Mine

Use these when you need source videos and editor-ready clips.

| Say this | Use it when | What you get |
|---|---|---|
| `run clip mine` | You want clip candidates from current AI trends. | Timestamped 15-60s clip briefs with source links, transcript quote, brand gate, and editor notes. |
| `find clips about [topic]` | You already know the topic. | Source Hunter plus Moment Finder for that topic. Example: `find clips about AI agents replacing SDRs`. |
| `find the moment in [URL]` | You already have a video. | Best 15-60s segment from that source, if transcript/source access allows it. |

## Clip Vault

Use these when you need stored clips, duplicates, or status updates.

| Say this | Use it when | What you get |
|---|---|---|
| `what clips are ready` | Editors need approved clips. | Approved clips waiting for handoff. |
| `search clips about [topic]` | You want to check prior work. | Stored clips matching the topic, source, summary, or caption. |
| `show clip [clip_id]` | You need one stored record. | Full clip record and regenerated brief if possible. |
| `update clip status` | A clip moved in production. | Status change to `approved`, `in_production`, `scheduled`, `posted`, or `shelved`. |

## Manual Assisted Input

Use these when public extraction is blocked or you have screenshots/captions from a human.

| Say this | Use it when | What you get |
|---|---|---|
| `manual scan this [URL/screenshot/caption]` | You provide the source material manually. | Normalized social signal, score, category, recommendation, and next action. |
| `run brand check on [content]` | You want to check copy before posting. | Pass/shelve/modify recommendation with blacklist and nuance-word flags. |

## Competitors

| Say this | Use it when | What you get |
|---|---|---|
| `run competitor scan` | You want competitor intelligence. | Competitor report with claims, source URLs, risks, and brand gap analysis. |

## Special Prompt Rules

| Prompt pattern | When to use it | Important instruction |
|---|---|---|
| `manual scan this ...` | For screenshots, pasted captions, or blocked social pages. | Include the URL, creator, date, visible metrics, caption, and your notes when possible. |
| `find the moment in [URL]` | For one specific YouTube/video source. | The result must be 15-60 seconds and should not cut mid-sentence. |
| `run brand check on ...` | For captions, hooks, summaries, or outbound copy. | The copy should be English-only and avoid blacklisted phrases. |
| `update clip status ...` | For Clip Vault changes. | Include clip ID and target status. Example: `update clip status CLIP-20260610-001 to approved`. |
| `what did we do so far?` | For progress status. | The agent should give the latest changes first and avoid repeating the full old summary unless needed. |

## Local Utility Commands

Run these from the project folder when needed.

| Terminal command | Use it for |
|---|---|
| `.venv/bin/python -m pytest` | Run the test suite. |
| `python3 scripts/check_secrets.py` | Check for accidental API keys before sharing or committing. |
| `.venv/bin/python scripts/social_intake.py --input vault/intake/social-signal.json --store` | Normalize and store a manual social signal. |
| `.venv/bin/python scripts/query_clips.py list --status approved` | List approved clips from the local vault. |
| `.venv/bin/python scripts/query_clips.py brief [clip_id]` | Regenerate a clip brief from stored metadata. |

## Response Quality Rule

Goblin Recon should not repeat the same answer again and again. On follow-ups, it should say what changed, what is still true, and what to do next.
