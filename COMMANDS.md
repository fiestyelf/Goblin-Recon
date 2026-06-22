# Goblin Recon Commands

Use these phrases inside the Goblin Recon Hermes profile. Keep prompts simple and direct.

## Daily Scans

| Say this | Use it when | What you get |
|---|---|---|
| `run fast scan` | You want a quick daily check. | A short list of trend ideas from trusted public sources. |
| `run deep social scan` | You want a deeper social check. | A closer look at Instagram and TikTok trends, with backup sources if access is blocked. |
| `run signal scan` | You want early ideas. | Early AI signals before they are everywhere. |
| `run full scan` | You want ideas and clips in one pass. | Finds trends, then finds clips for the strongest ideas. |
| `run full autonomous scan` | You want the full approved workflow. | Runs the whole workflow without asking at each step. |

## Social Pulse

Use these when you need ideas, blog angles, carousels, hooks, or content strategy.

| Say this | Use it when | What you get |
|---|---|---|
| `run social pulse` | You want content ideas. | Trend ideas with hooks, formats, sources, scores, and next steps. |
| `what's trending on Instagram` | You want Instagram ideas. | Instagram trends, creator hooks, and format notes. |
| `what's trending on TikTok` | You want TikTok ideas. | TikTok trends, sounds, and format notes when public access works. |
| `blog ideas` | You need article topics. | Long-form ideas and simple outlines. |
| `carousel ideas` | You need swipe-post ideas. | Carousel topics, slide ideas, and hooks. |
| `run carousel generator` | You have a reference/template and need files. | Builds editable Instagram or Facebook carousel layers in `vault/carousels/`. |
| `generate single post` | You need one social image. | Makes one editable social image for a topic. |
| `content strategy this week` | You want a weekly plan. | A simple posting plan with priorities. |
| `what formats are working?` | You want format inspiration. | Reel and carousel formats that are working now. |

### Carousel Generator

Use this when an idea is ready to become carousel assets.

| Say this | Use it when | What you get |
|---|---|---|
| `run carousel generator` | You have a topic and reference/template. | Brief, manifest, assets, exports, and generation log in `vault/carousels/`. |
| `make an Instagram carousel about [topic]` | You need Instagram slides. | Reference-first slide plan, then local rendered images after approval. |
| `make a Facebook carousel about [topic]` | You need Facebook page images. | Facebook-sized rendered assets after approval. |

Required process: provide a reference/template first, approve the slide plan before Replicate, then review final exports before use.

QA checks: mobile readability, no AI-garbled final text, correct dimensions, page fit, safe claims, clear CTA, visual consistency, export files, and human approval.

## Clip Mine

Use these when you need source videos and editor-ready clips.

| Say this | Use it when | What you get |
|---|---|---|
| `run clip mine` | You want short clip ideas. | 15-60 second clip options with links, quotes, and editor notes. |
| `find clips about [topic]` | You already know the topic. | Clip ideas for that one topic. Example: `find clips about AI agents replacing SDRs`. |
| `find the moment in [URL]` | You already have a video. | The best 15-60 second section from that video, if available. |

### Best Ways to Request Clips

| Tier | Say this | Speed | Example |
|---|---|---|---|
| 1 | `find the moment in [URL]` | Fastest | `find the moment in https://youtube.com/watch?v=...` |
| 2 | `[event] from [creator/platform]` | Fast | `Find the Apple/Gemini moment from MKBHD's WWDC review` |
| 3 | `[description] — I think it was [context]` | Medium | `Find the clip about AI agents buying things without permission. I think it was Google I/O.` |
| 4 | `[vague topic name]` | Slow, may fail | `Find clips about the Gemini 2.5 controversy` |

If Tier 4 returns no relevant results after 3 searches across 2+ platforms, the agent should stop and ask for a URL, screenshot, creator name, or more context.

## Clip Vault

Use these when you need stored clips, duplicates, or status updates.

| Say this | Use it when | What you get |
|---|---|---|
| `what clips are ready` | Editors need approved clips. | Approved clips ready for editors. |
| `search clips about [topic]` | You want to check old clips. | Stored clips that match the topic. |
| `show clip [clip_id]` | You need one saved clip. | The saved clip details. |
| `update clip status` | A clip moved forward. | Changes a clip to `approved`, `in_production`, `scheduled`, `posted`, or `shelved`. |

### How to See Clips Yourself

