---
name: email-hook
description: Generate and score outbound email subject lines, openers, and short drafts.
category: genx-marketing
version: 1.1.0
---

# Email Hook

Goal: write short outbound email hooks that earn a reply without hype.

## Inputs

Ask only if missing:
- offer
- audience
- campaign type
- desired tone
- proof/result/source

Load `config/email-campaigns.yaml` when campaign fit matters.

## Flow

```text
offer + audience -> campaign fit -> subject/opening variants -> goblin_recon.tools.email_gate -> Security Rail -> final picks
```

## Rules

- No fake personalization.
- No unsupported revenue/performance claims.
- No manipulative urgency.
- No blacklisted brand phrases.
- Keep drafts short: subject + 2-5 sentence body unless user asks longer.

## Output

Start with `## Decision`.

Return:
- top 3 subject lines with scores
- top 3 openers with scores
- one recommended short draft
- why it works
- risks/human-review items
- next step

Run `goblin_recon.tools.email_gate` before final copy when feasible. Run `skills/security-rail/SKILL.md` before delivery.
