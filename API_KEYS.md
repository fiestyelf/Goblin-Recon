# API Key Handling Guide

Goblin Recon should work without API keys for the current local transcript scripts. Future integrations may require keys for X/Twitter, Reddit, YouTube Data API, Discord, or paid research tools. Use this guide before adding any key.

---

## Simple Rule

If a value can unlock an account, spend money, access private data, post messages, or bypass limits, treat it as a secret.

---

## Where Keys Should Live

Recommended:

1. Hermes profile secret storage.
2. Local `.env` file that is never committed.
3. Company secret manager for deployed usage.

Not allowed:

1. `config/*.yaml`
2. `README.md`
3. `docs/ops/instructions.md`
4. `AGENTS.md`
5. `skills/**/SKILL.md`
6. Screenshots or copied terminal output.

---

## Three Safe Ways to Insert Keys

### 1. Local `.env` file

Best for local team usage.

```bash
cp .env.example .env
```

Then add approved values to `.env`. Never commit or share `.env`.

### 2. Hermes profile secrets

Best when Hermes supports profile-level secret storage.

Use Hermes secret commands instead of pasting keys into chat. If unsure, ask the admin for the exact Hermes command.

### 3. Company secret manager

Best for scheduled jobs, shared automation, or production usage.

Use GitHub Actions secrets, 1Password, AWS Secrets Manager, Doppler, Infisical, or the company-approved vault.

For social API setup details, read `docs/ops/social-api-setup.md`.

---

## Local `.env` Workflow

1. Copy `.env.example` to `.env`.
2. Add only the keys approved for your account.
3. Never share `.env`.
4. Run `python3 scripts/check_secrets.py` before sharing files.

Example:

```bash
cp .env.example .env
```

Then edit `.env` locally. Do not commit it.

---

## Key Approval Checklist

Before adding a new key, answer these questions:

1. What provider is this key for?
2. What data will it access?
3. Can it post, delete, message, or spend money?
4. Can scope be reduced to read-only?
5. Who owns the key: company or personal account?
6. Who can revoke it?
7. What is the monthly cost or rate limit?
8. Does the provider allow this usage in its terms?
9. Where will the key be stored?
10. When will it be rotated?

If any answer is unknown, do not add the key yet.

---

## Recommended Scopes

Use the smallest possible scope.

| Integration | Preferred Scope | Avoid |
|---|---|---|
| YouTube Data API | Read-only public metadata | Upload/delete/manage channel |
| Reddit API | Read-only public posts | Mod actions, private messages |
| X/Twitter API | Read-only search | Posting, DM access |
| Discord | Incoming webhook only | Bot admin permissions |
| Instagram/Meta | Approved public insights only | Personal account automation |

---

## Rotation Rules

Rotate keys:

1. Every 90 days.
2. Immediately after suspected leak.
3. When a team member leaves.
4. When permissions change.
5. When moving from testing to production.

---

## If a Key Leaks

1. Revoke it first.
2. Remove it from files.
3. Run the secret scanner.
4. Notify the admin.
5. Create a new scoped key.
6. Record what happened and how it was fixed.

Do not try to hide or ignore leaked keys.
