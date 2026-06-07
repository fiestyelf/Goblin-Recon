# Hermes Approvals and Startup Guide

This guide tells team members what to approve in Hermes so Goblin Recon can work properly without giving it unsafe access.

---

## What Goblin Recon Needs

Goblin Recon needs these Hermes capabilities:

1. **Web/search access** to find public trends and articles.
2. **Browser access** to inspect public pages when search results are not enough.
3. **File access** to read configs, skills, templates, and save approved briefs.
4. **Terminal access** to run local Python scripts for transcripts, scoring, tests, and secret scanning.
5. **Skills access** to load `trend-radar`, `source-hunter`, `moment-finder`, `competitor-scout`, and `orchestrator`.
6. **Memory/session search access** if the user wants deduplication and past-scan review.

It does not need personal account passwords, cookies, private browser sessions, or full computer access outside this folder.

---

## Recommended Hermes Tool Approvals

Enable these for the `goblin-recon` profile:

```bash
hermes tools enable web -p goblin-recon
hermes tools enable browser -p goblin-recon
hermes tools enable file -p goblin-recon
hermes tools enable terminal -p goblin-recon
hermes tools enable memory -p goblin-recon
hermes tools enable session_search -p goblin-recon
hermes tools enable skills -p goblin-recon
```

If Hermes asks for approval during a task, approve only actions that match the current job.

---

## Safe Approvals

Approve these:

| Hermes Request | Approve? | Why |
|---|---|---|
| Read files inside `goblin-recon/` | Yes | Needed for configs, skills, templates |
| Write files inside `vault/` or `memory/` | Yes | Needed to save approved briefs and scan history |
| Run scripts from `scripts/` | Yes | Needed for transcripts, scoring, setup, tests |
| Browse public URLs | Yes | Needed for research |
| Search public web results | Yes | Needed for trend discovery |
| Use approved `.env` or Hermes secrets | Yes | Only if keys were approved by admin |

---

## Unsafe Approvals

Deny these unless the company owner/admin explicitly approves:

| Hermes Request | Default Action | Why |
|---|---|---|
| Access files outside `goblin-recon/` | Deny | Prevent accidental data exposure |
| Read `.env` out loud or print secrets | Deny | Prevent key leakage |
| Use personal cookies or browser sessions | Deny | Prevent personal/company account risk |
| Login to personal social accounts | Deny | Do not automate personal accounts |
| Bypass paywall, captcha, rate limit, or access block | Deny | Legal/platform risk |
| Post, comment, DM, like, vote, or follow | Deny | Goblin Recon is research-first, not posting automation |
| Download full videos for reposting | Deny | Copyright risk |
| Access private groups, private communities, or paid content | Deny | Legal/platform risk |

---

## First-Time Startup Script

Team members should run this once after cloning:

```bash
cd goblin-recon
bash scripts/setup.sh
python3 scripts/check_secrets.py
hermes -p goblin-recon
```

If setup warns that profile creation failed, run this manually and rerun setup:

```bash
hermes profile create goblin-recon
```

---

## First Message To Send Hermes

After starting Hermes, paste this:

```text
Load this folder as the Goblin Recon agent. Follow AGENTS.md, SECURITY.md, LEGAL_GUARDRAILS.md, config/security.yaml, and the skills under skills/. Use only public sources unless an integration is explicitly approved. Do not ask for or reveal API keys. Start in manual approval mode.
```

Then run the desired command:

```text
run full scan
```

---

## Daily Startup

After the first setup, most users only need:

```bash
cd goblin-recon
hermes -p goblin-recon
```

Then type one of:

```text
run full scan
find trending AI stories
find sources for [topic]
find the moment in [video URL]
run competitor scan
```

---

## Approval Mode Rule

Keep Goblin Recon in **manual approval mode**.

The agent can research and prepare briefs, but a human must approve before:

1. Saving final content briefs.
2. Publishing clips.
3. Making competitor claims.
4. Enabling a new API integration.
5. Using a company social account.

---

## If Hermes Asks For API Keys

Do not paste keys into normal chat.

Use one of the approved methods from `API_KEYS.md` and `SOCIAL_API_SETUP.md`:

1. Hermes profile secrets.
2. Local `.env` file.
3. Company secret manager.

Then tell Hermes:

```text
The approved key is available in the local environment. Do not print it. Use it only for the approved read-only integration.
```

---

## If Something Feels Risky

Tell Hermes:

```text
Shelve this item and explain the risk.
```

Use this when:

1. Source is missing.
2. Date is missing.
3. Access requires login or private account.
4. Clip may be misleading.
5. Platform rules are unclear.
6. API key or account safety is unclear.

When unsure, shelve rather than approve.
