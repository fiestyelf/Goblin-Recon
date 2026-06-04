# Goblin Recon — Simple Setup Guide

**For: GenX Academy Marketing Team**

---

## What is Goblin Recon?

Goblin Recon is your AI research assistant. It finds trending AI stories, locates the best YouTube and Instagram videos about them, and extracts short clips (15-60 seconds) that you can post.

**Think of it as:** A research intern that never sleeps, finds the hottest AI topics, and hands you ready-to-post content ideas.

**Tagline:** "You trigger. It hunts."

---

## What You Get

When you run Goblin Recon, it will give you:

1. **Top 5 trending AI stories** of the day (with scores)
2. **Best YouTube/Instagram videos** about those stories
3. **Exact clip timestamps** (e.g., "start at 2:34, end at 3:04")
4. **Suggested captions** for social media posts
5. **Ready-to-use briefs** you just approve or reject

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

### Step 2: Install Dependencies

Run this command inside the goblin-recon folder:
```bash
bash scripts/setup.sh
```

This creates a virtual environment and installs the approved Python packages.

**Expected output:** Something like `Installed 7 packages in 7ms`

### Step 2.5: Security Check Before Sharing

Run this command before sharing the folder, pushing to GitHub, or sending files to anyone:

```bash
python3 scripts/check_secrets.py
```

If it says `No obvious secrets found`, you are clear.

If it reports a possible secret, stop and ask an admin before sharing anything.

### Step 3: Create Your Hermes Profile

Run this command:
```bash
hermes profile create goblin-recon
```

This creates a dedicated workspace for Goblin Recon in Hermes.

### Step 4: Set Your AI Model

Run these two commands:
```bash
hermes -p goblin-recon config set model.default deepseek-v4-flash
hermes -p goblin-recon config set model.provider deepseek
```

*(Note: You can change to a different AI model later if you prefer. Ask your team lead for the preferred model.)*

### Step 5: Launch Goblin Recon

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
- `GITHUB_DISTRIBUTION.md` explains how to clone/copy from GitHub safely.
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

| What you need | Type this | What it does |
|---|---|---|
| Daily content ideas from scratch | `run full scan` | Runs the full pipeline: trends, sources, clips, and approval briefs |
| Trending AI topics only | `find trending AI stories` | Finds the top AI stories worth watching today |
| Source material for a known topic | `find sources for [topic]` | Finds YouTube and Instagram content about that topic |
| Best short clip from a known video | `find the moment in [video URL]` | Finds 15-60 second quotable moments from a video |
| Competitor/campaign research | `run competitor scan` | Checks competitor pricing, features, messaging, and public activity |

Simple rule:

- If you do not know where to start, type `run full scan`.
- If you already have a topic, type `find sources for [topic]`.
- If you already have a video, type `find the moment in [video URL]`.
- If you are planning a campaign or checking competitors, type `run competitor scan`.

Examples:

```text
run full scan
find trending AI stories
find sources for AI agents replacing SDRs
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
source .venv/bin/activate
uv pip install youtube-transcript-api
```

### Issue 2: "Profile not found"
**Fix:** Create the profile:
```bash
hermes profile create goblin-recon
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
| `find trending AI stories` | Find top 5 AI trends |
| `find sources for [topic]` | Find videos about topic |
| `find the moment in [URL]` | Extract clip from video |
| `run full scan` | Run everything at once |
| `run competitor scan` | Check competitors |
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
Edit `config/content-sources.yaml` and add channels under `youtube:` → `podcast_channels:`

Example:
```yaml
- name: "Your Favorite Channel"
  channel_id: "UC..."
  type: podcast
  focus: AI, tech
```

### Add Instagram Accounts to Monitor
Edit `config/content-sources.yaml` and add accounts under `instagram:` → `tech_accounts:`

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
