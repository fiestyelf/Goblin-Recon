# Goblin Recon Pre-Launch Checklist

Use this checklist before the team starts using Goblin Recon with company accounts, third-party APIs, or recurring workflows.

---

## 1. Repository Safety

- [ ] `.gitignore` is present.
- [ ] `.env` is not committed.
- [ ] `.venv` is not committed.
- [ ] `vault/` outputs are not committed unless intentionally approved.
- [ ] `python3 scripts/check_secrets.py` returns `No obvious secrets found.`

---

## 2. API Key Approval

- [ ] Each API key belongs to a company-approved account.
- [ ] No personal employee social accounts are used for automation.
- [ ] Each key has the minimum required scope.
- [ ] Read-only access is used whenever possible.
- [ ] Billing alerts are enabled for paid APIs.
- [ ] Key owner and revocation process are documented.
- [ ] Rotation schedule is defined.

---

## 3. Source Approval

- [ ] Source is public or explicitly approved.
- [ ] Source does not require paywall bypass.
- [ ] Source does not require captcha bypass.
- [ ] Source does not require private group or private account access.
- [ ] Platform terms allow the intended access pattern.
- [ ] Rate limits are understood.
- [ ] Access-denied behavior is `stop`, not `bypass`.

---

## 4. Legal and Publishing Review

- [ ] Every brief includes source URL, creator/publisher, date, and timestamp when relevant.
- [ ] Clips are reviewed before publishing.
- [ ] Competitor claims are reviewed before publishing.
- [ ] Sensitive claims are reviewed before publishing.
- [ ] Copyright or reuse concerns are resolved before publishing.
- [ ] The content does not misrepresent the speaker or source.

---

## 5. Data Retention

- [ ] Raw intake retention is set to 30 days.
- [ ] Approved brief retention is set to 365 days.
- [ ] Competitor snapshot retention is set to 365 days.
- [ ] Full raw transcripts are not stored by default.
- [ ] Team knows where approved outputs are stored.

---

## 6. Team Training

- [ ] Team has read `INSTRUCTIONS.md`.
- [ ] Team has read `SECURITY.md`.
- [ ] Team knows not to paste keys into chat.
- [ ] Team knows when to use `approve`, `shelve`, and `modify`.
- [ ] Team knows to shelve unclear or risky items.

---

## Launch Decision

Launch only when every required item above is checked.

If any item is unclear, pause and resolve it before using Goblin Recon with company accounts.
