# Goblin Recon — Session Issues & Solutions
## June 10, 2026

---

## 1. Missing Tools

### 1.1 `web_search` Does Not Exist

**Problem:** No search engine API configured. Every search required either browser navigation (slow, cookie walls) or `curl` commands (manual, fragile). What should take 10 seconds took 30-60 seconds per attempt.

**Symptom:** `Tool 'web_search' does not exist` error. Agent forced to use browser for everything.

**Fix:** Add a Brave Search API or Google Custom Search API key to Hermes config. One key gives agent instant search. Steps:
1. Get a free Brave Search API key from https://brave.com/search/api/
2. Configure in Hermes: `hermes config set tools.web_search.api_key <key> -p goblin-recon`
3. Or add to Hermes config.yaml under the goblin-recon profile

**File:** Hermes config.yaml (profile: goblin-recon)

---

### 1.2 `extract_clip` Module Missing

**Problem:** Referenced in skill documentation but never built. Agent tried `python -m goblin_recon.tools.extract_clip` and got `No module named goblin_recon.tools.extract_clip`.

**Impact:** Clip URLs cannot be auto-generated. Agent manually computes YouTube timestamp URLs (`?t=Xs`).

**Fix:** Build `goblin_recon/tools/extract_clip.py`. Minimum viable:
```python
def extract_clip_url(source_url: str, start_sec: int, end_sec: int) -> str:
    video_id = extract_youtube_id(source_url)
    return f"https://www.youtube.com/watch?v={video_id}&t={start_sec}"
```

**File to create:** `goblin_recon/tools/extract_clip.py`

---

### 1.3 `score_engagement` Module Missing

**Problem:** Referenced in skill but never built. Agent attempted `python -m goblin_recon.tools.score_engagement` — `No module named`.

**Impact:** Clip briefs lack engagement analytics (velocity score, platform percentile). Agent calculates manually from available data.

**Fix:** Build `goblin_recon/tools/score_engagement.py`. Minimum viable:
```python
def score_engagement(platform: str, video_id: str, publish_time: str, views: int) -> dict:
    hours_online = (datetime.now() - parse(publish_time)).total_seconds() / 3600
    velocity = views / hours_online if hours_online > 0 else views
    return {"velocity_score": min(int(velocity / 1000), 20), "velocity_per_hour": round(velocity)}
```

**File to create:** `goblin_recon/tools/score_engagement.py`

---

### 1.4 `get_clip_count` Function Does Not Exist

**Problem:** `clip_store.py` has `find_clips()` but not `get_clip_count()`. Script failed with `ImportError: cannot import name 'get_clip_count'`.

**Fix:** Add to `clip_store.py`:
```python
def get_clip_count(db_path=DEFAULT_DB_PATH) -> int:
    with connect(db_path) as conn:
        return conn.execute("SELECT COUNT(*) FROM clips").fetchone()[0]
```

**File:** `goblin_recon/tools/clip_store.py`

---

### 1.5 `save_clip` Signature Mismatch

**Problem:** Agent tried `save_clip(video_id=..., source_url=...)` with keyword args. Actual function takes a single `clip: dict` parameter.

**Fix:** Document the correct API in the skill. If you want keyword-arg interface, add a wrapper:
```python
def save_clip_kwargs(**kwargs):
    return save_clip(kwargs)
```

**File:** `goblin_recon/tools/clip_store.py` (add wrapper) or `skills/goblin-recon/SKILL.md` (document correct usage)

---

### 1.6 PYTHONPATH Required for Imports

**Problem:** Running `python scripts/query_clips.py` fails with `ModuleNotFoundError: No module named 'goblin_recon'`. Must prefix with `PYTHONPATH=.`.

**Fix:** Add `pip install -e .` or create a proper `setup.py`/`pyproject.toml`. Or add a shebang wrapper that sets PYTHONPATH. For now, all commands need:
```bash
PYTHONPATH=. .venv/bin/python scripts/query_clips.py list
```

**File:** `setup.py` or `pyproject.toml` (create)

