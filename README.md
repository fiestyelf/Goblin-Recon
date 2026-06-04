# Goblin Recon

**Automated Intelligence & Content Research for GenX Academy**

*"You trigger. It hunts."*

---

## What is Goblin Recon?

Goblin Recon is an AI-powered content research agent that:

1. **Finds trending AI stories** from X/Twitter, Reddit, TechCrunch, Product Hunt, Hacker News
2. **Locates source videos** on YouTube and Instagram discussing those stories
3. **Extracts quotable moments** (15-60 seconds) with exact timestamps
4. **Presents briefs** for your approval before content creation

**Use case:** Marketing team finds viral AI content → extracts best clips → creates faceless reels → posts on Instagram/TikTok/YouTube Shorts

---

## Quick Start (5 minutes)

### Step 1: Install Dependencies

```bash
# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install required Python packages for Goblin Recon
bash scripts/setup.sh
```

### Step 2: Create Your Hermes Profile

```bash
# Create a new profile for Goblin Recon
hermes profile create goblin-recon

# Set your preferred model (DeepSeek is fast and cheap)
hermes -p goblin-recon config set model.default deepseek-v4-flash
hermes -p goblin-recon config set model.provider deepseek
```

### Step 3: Load the Agent

```bash
# Navigate to the goblin-recon directory
cd goblin-recon

# Launch Hermes with your profile
hermes -p goblin-recon
```

### Step 4: Start Hunting

Once inside Hermes, use these commands:

```
"find trending AI stories"     → Finds today's top 5 trending stories
"find sources for [topic]"     → Finds YouTube/IG videos about that topic
"find the moment in [url]"     → Extracts the best 15-60 second clip
"run full scan"                → Runs all 3 layers automatically
"run competitor scan"          → Monitors competitor activity
```

---

## How It Works

### The 3-Layer Pipeline

```
Layer 1: TREND RADAR
├── Scans X/Twitter, Reddit, TechCrunch, Product Hunt, Hacker News
├── Scores stories on recency, velocity, cross-source confirmation
└── Output: Top 5 trending AI stories (score > 60/100)

         ↓

Layer 2: SOURCE HUNTER
├── Searches YouTube and Instagram for each trending story
├── Filters by topic match, recency, credibility
└── Output: 3-5 source videos per story (score > 65/100)

         ↓

Layer 3: MOMENT FINDER
├── Pulls transcripts with timestamps
├── Identifies "hot zones" (bold claims, predictions, controversy)
└── Output: Clip briefs with exact timestamps (15-60 seconds)

         ↓

HUMAN GATE
├── You approve / shelve / modify each clip brief
└── Approved briefs saved to vault/briefs/
```

### What Makes a Good Clip?

The agent looks for moments where someone:
- Makes a bold prediction ("AI will replace all jobs by 2030")
- Drops a shocking statistic ("80% of startups will fail")
- Has a heated debate or disagreement
- Reveals insider knowledge ("Nobody talks about this...")
- Shows strong emotion (laughter, gasps, "wow")

These moments stop people from scrolling.

---

## Commands Reference

### Trend Radar (Layer 1)
```
"find trending AI stories"
"what's buzzing in AI?"
"daily scan"
```

### Source Hunter (Layer 2)
```
"find sources for [topic]"
"where are people talking about [topic]?"
"find YouTube videos about [topic]"
```

### Moment Finder (Layer 3)
```
"find the moment in [video URL]"
"extract clip from [video URL]"
"what's quotable in this video?"
```

### Full Pipeline
```
"run full scan"
"goblin recon go"
"find me content"
```

### Competitor Scout
```
"run competitor scan"
"check competitors"
"what are competitors doing?"
```

---

## Output Examples

### Clip Brief Format
```
CLIP BRIEF: "AI Will Replace 80% of Jobs by 2030"

Trend Score: 78/100 | Source: Lex Fridman Podcast #421
youtube.com/watch?v=XXX&t=1842 → t=1902
Duration: 60 seconds

THE MOMENT:
"By 2030, 80% of knowledge work will be automated. Not maybe. 
Not possibly. It's happening right now. The companies that don't 
adapt will be dead in 5 years."

WHY POST:
This is a bold prediction from a credible source. Strong emotion 
("not maybe, not possibly") will trigger engagement.

CAPTION:
"80% of jobs GONE by 2030? Here's the truth nobody's talking about..."

FORMAT: Faceless reel, text overlay + podcast audio
#AI #ArtificialIntelligence #FutureOfWork #TechNews #MachineLearning
```

---

## Configuration Files

