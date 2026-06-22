# Goblin Recon — Simple Setup Guide

**For: GenX Academy Marketing Team**

---

## What is Goblin Recon?

Goblin Recon is your AI research assistant. It finds trending AI stories, locates the best YouTube and Instagram videos about them, and extracts short clips (15-60 seconds) that you can post.

**Think of it as:** A research intern that never sleeps, finds the hottest AI topics, and hands you ready-to-post content ideas.

**Tagline:** "You trigger. It hunts."

---

## What You Get

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

**You don't need to:**
- Browse Reddit or Twitter for hours
- Watch full 2-hour podcasts
- Guess what's trending
- Write captions from scratch

---

## Before You Start (Prerequisites)

You need these on your computer:

### 1. Python 3.12 or newer
**Check if you have it:**
```bash
python3 --version
```

**If you see something like `Python 3.12.x`** → You have it! ✅

**If you see "command not found" or an older version** → 
- **Mac:** Run `brew install python@3.12`
- **Windows:** Download from [python.org](https://python.org)
- **Linux:** Run `sudo apt-get install python3.12`

### 2. uv (Python Package Manager)
**Check if you have it:**
```bash
uv --version
```

**If you see a version number** → You have it! ✅

**If not, install it:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then restart your terminal.

### 3. Hermes (AI Agent Platform)
**Check if you have it:**
```bash
hermes --version
```

**If you see a version number** → You have it! ✅

**If not:** Ask your IT team or the person who gave you this guide to help install Hermes.

---

## Step-by-Step Setup (5 Minutes)

### Step 1: Get the Files

Copy the `goblin-recon` folder to your computer. You should have received it as a zip file or folder.

**Open your terminal and navigate to the folder:**
```bash
cd goblin-recon
```

*(Tip: Type `cd ` and then drag the goblin-recon folder into your terminal)*

### Step 2: Run Setup

Run this command inside the goblin-recon folder:
```bash
bash scripts/setup.sh
```

This installs the Goblin Recon Hermes profile, SOUL.md, bundled skills, profile defaults, Python virtual environment, and approved Python packages.

If setup warns that no model provider is detected, continue the setup and ask your team lead which approved provider to configure.

### Step 2.5: Security Check Before Sharing

Run this command before sharing the folder, pushing to GitHub, or sending files to anyone:

```bash
python3 scripts/check_secrets.py
```

If it says `No obvious secrets found`, you are clear.

If it reports a possible secret, stop and ask an admin before sharing anything.

### Step 3: Configure Your AI Provider If Needed

Use whichever provider/model your company has approved. Example for OpenAI:
```bash
hermes -p goblin-recon config set model.provider openai
hermes -p goblin-recon config set model.default gpt-4o
```

If your provider needs an API key, set it through Hermes secrets or your approved local secret method. Never paste keys into chat or commit them to this folder.

### Step 4: Launch Goblin Recon

Run this command:
```bash
hermes -p goblin-recon
```

You should see something like:
```
[Goblin Recon] Ready. What would you like me to hunt?
```

**You're ready!** 🎉

---

## Using Hermes Desktop With Goblin Recon

Hermes Agent v0.16.0 adds a native Desktop app. Use the CLI when you want speed, but use Hermes Desktop for day-to-day team operations because it gives you a visual workspace for profiles, memory, skills, schedules, tools, and gateways.

### Recommended Desktop Setup

1. Open Hermes Desktop.
2. Choose local mode if Hermes is installed on this machine, or remote mode if your team runs Hermes on a server.
3. Select the `goblin-recon` profile.
4. Open the project folder: `goblin-recon/`.
5. Verify the active profile can read `AGENTS.md`, `memory/brand-rules.md`, and `config/brand-voice.yaml`.

### Desktop Screens To Use

| Desktop screen | Use it for |
|---|---|
| Chat | Run `run full scan`, approve/shelve/modify briefs, ask follow-up questions |
| Sessions | Search old scans, recover prior decisions, compare recurring trends |
| Skills | Confirm `trend-radar`, `source-hunter`, `moment-finder`, `competitor-scout`, and `orchestrator` are available |
| Memory | Review or edit `brand-rules.md`, `trend-history.md`, `competitor-snapshots.md`, and `content-performance.md` |
| Tools | Enable only approved toolsets: web, browser, file, terminal, memory, session_search, skills |
| Schedules | Create daily trend scans and weekly competitor scans without writing cron commands |
| Gateway | Connect approved Discord, Slack, Email, or other delivery targets |
| Soul | Review the active profile persona; project behavior still comes from `AGENTS.md` |
| Models | Pick the approved model and switch only with team approval |

### Recommended Desktop Schedules

Create these from the Schedules screen after the manual flow works:

| Schedule | Prompt | Delivery |
|---|---|---|
| Daily 8:00 | `find trending AI stories and apply the GenX brand gate` | Chat or approved Discord channel |
| Monday 9:00 | `run competitor scan and include brand gap analysis` | Chat or approved Discord channel |
| Friday 15:00 | `summarize this week's approved, shelved, and brand-gate rejected content` | Chat |

### Desktop Brand Workflow

1. Run a scan from Chat.
2. Let the agent apply the brand gate before human approval.
3. Review only briefs with Brand Alignment >= 8/15 and no unresolved blacklist flags.
4. Use `approve`, `shelve`, or `modify [instructions]`.
5. Record live content results in `memory/content-performance.md` so future scoring improves.

### Important Desktop Safety Rule

Do not paste API keys into Desktop chat. Use Hermes profile secrets, the Desktop provider settings, or the local `.env` method approved by your admin.

---

## Security Rules for Business Use

These rules protect company accounts, API keys, and unpublished content.

### Never Do These

- Do not paste API keys into Hermes, Slack, Discord, GitHub, or content briefs.
- Do not commit `.env`, cookies, tokens, session files, or screenshots showing secrets.
- Do not scrape private accounts, private groups, paid content, or login-only pages.
- Do not bypass paywalls, captchas, rate limits, or platform access blocks.
- Do not use your personal social media account for automated company research.
- Do not publish a clip or competitor claim without human approval.

### Safe Defaults

- Use public sources only.
- Use company-approved accounts only.
- Keep API keys in Hermes profile secrets or local environment variables.
- Store short excerpts, timestamps, and links instead of full raw transcripts.
- When unsure, shelve the item and ask for review.

### Files to Read Before Using APIs

- `SECURITY.md` explains the overall security policy.
- `API_KEYS.md` explains how to handle keys safely.
- `SOCIAL_API_SETUP.md` explains how to add approved social API keys.
- `HERMES_APPROVALS.md` explains what to approve or deny when Hermes asks for permissions.
- `LEGAL_GUARDRAILS.md` explains platform and copyright rules.
- `PRE_LAUNCH_CHECKLIST.md` is the final checklist before company rollout.
- `config/security.yaml` contains the agent's default security settings.

### Simple API Key Setup

If an admin gives you an approved API key, use this safe method:

```bash
cp .env.example .env
```

Then open `.env` and paste the key only there.

Before sharing the folder or pushing to GitHub, run:

```bash
python3 scripts/check_secrets.py
```

Do not paste API keys into Hermes chat, Slack, Discord, GitHub, screenshots, or Markdown files.

---

## How to Use Goblin Recon

Once you're inside Hermes (you see the prompt), you can say these commands:

### What to Trigger When

Use this table when you are not sure which command to run.

| Say this | It does |
|---|---|
| `run fast scan` | Quick daily trend check |
| `run deep social scan` | Deeper Instagram and TikTok trend check |
| `run signal scan` | Early AI signals before they are mainstream |
| `manual scan this [URL/screenshot/caption]` | Score something you paste in |
| `run social pulse` | Find content ideas, blog angles, and hooks |
| `what's trending on Instagram` | Instagram trends and creator hooks |
| `what's trending on TikTok` | TikTok trends, sounds, and formats |
| `blog ideas` | Article ideas from current trends |
| `carousel ideas` | Swipe-post ideas from current trends |
| `content strategy this week` | Simple weekly posting plan |
| `run clip mine` | Find short video clip ideas |
| `find clips about [topic]` | Find clips about one topic |
| `find the moment in [URL]` | Pick the best short clip from one video |
| `what clips are ready` | Approved clips ready for editors |
| `run full scan` | Find trends, then clips for the best ones |
| `run full autonomous scan` | Run the whole approved workflow without asking at each step |
| `run competitor scan` | Check competitors and suggest next moves |
| `run brand check on [content]` | Check copy against brand rules before posting |
| `write email hooks for [offer/audience]` | Write and score email subject lines and openers |

Simple rule:

- If you do not know where to start, type `run full scan`.
- If you already have a topic, type `find clips about [topic]` or `find sources for [topic]`.
- If you already have a video, type `find the moment in [video URL]`.
- If you want the full workflow, type `run full autonomous scan`.
- If you are planning a campaign or checking competitors, type `run competitor scan`.

Examples:

```text
run fast scan
run full scan
run full autonomous scan
find clips about AI agents replacing SDRs
find the moment in https://youtube.com/watch?v=VIDEO_ID
run competitor scan
```

### Campaign Research vs Content Research

Use Goblin Recon differently depending on your goal.

For content research:

- Use `run full scan` when you need fresh content ideas for the week.
- Use `find trending AI stories` when you only want to see what is hot today.
- Use `find sources for [topic]` when you already have a content theme.
- Use `find the moment in [video URL]` when someone gives you a long video or podcast.

For campaign research:

- Use `run competitor scan` when planning campaigns, checking offers, pricing, positioning, or messaging.
- Use `find trending AI stories around [campaign theme]` to validate whether a campaign idea is timely.
- Use `find sources for [campaign topic]` to collect proof points, examples, and public discussion around the campaign.

### Command 1: Find Trending Stories
```
find trending AI stories
```

**What happens:**
- Goblin Recon scans Twitter/X, Reddit, TechCrunch, Product Hunt, and Hacker News
- It finds the top 5 trending AI stories
- Each story gets a score (0-100)
- Stories below 60/100 are automatically filtered out

**What you see:**
```
TREND REPORT — June 4, 2026

1. "OpenAI Announces GPT-5" — Score: 92/100
   Sources: TechCrunch, Twitter, Reddit
   Why trending: Major announcement with 50K+ mentions

2. "AI Replaces 10,000 Jobs at Tech Giant" — Score: 85/100
   Sources: The Verge, Twitter
   Why trending: Controversial, lots of debate
```

### Command 2: Find Sources for a Story
```
find sources for OpenAI GPT-5
```

**What happens:**
- Searches YouTube and Instagram for videos about this topic
- Finds 3-5 best videos
- Pulls transcripts from YouTube videos

**What you see:**
```
SOURCES FOUND: "OpenAI GPT-5"

1. YouTube: "GPT-5 Explained in 10 Minutes" — Score: 78/100
   Channel: AI Explained | Views: 500K
   URL: youtube.com/watch?v=abc123
   Transcript: Available ✅

2. Instagram Reel: "GPT-5 is INSANE" — Score: 65/100
   Account: @ai_news | Likes: 25K
   URL: instagram.com/p/xyz789
```

### Command 3: Find the Best Clip Moment
```
find the moment in youtube.com/watch?v=abc123
```

**What happens:**
- Reads the transcript
- Finds the most quotable, emotional, or controversial moment
- Gives you exact timestamps

**What you see:**
```
CLIP BRIEF: "GPT-5 Will Change Everything"

URL: youtube.com/watch?v=abc123&t=1842 → t=1902
Duration: 60 seconds

THE MOMENT:
"By 2027, 90% of white-collar work will be automated. 
This isn't science fiction. It's already happening."

WHY POST: Bold prediction from credible source. 
Triggers fear + curiosity = high engagement.

CAPTION: "90% of jobs GONE by 2027? The truth nobody's talking about..."

Reply: approve / shelve / modify
```

### Command 4: Run Everything at Once
```
run full scan
```

**What happens:**
- Runs all 3 steps automatically
- Finds trends → Finds sources → Finds clips
- Presents everything for your approval

**Best for:** When you want the full pipeline without typing multiple commands.

### Command 5: Check Competitors
```
run competitor scan
```

**What happens:**
- Checks competitor websites, pricing, and social media
- Tells you what changed since last scan
- Suggests what GenX Academy should do in response

**Note:** You need to add competitors to `config/competitors.yaml` first.

---

## What You Do Next

When Goblin Recon shows you a clip brief, you have 3 options:

### Option 1: Approve ✅
Type: `approve`

**What happens:** The brief is saved to `vault/briefs/` for your content team to create the actual post.

**Use when:** The clip looks good and you want to post it.

### Option 2: Shelve 🗄️
Type: `shelve`

**What happens:** The brief is skipped and recorded so Goblin Recon doesn't suggest it again.

**Use when:** The clip isn't interesting or you don't want to post about this topic.

### Option 3: Modify ✏️
Type: `make the caption shorter and more urgent`

**What happens:** Goblin Recon revises the brief based on your instructions and shows it again.

**Use when:** You like the clip but want to change the caption, format, or focus.

---

## Weekly Workflow (Suggested)

### Monday Morning (15 minutes)
```
hermes -p goblin-recon
"run full scan"
```
- Review top 5 trending stories
- Approve 2-3 clip briefs for the week

### Wednesday (5 minutes)
```
"run competitor scan"
```
- Check what competitors are doing
- Note any pricing or feature changes

### Friday (5 minutes)
```
"what did we find this week?"
```
- Review approved briefs
- Plan content for next week

---

## Understanding the Scores

Every story and clip gets a score (0-100). Here's what they mean:

| Score | Meaning | Action |
|-------|---------|--------|
| 90-100 | 🔥 Viral potential | Definitely post this |
| 75-89 | ⚡ Strong trend | Good content opportunity |
| 60-74 | 📈 Worth considering | Evaluate if it fits your brand |
| Below 60 | 🗄️ Auto-shelved | Not trending enough |

**Why scores matter:** They save you time. You don't need to guess if a story is worth posting.

---

## Common Issues & Fixes

### Issue 1: "No module named 'youtube_transcript_api'"
**Fix:** Run this inside the goblin-recon folder:
```bash
bash scripts/setup.sh
```

### Issue 2: "Profile not found"
**Fix:** Run setup again. If setup warns that the Hermes profile command failed, create the profile manually and rerun setup:
```bash
hermes profile create goblin-recon
bash scripts/setup.sh
```

### Issue 3: "No trending stories found"
**Possible reasons:**
- It's a slow news day (rare in AI)
- Your internet connection is down
- Rate limits from Reddit/Twitter (wait 5 minutes and try again)

**Fix:** Try running at a different time (mornings usually have the most news).

### Issue 4: "Video transcript not available"
**Why:** Some YouTube videos don't have captions/subtitles.

**Fix:** Goblin Recon will skip these and try the next video. You don't need to do anything.

### Issue 5: Hermes doesn't start
**Fix:** Check if Hermes is installed:
```bash
which hermes
```

If nothing shows up, Hermes isn't installed. Ask your IT team for help.

---

## Quick Command Cheat Sheet

| You type | What it does |
|----------|--------------|
| `run fast scan` | Quick daily trend check |
| `run deep social scan` | Deeper Instagram and TikTok trend check |
| `run signal scan` | Find early AI signals |
| `manual scan this [URL/screenshot/caption]` | Score something you paste in |
| `find trending AI stories` | Find top AI trends |
| `find clips about [topic]` | Find clips about one topic |
| `find the moment in [URL]` | Pick the best short clip from one video |
| `run full scan` | Find trends, then clips |
| `run full autonomous scan` | Run the whole approved workflow |
| `run competitor scan` | Check competitors |
| `run brand check on [content]` | Check copy before posting |
| `write email hooks for [offer/audience]` | Write email hooks |
| `approve` | Save this clip brief |
| `shelve` | Skip this clip brief |
| `modify [instructions]` | Change and re-propose |
| `/exit` | Leave Goblin Recon |

---

## FAQ

### Q: Do I need to know coding?
**A:** No. You just type commands in plain English. The scripts run automatically.

### Q: Is this free?
**A:** The YouTube transcript tool is free. You may need to pay for AI model usage (like DeepSeek) depending on your Hermes setup. Ask your team lead.

### Q: Can I use this on Instagram and TikTok too?
**A:** Yes! Goblin Recon finds Instagram reels. The clip format suggested works for TikTok, Instagram Reels, and YouTube Shorts.

### Q: What if the AI suggests something inappropriate?
**A:** You always have final say. Use `shelve` to reject anything that doesn't fit your brand.

### Q: Can multiple people use this?
**A:** Yes. Each person creates their own Hermes profile, but everyone uses the same `goblin-recon` folder and configs.

### Q: How often should I run this?
**A:** Daily is best for catching trends early. At minimum, run it Monday, Wednesday, Friday.

### Q: Can I change what sources it scans?
**A:** Yes! Edit `config/sources.yaml` to add/remove Reddit subreddits, Twitter accounts, or news sites.

### Q: The clips are too long/short. Can I adjust?
**A:** Yes. Tell Goblin Recon: `make the clip 45 seconds` or `find a shorter moment`.

---

## Customizing Goblin Recon

### Add Your Favorite YouTube Channels
Edit `config/sources.yaml` and add channels under `sources:` → `content_sources:` → `youtube:` → `podcast_channels:`

Example:
```yaml
- name: "Your Favorite Channel"
  channel_id: "UC..."
  type: podcast
  focus: AI, tech
```

### Add Instagram Accounts to Monitor
Edit `config/sources.yaml` and add accounts under `sources:` → `content_sources:` → `instagram:` → `tech_accounts:`

Example:
```yaml
tech_accounts:
  - "your_favorite_account"
```

### Change Scoring Weights
Edit `config/scoring.yaml` to adjust how stories are scored.

Example: If you care more about controversy than recency:
```yaml
controversy:
  max: 25  (was 15)
recency:
  max: 10  (was 20)
```

### Add Competitors
Edit `config/competitors.yaml` and add companies you want to monitor:

```yaml
competitors:
  - name: "Competitor Name"
    website: "https://competitor.com"
    pricing_page: "https://competitor.com/pricing"
```

---

## Best Practices

1. **Trust the scores** — Stories below 60/100 usually aren't worth your time
2. **Approve quickly** — Don't overthink. If it's good, approve and move on
3. **Check the transcript** — Always verify the clip actually says what the brief claims
4. **Run daily** — AI moves fast. Catch trends early for maximum engagement
5. **Customize sources** — Add channels and accounts that match your brand voice

---

## Getting Help

If something doesn't work:

1. Check this guide's "Common Issues" section above
2. Read the `README.md` file for technical details
3. Ask in your team Slack channel: `#goblin-bureau`
4. Check the `AGENTS.md` file for advanced rules

---

## What Happens Next?

**After you approve a clip brief:**
1. The brief is saved to `vault/briefs/`
2. Your content team creates the faceless reel using the timestamps
3. They post it on Instagram/TikTok/YouTube Shorts
4. You track performance
5. Goblin Recon learns what works and improves over time

**The cycle repeats:** Trigger → Hunt → Approve → Post → Track

---

**Goblin Recon** — Part of the Goblin Bureau  
*"You trigger. It hunts."*

---

*Last updated: June 4, 2026*
