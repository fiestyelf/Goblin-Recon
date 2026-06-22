---
name: caption-tone
description: Write platform-ready GenX captions and descriptions with brand guardrails. Use for caption, description, hook, LinkedIn post, Instagram caption, YouTube Shorts description.
category: genx-marketing
version: 2.1.0
---

# Caption Tone

Goal: produce concise, brand-safe captions. Do not invent facts or sources.

## Inputs

Ask only if missing:
- audience: B2C, B2B, or Both
- platform: Instagram, LinkedIn, YouTube Shorts, email, other
- tone: professional, casual, edgy, warm, wry, reflective, analytical/data-driven, bold, platform-native
- source proof: URL, quote, result, or user-provided context

Default: Both / Faceless Instagram / professional.

## Brand Rules

Load:
- `memory/brand-rules.md`
- `config/brand-voice.yaml`

Avoid blacklisted phrases in GenX-written copy. If a quoted source contains them, flag the quote and write around it.

B2C: real science + real soul, transformation through proof, not woo.
B2B: results, delivery, operators, no advice-merchant language.

## Flow

```text
input -> audience/platform/tone -> draft variants -> brand_gate -> skills/security-rail/SKILL.md -> templates/caption-pack.md
```

## Output

Use `templates/caption-pack.md` for multi-caption work.

For quick caption requests, return:

```text
## Decision
Recommended caption: ...

Variants:
1. ...
2. ...
3. ...

Brand Gate: pass/revise/shelve
Security Rail: APPROVE/REVISE/SHELVE/NEEDS HUMAN REVIEW
Next step: ...
```

## Platform Defaults

- Instagram: short hook, 1 idea, readable line breaks, light CTA.
- LinkedIn: operator context, proof, practical takeaway.
- YouTube Shorts: direct description, source/context, no fluff.
- Email: use `skills/email-hook/SKILL.md` instead.

## Gate

Run `goblin_recon.tools.brand_gate` when feasible. Run `skills/security-rail/SKILL.md` before final delivery. If factual, competitor, performance, health, legal, or sensitive claims lack proof, mark `NEEDS HUMAN REVIEW` or `REVISE`.