All configuration lives in the `config/` folder:

- **sources.yaml** — Where to look for trending stories
- **scoring.yaml** — How to score stories, sources, and clips
- **content-sources.yaml** — YouTube channels and Instagram accounts to monitor
- **competitors.yaml** — Competitor websites to track (add later)
- **security.yaml** — Security, API key, retention, and source-use guardrails

You can edit these files to customize what Goblin Recon finds.

---

## Security and Business-Use Guardrails

Before using Goblin Recon with company accounts or third-party APIs, read:

- `SECURITY.md` — project security policy
- `API_KEYS.md` — how keys must be stored, scoped, rotated, and revoked
- `SOCIAL_API_SETUP.md` — simple guide for enabling approved social APIs
- `GITHUB_DISTRIBUTION.md` — how to share through GitHub safely
- `LEGAL_GUARDRAILS.md` — platform, copyright, competitor research, and publishing rules
- `PRE_LAUNCH_CHECKLIST.md` — approval checklist before company rollout
- `config/security.yaml` — machine-readable defaults the agent should follow
- `config/integrations.yaml` — integration switches and required environment variable names

Core rules:

- Use public sources only unless admin/legal approves the integration.
- Do not commit API keys, cookies, tokens, `.env`, or Hermes session data.
- Do not bypass paywalls, captchas, login gates, rate limits, or access restrictions.
- Do not use personal social accounts for automated company research.
- Human review is required before publishing clips or competitor claims.

Run this before sharing or committing the folder:

```bash
python3 scripts/check_secrets.py
```

---

## Folder Structure

```
goblin-recon/
├── AGENTS.md              ← Agent personality and rules
├── SECURITY.md            ← Security policy
├── API_KEYS.md            ← API key handling guide
├── LEGAL_GUARDRAILS.md    ← Legal and platform-use rules
├── config/                ← All configuration files
├── scripts/               ← Python scripts for transcripts and scoring
├── templates/             ← Output templates (coming in Week 2-4)
├── memory/                ← Past trends and competitor snapshots
├── vault/                 ← Approved content lives here
│   ├── intake/            ← Raw scout reports land here
│   ├── briefs/            ← Approved content briefs
│   └── reports/           ← Approved competitor reports
└── README.md              ← This file
```

---

## Troubleshooting

### "No module named 'youtube_transcript_api'"
```bash
bash scripts/setup.sh
```

### "Potential secrets found"
```bash
python3 scripts/check_secrets.py
```

If this reports a finding, remove the secret before sharing or committing. If the secret was real, rotate it immediately.

### "Profile not found"
```bash
hermes profile list  # Check if profile exists
hermes profile create goblin-recon  # Create if missing
```

### "No trending stories found"
- Check internet connection
- Try running at different times (morning catches overnight trends)
- Reddit/X may be rate-limited — wait a few minutes

### "Video transcript not available"
- Some videos don't have captions/subtitles
- The agent will skip these and note "no transcript available"
- Try a different video on the same topic

---

## Advanced: Creating Your Own Personality

By default, Goblin Recon uses a neutral, professional personality. If you want to customize:

1. **Copy the default personality:**
   ```bash
   cp AGENTS.md AGENTS.custom.md
   ```

2. **Edit the personality section:**
   ```markdown
   ## Personality
   - Your custom traits here
   - Be as specific as you want
   ```

3. **Tell Hermes to use your custom file:**
   ```
   "Load AGENTS.custom.md as your personality"
   ```

---

## Weekly Workflow (Suggested)

### Monday Morning
```
hermes -p goblin-recon
"run full scan"
```
Review the top 5 trending stories. Approve 2-3 clips for the week.

### Wednesday
```
hermes -p goblin-recon
"run competitor scan"
```
Check what competitors are doing. Note any pricing or feature changes.

### Friday
```
hermes -p goblin-recon
"what did we find this week?"
```
Review approved briefs. Create content for next week.

---

## Tips for Best Results

1. **Run daily** — Trends change fast. Catch them early.
2. **Trust the scoring** — Stories below 60/100 usually aren't worth it.
3. **Approve quickly** — Don't overthink. If it's good, approve and move on.
4. **Check transcripts** — Always verify the clip actually says what the brief claims.
5. **Customize sources** — Add your favorite YouTube channels to content-sources.yaml.

---

## Support

Questions? Issues? Ideas?
- Check the troubleshooting section above
- Review the config files to customize behavior
- Ask in #goblin-bureau Slack channel

---

**Goblin Recon** — Part of the Goblin Bureau
*"You trigger. It hunts."*
