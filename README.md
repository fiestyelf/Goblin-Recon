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

For a clean file-by-file explanation of the repository, read [`FILE_DESCRIPTIONS.md`](FILE_DESCRIPTIONS.md).

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
- `HERMES_APPROVALS.md` — what Hermes permissions to approve or deny
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

## Repository Map

Use this section to understand what every major file and folder does.

### Core Agent Files

| File | What It Does |
|---|---|
| `README.md` | Main technical overview for Goblin Recon. Use this first if you are setting up or reviewing the project. |
| `FILE_DESCRIPTIONS.md` | Complete file-by-file guide explaining the job of every tracked file and folder. |
| `INSTRUCTIONS.md` | Simple marketing-team guide with setup steps, commands, examples, and when to trigger each workflow. |
| `AGENTS.md` | The main Hermes agent rules: identity, behavior, source verification, clip rules, and security guardrails. |
| `HERMES_APPROVALS.md` | Explains which Hermes permissions to approve or deny when starting Goblin Recon. |

### Security and Compliance Files

| File | What It Does |
|---|---|
| `SECURITY.md` | Business-use security policy for API keys, public-source rules, data retention, and incident response. |
| `API_KEYS.md` | Explains safe API key handling: `.env`, Hermes secrets, company secret managers, rotation, and leak response. |
| `SOCIAL_API_SETUP.md` | Simple guide for adding approved social media API keys and enabling integrations safely. |
| `LEGAL_GUARDRAILS.md` | Explains platform, copyright, competitor research, source attribution, and publish/shelve rules. |
| `PRE_LAUNCH_CHECKLIST.md` | Final checklist before rolling Goblin Recon out to the marketing team. |
| `.env.example` | Safe template showing allowed environment variable names. Copy to `.env` locally, but never commit `.env`. |
| `.gitignore` | Prevents local secrets, virtual environments, logs, caches, and vault outputs from being committed. |

### Configuration Files

| File | What It Does |
|---|---|
| `config/sources.yaml` | Defines where Trend Radar looks for AI trends: X/Twitter queries, Reddit subreddits, tech news sites, and Product Hunt topics. |
| `config/scoring.yaml` | Defines score thresholds and weights for trend scoring, source scoring, moment scoring, and clip duration rules. |
| `config/content-sources.yaml` | Defines YouTube channels, Instagram accounts, hashtags, and search query patterns for Source Hunter. |
| `config/competitors.yaml` | Placeholder for competitors to monitor later. Keep empty until actual competitors are approved. |
| `config/security.yaml` | Machine-readable security defaults: public-only sources, API key rules, rate limits, human review, and retention. |
| `config/integrations.yaml` | Registry of optional third-party integrations. All social APIs are disabled by default until approved. |

### Skills

| File | What It Does |
|---|---|
| `skills/orchestrator/SKILL.md` | Main driver. Runs Trend Radar -> Source Hunter -> Moment Finder -> Human Gate when the user says `run full scan`. |
| `skills/trend-radar/SKILL.md` | Layer 1. Finds and scores trending AI stories from public sources. |
| `skills/source-hunter/SKILL.md` | Layer 2. Finds YouTube and Instagram sources for a selected trend or known topic. |
| `skills/moment-finder/SKILL.md` | Layer 3. Finds 15-60 second clip moments from transcripts and creates clip briefs. |
| `skills/competitor-scout/SKILL.md` | Standalone campaign/competitor research flow for pricing, features, messaging, and public activity. |

### Scripts and Local Tooling

| File | What It Does |
|---|---|
| `scripts/setup.sh` | One-command local setup. Creates `.venv` and installs approved Python dependencies. |
| `scripts/check_secrets.py` | Lightweight scanner that checks the repo for accidental API keys, tokens, or webhooks before sharing or pushing. |
| `scripts/get_youtube_transcript.py` | Pulls public YouTube captions/transcripts with timestamps using `youtube-transcript-api`. |
| `scripts/extract_clip.py` | Validates video URLs and clip boundaries, then creates timestamped clip metadata. |
| `scripts/score_engagement.py` | Calculates engagement velocity scores for X/Twitter, Reddit, YouTube, and Instagram-style inputs. |
| `requirements.txt` | Pinned Python dependency list for simple installation. |
| `pyproject.toml` | Project metadata and Python dependency declaration for `uv`. |
| `tests/test_scripts.py` | Offline unit tests for URL validation, clip extraction, transcript input validation, and scoring safety checks. |

### Templates

| File | What It Does |
|---|---|
| `templates/trend-report.md` | Output format for daily AI trend reports. |
| `templates/clip-brief.md` | Output format for short-form clip opportunities with timestamps, hooks, captions, and hashtags. |
| `templates/content-brief.md` | Output format for broader content planning based on approved trends and sources. |
| `templates/competitor-report.md` | Output format for competitor intelligence reports. |

### Memory and Output Folders

| Path | What It Does |
|---|---|
| `memory/trend-history.md` | Stores past trends for deduplication and review. Starts as a placeholder. |
| `memory/competitor-snapshots.md` | Stores competitor snapshots for future change detection. Starts as a placeholder. |
| `memory/content-performance.md` | Stores performance notes after content is posted, so scoring can improve later. Starts as a placeholder. |
| `vault/intake/` | Local folder for raw scout reports. Contents are ignored by Git except `.gitkeep`. |
| `vault/briefs/` | Local folder for approved content briefs. Contents are ignored by Git except `.gitkeep`. |
| `vault/reports/` | Local folder for approved competitor reports. Contents are ignored by Git except `.gitkeep`. |

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
