---
name: email-hook
description: |
  Generate and validate outbound email subject lines, openers, and short drafts for GenX Academy.
  Use for cold email, value emails, trust-building follow-ups, launch emails, re-engagement emails,
  subject-line variants, opener variants, and email quality checks.
category: genx-marketing
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Email Hook - Outbound Email Generator

Generate campaign-aware subject lines, openers, and short email drafts, then validate every deliverable through `goblin_recon.tools.email_gate`.

## Required Files

Before using this skill, verify these files exist:

| File | Purpose |
|---|---|
| `goblin_recon/tools/email_gate.py` | Five-dimension validation engine. |
| `config/email-guardrails.yaml` | Spam triggers, filler openers, CTA patterns, and subject rules. |
| `config/email-campaigns.yaml` | Campaign types, triggers, tones, CTAs, and subject formulas. |
| `config/brand-voice.yaml` | GenX brand voice, blacklist, and tone definitions. |

## Output Direction

Before generating brand-facing email copy, ask the Output Direction pre-check if it is missing:

1. Who is this for? B2C, B2B, or Both?
2. Where does it go? Email/outbound, client work, internal use, or other?
3. What tone should it carry? Professional, casual, edgy, warm, wry, reflective, analytical/data-driven, bold, or platform-native?

If the user skips direction, default to B2B / email-outbound / professional and state that default before generating.

## Campaign Types

Use `config/email-campaigns.yaml` to select the campaign type.

| Campaign | Primary trigger | Secondary trigger | Tone |
|---|---|---|---|
| `value` | Curiosity gap | Specificity | Direct |
| `trust_building` | Social proof | Identity | Warm |
| `launch` | Loss aversion | Curiosity gap | Bold |
| `re_engagement` | Pattern interrupt | Curiosity gap | Wry |

If the campaign type is unclear, infer the most likely type from the user's goal and say what you chose.

## Workflow

### Step 1: Collect Inputs

Capture or infer:

| Input | Example |
|---|---|
| Campaign type | `value`, `trust_building`, `launch`, `re_engagement` |
| Offer or value prop | AI team platform for founders |
| Audience segment | SME founders, 50-200 employees |
| Brand angle | B2B, B2C, or Both |
| Tone | Professional by default unless user requests another tone |
| Variant count | Default 5 |

### Step 2: Generate Variants

Generate 5 subject and opener variants unless the user requests a different count.

Each variant should include:

```json
{
  "variant": 1,
  "campaign_type": "value",
  "trigger": "curiosity_gap",
  "subject": "The metric you're not tracking",
  "opener": "Most founders track open rates. Almost no one tracks this one number, and it predicts retention better than anything else.",
  "cta": "Reply if you want the checklist."
}
```

Never generate with these patterns:

- Filler openers from `config/email-guardrails.yaml`.
- Spam triggers from `config/email-guardrails.yaml`.
- Banned GenX subject patterns from `config/email-guardrails.yaml`.
- Blacklisted GenX phrases from `config/brand-voice.yaml`.

### Step 3: Run Email Gate

Run the gate before delivering final copy.

```bash
.venv/bin/python -m goblin_recon.tools.email_gate \
  --subject "The metric you're not tracking" \
  --body "Most founders track open rates. Almost no one tracks this one number, and it predicts retention better than anything else. Reply if you want the checklist." \
  --campaign-type value \
  --brand-angle b2b
```

The gate scores:

| Dimension | Max |
|---|---:|
| Attention | 25 |
| Psychological Fit | 20 |
| Brand Voice | 25 |
| Professional Guardrails | 15 |
| Campaign Alignment | 15 |

Verdicts:

| Score | Verdict | Delivery rule |
|---|---|---|
| 80-100 | PASS | Can recommend. |
| 60-79 | FLAGGED | Show only if useful and explain fixes. |
| 0-59 | REJECT | Do not deliver as final copy. Regenerate. |

### Step 4: Deliver Results

Use this format:

```markdown
## Decision

Recommended variant: [N] - [score]/100 - PASS
Campaign: [value / trust_building / launch / re_engagement]
Trigger: [curiosity_gap / social_proof / loss_aversion / pattern_interrupt]

## Recommended Copy

Subject: [subject]

[email body]

## Gate Results

| Dimension | Score | Max | Status |
|---|---:|---:|---|
| Attention | X | 25 | PASS/FAIL |
| Psychological Fit | X | 20 | PASS/FAIL |
| Brand Voice | X | 25 | PASS/FAIL |
| Professional Guardrails | X | 15 | PASS/FAIL |
| Campaign Alignment | X | 15 | PASS/FAIL |
| Total | X | 100 | PASS/FLAGGED/REJECT |

## Alternatives

| Variant | Subject | Score | Verdict | Best use |
|---:|---|---:|---|---|
| 1 | ... | 84 | PASS | Best default |

## Next Step

[Send as-is / expand into full body / regenerate around a sharper angle]
```

## Anti-Patterns

- Do not skip `email_gate`.
- Do not deliver rejected variants as final copy.
- Do not use filler openers.
- Do not use generic cold-email subjects like `quick question` or `are you interested`.
- Do not pitch aggressively in a value campaign.
- Do not create fake scarcity for launch campaigns.
- Do not use emoji in final email output unless the user explicitly asks.

## Validation Command

For a quick known-good check:

```bash
.venv/bin/python -m goblin_recon.tools.email_gate \
  --subject "The metric you're not tracking" \
  --body "Most founders track open rates. Almost no one tracks this one number, and it predicts retention better than anything else. Reply if you want the checklist." \
  --campaign-type value \
  --brand-angle b2b
```