---

## 2. Platform Access Issues

### 2.1 YouTube Cookie Walls

**Problem:** YouTube shows "Before you continue" consent dialog on ~50% of navigations. Blocks search results. Agent must click "Reject all" then re-navigate.

**Severity:** Medium. Intermittent. Adds 10-15 seconds per search.

**Fix (short-term):** Document in skill: "If YouTube shows cookie dialog, click Reject all first, then search."
**Fix (long-term):** YouTube Data API key. Free quota: 10,000 searches/day.

**File:** `skills/goblin-recon/SKILL.md` — add to troubleshooting section.

---

### 2.2 Reddit — JS Challenge on Every Request

**Problem:** Reddit returns JS challenge page. Zero content accessible. JSON API also blocked: returns empty responses with `JSONDecodeError`.

**Severity:** High. Reddit is completely inaccessible without API.

**Fix:** Reddit API requires OAuth app registration. Not available without API keys. Accept this as a limitation and prioritize HN + tech news.

**File:** `AGENTS.md` — document as known platform limitation.

---

### 2.3 Instagram — Login Wall

**Problem:** Even public profiles (@therundownai) show zero content. One-click generic element, nothing else.

**Severity:** High. Instagram is completely inaccessible.

**Fix:** Instagram Graph API requires Facebook Developer account + app review. Not practical without keys. Accept as limitation. Recommend manual assisted scan: user browses Instagram on phone and sends screenshots/URLs.

**File:** `AGENTS.md` — document as known platform limitation. Add manual assisted workflow.

---

### 2.4 TikTok — Tag Metadata Only

