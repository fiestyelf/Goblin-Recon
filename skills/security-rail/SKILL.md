---
name: security-rail
description: Final safety, source, access, claim, and usefulness gate before user-facing Goblin Recon output.
category: genx-marketing
version: 1.1.0
---

# Security Rail

Goal: decide if an output is safe and useful to deliver.

Return exactly one decision:

```text
APPROVE
REVISE
SHELVE
NEEDS HUMAN REVIEW
```

## Check

1. Sources: real URLs, dates, public/approved access.
2. Access: no login/paywall/captcha/rate-limit/robots bypass.
3. Secrets: no keys, tokens, cookies, private data.
4. Claims: no unsupported competitor, health, legal, financial, performance, or sensitive claims.
5. Copyright: no raw transcript dumps, no republishing restricted content.
6. Brand: no unhandled blacklisted phrases in GenX-written copy.
7. Usefulness: recommendation is specific, current, and actionable.

## Decisions

- `APPROVE`: safe to deliver.
- `REVISE`: fixable issue; rewrite and deliver the revised version.
- `SHELVE`: weak, stale, blocked, unsafe, or unsupported. Do not recommend.
- `NEEDS HUMAN REVIEW`: publish/send/legal/sensitive/competitor claim needs approval.

## Output

```text
Security Rail: APPROVE|REVISE|SHELVE|NEEDS HUMAN REVIEW
Reason: one sentence
Required fix: only if REVISE or NEEDS HUMAN REVIEW
```

When uncertain, choose `SHELVE`.
