# Social Media API Setup Guide

This guide explains how to add API keys safely for Goblin Recon.

Use this only after the company approves the integration. Do not connect personal accounts for company automation.

---

## The Simple Rule

API keys should never be written inside project code, YAML configs, Markdown files, prompts, Slack, Discord, or screenshots.

Use one of these safe methods instead:

1. Hermes profile secrets, if Hermes supports secret storage.
2. A local `.env` file that is never committed.
3. A company secret manager, if Goblin Recon is deployed later.

For the current local team setup, the simplest method is `.env`.

---

## Method 1: Local `.env` File, Simple Team Setup

Use this for local marketing team usage.

### Step 1: Copy the template

```bash
cp .env.example .env
```

### Step 2: Open `.env`

Open `.env` in your editor and fill only the keys approved for your account.

Example:

```bash
YOUTUBE_API_KEY=
X_BEARER_TOKEN=
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USER_AGENT=GoblinRecon/0.1 by GenXAcademy
```

### Step 3: Do not share `.env`

The `.env` file is ignored by Git through `.gitignore`. Still, do not send it in Slack, email, Discord, screenshots, or support tickets.

### Step 4: Run the secret check

```bash
python3 scripts/check_secrets.py
```

If it reports a secret, stop and ask an admin before sharing files.

---

## Method 2: Hermes Profile Secrets

Use this if Hermes supports storing secrets inside a profile.

The exact command may depend on your Hermes version. The idea is:

```bash
hermes -p goblin-recon secrets set YOUTUBE_API_KEY
hermes -p goblin-recon secrets set X_BEARER_TOKEN
hermes -p goblin-recon secrets set REDDIT_CLIENT_ID
hermes -p goblin-recon secrets set REDDIT_CLIENT_SECRET
```

If your Hermes version uses different commands, ask your admin for the approved command. Do not paste the key into the normal chat window.

---

## Method 3: Company Secret Manager

Use this if Goblin Recon is later deployed to a server or shared automation environment.

Examples include GitHub Actions secrets, 1Password service accounts, AWS Secrets Manager, Doppler, Infisical, or another approved company vault.

Use this method when:

1. More than one person needs the same integration.
2. The workflow runs on a schedule.
3. The workflow can spend money or touch company accounts.
4. Audit logs are required.

---

## How to Enable a Social API Safely

Do not enable every API just because the fields exist. Enable only what you need.

### Step 1: Get approval

Before enabling an API, answer:

1. What data will this API read?
2. Is the data public?
3. Is the account company-owned?
4. Is the permission read-only?
5. Does the platform allow this use?
6. Who can revoke the key?
7. What is the monthly cost or rate limit?

If any answer is unclear, do not enable it yet.

### Step 2: Add the key to `.env` or Hermes secrets

Do not add keys to source files or chat. MCP servers are listed in `mcp.json`.

### Step 3: Test with a low-risk command

Start with read-only testing. Do not post, message, follow, like, vote, or comment.

### Step 5: Review outputs manually

Every trend, competitor claim, and clip brief still needs human review before publishing.

---

## Recommended API Keys by Platform

### YouTube

Current transcript extraction does not need a YouTube API key.

Use `YOUTUBE_API_KEY` only if you later need official YouTube Data API metadata like channel stats, search, or video details.

Recommended permission: public read-only metadata.

Avoid: upload, delete, channel management.

### X/Twitter

Use `X_BEARER_TOKEN` for approved read-only trend/search data.

Recommended permission: read-only.

Avoid: posting, deleting, direct messages, account management.

### Reddit

Use:

```bash
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USER_AGENT=GoblinRecon/0.1 by GenXAcademy
```

Recommended permission: read-only public posts/comments.

Avoid: private messages, moderation, posting, voting.

### Instagram / Meta

Use Meta-approved app credentials only:

```bash
META_APP_ID=
META_APP_SECRET=
META_ACCESS_TOKEN=
```

Recommended permission: approved business/public data only.

Avoid: personal account automation, scraping login-only pages, bypassing restrictions.

### LinkedIn

Use LinkedIn-approved app credentials only:

```bash
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
```

Recommended permission: approved organization/page data only.

Avoid: profile scraping, personal account automation, unsolicited messaging.

### Discord

Use `DISCORD_WEBHOOK_URL` only for sending approved briefs to one channel.

Recommended permission: single-channel incoming webhook.

Avoid: broad bot admin permissions.

---

## Do Not Use Personal Accounts

For company work, avoid personal accounts because:

1. The company cannot safely revoke access.
2. The employee may be personally rate-limited or banned.
3. It mixes personal and company data.
4. It creates audit and ownership issues.

Use company-owned developer apps and company-owned social accounts.

---

## If a Key Leaks

Do this immediately:

1. Revoke the key in the provider dashboard.
2. Remove it from the file or message.
3. Run `python3 scripts/check_secrets.py`.
4. Notify the admin.
5. Create a new read-only scoped key.
6. Record what happened and how it was fixed.

Do not keep using a leaked key.
