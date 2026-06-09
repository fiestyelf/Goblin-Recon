# Goblin Recon Security Policy

This project is intended for internal business use by the GenX Academy team. It must be used only with approved accounts, approved data sources, and approved API keys.

This document is an operational security policy. It is not legal advice. If a source, clip, competitor claim, or platform workflow feels legally unclear, pause and ask the company owner or legal reviewer before publishing or automating it.

---

## Security Goals

1. Prevent API keys, tokens, internal prompts, and unpublished content from leaking.
2. Use public online data responsibly without bypassing access controls.
3. Keep company accounts safe from rate-limit violations, account bans, or platform abuse flags.
4. Ensure humans approve clips and competitor claims before public posting.
5. Keep only the minimum data needed for marketing decisions.

---

## Hard Rules

1. Never commit `.env`, API keys, access tokens, cookies, session files, or private credentials.
2. Never paste API keys into Hermes chat, Discord, Slack, GitHub issues, or content briefs.
3. Do not scrape login-only pages, private accounts, private groups, paid content, or paywalled content unless the company has written approval and the platform terms allow it.
4. Do not bypass captchas, rate limits, robots.txt, geo-blocks, account restrictions, or platform safety controls.
5. Do not use personal employee accounts for automated research. Use company-approved accounts only.
6. Do not collect personal data unless it is already public and directly needed for the approved marketing task.
7. Do not publish a clip, quote, claim, or competitor statement without human review.
8. If access is denied, stop. Do not work around the block.

---

## API Key Rules

Use this order of preference:

1. Hermes profile secret storage, if available.
2. Environment variables on the local machine or approved deployment environment.
3. Company secret manager, if the project is deployed later.

Do not use:

1. Keys hardcoded in scripts.
2. Keys inside YAML config files.
3. Keys inside Markdown files.
4. Keys pasted into prompts.
5. Keys from personal accounts.

Recommended key practices:

1. Create separate keys per tool or integration.
2. Use read-only scopes whenever possible.
3. Restrict keys by domain, IP, or app if the provider supports it.
4. Rotate keys every 90 days or immediately after suspected exposure.
5. Revoke keys when a team member leaves or no longer needs access.
6. Keep billing alerts enabled for paid APIs.

---

## Approved Data Collection

Allowed by default:

1. Public news pages.
2. Public YouTube videos and public captions/transcripts.
3. Public Reddit posts and comments that do not require login-only access.
4. Public Product Hunt pages.
5. Public company websites, pricing pages, changelogs, and blogs.

Requires review before use:

1. X/Twitter API or scraping.
2. Instagram data collection.
3. LinkedIn data collection.
4. Competitor ad libraries or paid intelligence tools.
5. Any source that requires a login, cookie, token, or browser session.

Forbidden unless legal/admin explicitly approves:

1. Private groups or communities.
2. Paywalled reports or paid courses.
3. Automated scraping with personal accounts.
4. Captcha bypassing or bot evasion.
5. Downloading copyrighted videos for reposting without rights review.

---

## Copyright and Publishing Guardrails

Goblin Recon finds moments and creates briefs. It does not grant rights to reuse content.

Before publishing a clip, the human reviewer must check:

1. Is the source public?
2. Is the clip short and transformative enough for the intended use?
3. Are we adding commentary, context, captions, or analysis?
4. Are we crediting the source and creator?
5. Are we avoiding misleading edits or out-of-context claims?
6. Is the topic sensitive, defamatory, financial, medical, or legal?

If any answer is unclear, shelve the clip or request review.

---

## Data Retention

Default retention:

1. Raw intake: 30 days.
2. Approved content briefs: 365 days.
3. Competitor snapshots: 365 days.
4. Local logs: delete when no longer needed.

Do not store full raw transcripts by default. Store source URLs, timestamps, and short excerpts instead. Any exception requires explicit human approval and a documented retention reason.

---

## Pre-Share Checklist

Run this before pushing or sharing the folder:

```bash
python3 scripts/check_secrets.py
```

Also verify:

1. `.env` is not committed.
2. `.venv` is not committed.
3. `vault/` content does not contain private or unpublished sensitive material.
4. No API keys appear in screenshots, docs, prompts, or logs.
5. All third-party integrations are approved.

---

## Incident Response

If a key or private data is exposed:

1. Stop using the exposed key immediately.
2. Revoke or rotate the key in the provider dashboard.
3. Remove the secret from files and history if it was committed.
4. Notify the company owner/admin.
5. Review logs to see what was accessed.
6. Create a new scoped key only after the leak is cleaned up.

Do not keep working with a leaked key.