| Method | Command or action |
|---|---|
| Ask the agent | `show clip [clip_id]`, `search clips about [topic]`, or `what clips are ready` |
| Terminal list | `.venv/bin/python scripts/query_clips.py list` |
| Terminal brief | `.venv/bin/python scripts/query_clips.py brief [clip_id]` |
| SQLite viewer | Open `vault/clips.db` in DB Browser for SQLite or another SQLite viewer |

## Manual Assisted Input

Use these when public extraction is blocked or you have screenshots/captions from a human.

| Say this | Use it when | What you get |
|---|---|---|
| `manual scan this [URL/screenshot/caption]` | You paste in source material. | A cleaned-up, scored idea with a next step. |
| `run brand check on [content]` | You want to check copy before posting. | Tells you if the copy should pass, change, or be shelved. |

## Captions

Use `skills/caption-tone/SKILL.md` for caption and description writing.

| Say this | What you get |
|---|---|
| `write captions for this [brief/source]` | Writes captions from your brief or source. |
| `make this more casual` | Makes the caption sound more natural. |
| `make this edgier` | Makes the caption sharper. |
| `make this warmer` | Makes the caption more human. |

Default behavior: ask Output Direction first when missing, produce normal professional GenX copy, then ask if the user wants a different tone or voice for the use case.

## Email Hooks

Use `skills/email-hook/SKILL.md` for outbound subject lines, openers, and short drafts.

| Say this | What you get |
|---|---|
| `write email hooks for [offer/audience]` | Writes and scores five subject lines and openers. |
| `write subject lines for [campaign]` | Writes subject lines for one campaign. |
| `validate this email` | Checks if an email is ready or needs changes. |

Before generating, the agent should ask who it is for, where it goes, and what tone it should carry when that direction is missing.

## Competitors

| Say this | Use it when | What you get |
|---|---|---|
| `run competitor scan` | You want to check competitors. | Competitor changes, source links, risks, and suggested next moves. |

## Full Autonomous Mode

Say this when you want to give Goblin Recon full working permission for one scan without repeated yes/no prompts:

```text
run full autonomous scan
```

This lets Goblin Recon:

- read the project files it needs
- use approved public sources
- run local Python checks and tools
- create reports, briefs, and captions in `vault/`
- update local memory when needed
- run the safety check automatically

It does **not** grant permission to:

- reveal, print, or use secrets without explicit approval
- create external accounts or configure paid services
- bypass paywalls, captchas, login walls, robots.txt, or rate limits
- publish, post, email, DM, or contact anyone externally
- delete important source files or perform irreversible deployment actions

Required output at the end:

```text
What I scanned
What I created
What passed Security Rail
What needs human review
Where files were saved
Next recommended action
```

## Special Prompt Rules

| Prompt pattern | When to use it | Important instruction |
|---|---|---|
| `manual scan this ...` | For screenshots, pasted captions, or blocked social pages. | Add the URL, creator, date, numbers, caption, and notes if you have them. |
| `find the moment in [URL]` | For one YouTube or video source. | Finds a 15-60 second moment that does not cut off mid-sentence. |
| `run brand check on ...` | For captions, hooks, summaries, or emails. | Checks if the copy is safe to use or needs changes. |
| `write email hooks for ...` | For outbound emails. | Add the offer, audience, and campaign type if you know them. |
| `update clip status ...` | For saved clip updates. | Add clip ID and status. Example: `update clip status CLIP-20260610-001 to approved`. |
| `what did we do so far?` | For progress status. | Shows what changed recently and what to do next. |

## Local Utility Commands

Run these from the project folder when needed.

| Terminal command | Use it for |
|---|---|
| `.venv/bin/python -m pytest` | Run the test suite. |
| `.venv/bin/python -m pip install -e .` | Install the package in editable mode so imports work without setting `PYTHONPATH`. |
| `python3 scripts/check_secrets.py` | Check for accidental API keys before sharing or committing. |
| `.venv/bin/python -m goblin_recon.tools.social_intake --input vault/intake/social-signal.json --store` | Normalize and store a manual social signal. |
| `.venv/bin/python -m goblin_recon.tools.email_gate --subject "..." --body "..."` | Score an outbound email draft. |
| `.venv/bin/python scripts/query_clips.py list --status approved` | List approved clips from the local vault. |
| `.venv/bin/python scripts/query_clips.py brief [clip_id]` | Regenerate a clip brief from stored metadata. |

## Response Quality Rule

Goblin Recon should not repeat the same answer again and again. On follow-ups, it should say what changed, what is still true, and what to do next.