**Problem:** Tag pages show video count (58.4K for #ainews) but individual videos require login. Can't extract content or format signals.

**Severity:** Medium. Some signal available (tag volume), but no content.

**Fix:** Same as Instagram — manual assisted scan. Or TikTok Research API (requires approval).

**File:** `AGENTS.md` — document limitation.

---

### 2.5 Browser Daemon Crashes

**Problem:** Browser crashed mid-session: `Daemon process exited during startup with no error output`. Required restart. Happens under heavy multi-tab load.

**Severity:** Low. Rare but disruptive when it happens.

**Fix:** Don't open 3+ browser tabs simultaneously. Use terminal + curl for HN. Reserve browser for YouTube only.

**File:** `skills/goblin-recon/SKILL.md` — add to troubleshooting.

---

## 3. Agent Behavior Issues

### 3.1 `delegate_task` Burns Tokens (1.5M+ Per Session)

**Problem:** Sub-agents lack goblin-recon skill, brand rules, and config. They brute-force browser navigation instead of using lightweight APIs. One session burned 1.5M tokens across 247 seconds with only 1 of 3 tasks completed.

**Root cause:** `delegate_task` spawns fresh agents with no project context. They don't know about `youtube_tool`, `clip_store`, or brand gate. They default to browser everything.

**Fix:** Add hard rule to SKILL.md:
```markdown
### Delegate Task Policy (HARD RULE)

NEVER use delegate_task for:
- Fast Scan, Deep Scan, or Signal Scan
- Single-source lookups (one URL, one platform)
- Brand gate checks
- Transcript extraction

ONLY use delegate_task for:
- Post-processing after data is collected (scoring, cross-referencing)
- Formatting reports where the data is already in hand
```

**File:** `skills/goblin-recon/SKILL.md` and `AGENTS.md`

---

### 3.2 No "3 Dead Ends" Rule — Agent Searches Too Long

**Problem:** When searching for "Gemini 2.5 controversy," agent ran 10+ searches across 5 platforms without finding the story. Should have stopped after 2-3 failures and asked the user for more context.

**Symptom:** Wasted time, user frustration. Story didn't exist under that name.

**Fix:** Add to AGENTS.md:
```markdown
### Search Stop Rule

If a named topic returns zero relevant results after 3 different search queries across 2+ platforms:
- STOP searching
- Tell the user: "I can't find a story matching [name]. Can you provide a URL or more context?"
- Do NOT continue searching with different keywords
```

**File:** `AGENTS.md`

---

### 3.3 Fabricated Video URLs

**Problem (FIXED):** Agent was constructing YouTube URLs from video titles (`XB9m5sX6dN0` — fabricated) instead of extracting real `href` values from the page.

**Fix applied:** Now uses `browser_console` with `document.querySelector('a[title*="..."]')?.href`. Returns real URLs every time.

**No file change needed** — this is fixed in agent behavior. Document in skill as the correct approach.

**File:** `skills/goblin-recon/SKILL.md` — document the console extraction pattern.

---

### 3.4 Reports Vanish After Scrolling

**Problem:** Every deep scan, fast scan, and clip brief lives only in the chat transcript. When conversation scrolls, reports feel "lost."

**Fix:** Auto-save rule. Add to SKILL.md:
```markdown
### Auto-Save Rule (HARD)

After EVERY Social Pulse report, Deep Scan, Fast Scan, or Clip Brief:
- Write the full output to `vault/reports/YYYY-MM-DD-{type}.md`
- Tell the user: "Saved → vault/reports/<filename>"
- Never require the user to ask for a save

Naming:
- vault/reports/2026-06-10-deep-scan.md
- vault/reports/2026-06-10-clip-brief-<clip_id>.md
- vault/reports/2026-06-10-fast-scan.md
```

**File:** `skills/goblin-recon/SKILL.md` and `AGENTS.md`

---

### 3.5 Clip Briefs Missing Background Section

**Problem:** Clip briefs jumped straight to the quote. User: "I feel like I'm totally clueless and don't understand what I'm checking for."

**Fix:** Every clip brief must lead with:
```markdown
## Background
[2-3 sentences. What this video is about. Who's speaking. Why it matters.]

## The Clip Moment
[Timestamp, quote, scoring]
```

**File:** `skills/goblin-recon/SKILL.md` — update clip brief template.

---

## 4. User Experience Solutions

### 4.1 How Users Should Request Clips (4-Tier Guide)

**Problem:** "Find source material about the Gemini 2.5 controversy" failed because the topic name was vague and the story didn't exist under that name.

**Solution:** Tiered request format:

| Tier | Format | Speed | Example |
|------|--------|-------|---------|
| 1 | "Clip from [URL]" | Instant | "Find the best clip from this article: [URL]" |
| 2 | "[Event] from [creator/platform]" | Fast | "Find the best clip about Apple/Gemini from MKBHD's WWDC review" |
| 3 | "[Description] — I think it was [context]" | Medium | "Find me a clip about AI agents buying things without permission. I think it was Google I/O" |
| 4 | "[Vague topic name]" | Slow — may fail | "Find clips about Gemini 2.5 controversy" |

Add as user-facing documentation.

**File:** `COMMANDS.md` or `README.md` (create)

---

### 4.2 Caption Tone Architecture

**Problem:** Captions had one tone (brand voice only). No flexibility for different platforms and story types.

**Solution:** 5-tone system × 2 brand doors:

| Tone | Voice | Best For |
|------|-------|----------|
| **Direct** | No adjectives. Facts first. | B2B LinkedIn, newsjacking |
| **Wry** | Sardonic, knowing. | Controversial takes |
| **Warm** | Human, emotionally true. | B2C Instagram |
| **Curious** | Asks questions. | Analytical, deep dives |
| **Bold** | Provocative. Picks a side. | Controversy, predictions |

Default tone by category:
- Latest AI News → Direct
- Controversial → Bold
- Upgrade/Democratization → Curious
- Analytical/Deep-dive → Curious

Add to config.

**File:** `config/brand-voice.yaml` — add `caption_tones` section

---

### 4.3 How Users See Their Clips

**Problem:** User asked "How can I see the clips by myself? I'm clueless."

**Solution:** Three methods documented:

1. **Ask the agent:** `show clip <id>`, `search clips about <topic>`, `what clips are ready`
2. **Terminal command:** `PYTHONPATH=. .venv/bin/python scripts/query_clips.py list`
3. **Open the database:** `vault/clips.db` in any SQLite viewer (DB Browser for SQLite is free)

Add as user-facing documentation.

**File:** `README.md` or `COMMANDS.md`

---

### 4.4 Signal Scan — First-Mover Content Discovery

**Problem:** Current scans hit mainstream sources (TechCrunch, Verge) — by the time a story appears there, 96K people have already watched the creator video. First-mover advantage is lost.

**Solution:** New "Signal Scan" mode with inverted priority:
```
Current: News sites → Reddit → X → score
Signal:  X → Hacker News → GitHub trending → Reddit (velocity filter) → score
```

Sources to add:
- Hacker News (`news.ycombinator.com`) — public, no login
- GitHub Trending (`github.com/trending`) — filter for Python/JavaScript AI repos
- ArXiv (`arxiv.org/list/cs.AI/recent`) — papers today → products in 2-3 months

Time gate: scan last 6 hours only. If nothing passes velocity threshold, return "nothing worth posting right now."

**Files to edit:**
- `config/sources.yaml` — add HN, GitHub trending, ArXiv
- `skills/goblin-recon/SKILL.md` — add Signal Scan workflow
- `AGENTS.md` — add Signal Scan rules

---

## 5. Why YouTube Works Now (Answer to User Question)

**Q: "Earlier, before all the changes I made, why were you not able to check YouTube, and what is changed now?"**

**A:** Three things:

1. **You added `youtube-transcript-api`** to the venv. Without it, transcript extraction failed silently. The `youtube_tool` worked from the start — it just needed the dependency.

2. **Agent was fabricating URLs.** Was constructing `https://www.youtube.com/watch?v=XB9m5sX6dN0` from video titles instead of extracting real `href` values from the page using `browser_console`. Fixed by using `document.querySelector('a[title*="..."]')?.href`.

3. **Agent wasn't handling cookie walls.** YouTube showed "Before you continue" dialog. Agent didn't click "Reject all" to dismiss it. Fixed by clicking the consent button first.

The `youtube_tool` transcript extractor always worked. The bottleneck was getting video URLs into it fast enough. Now: one console call → URL → transcript → clip brief. ~45 seconds per clip.

---

## Summary of Files to Edit

| Priority | File | Changes |
|----------|------|---------|
| 🔴 | `skills/goblin-recon/SKILL.md` | Delegate task ban, auto-save rule, Background section, Signal Scan, 3-dead-ends rule, YouTube cookie handling, console extraction pattern, correct clip_store API docs |
| 🔴 | `AGENTS.md` | Delegate Task Policy, auto-save rule, Signal Scan rules, search stop rule, platform limitation docs |
| 🔴 | `config/brand-voice.yaml` | Caption tones (5) + default mapping by category |
| 🟡 | `goblin_recon/tools/extract_clip.py` | Create: clip URL generation |
| 🟡 | `goblin_recon/tools/score_engagement.py` | Create: engagement velocity scoring |
| 🟡 | `goblin_recon/tools/clip_store.py` | Add `get_clip_count()`, add keyword-arg wrapper |
| 🟡 | `config/sources.yaml` | Add HN, GitHub trending, ArXiv sources |
| 🟢 | `setup.py` or `pyproject.toml` | Create: pip install -e support |
| 🟢 | `README.md` or `COMMANDS.md` | Create: user-facing documentation (clip request formats, viewing clips, caption tones) |
| 🟢 | Hermes config.yaml | Add web_search API key (Brave or Google) |

---

## Not Fixed Yet (Needs External Action)

| Issue | What's Needed |
|-------|---------------|
| No search API | Brave Search API key or Google Custom Search key |
| Instagram blocked | Facebook Developer account + app review |
| Reddit blocked | Reddit OAuth app registration |
| TikTok content blocked | TikTok Research API approval |
| Browser crashes | Reduce concurrent browser tabs |
| YouTube intermittent cookie walls | YouTube Data API key as fallback |
