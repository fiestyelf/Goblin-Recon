---
name: moment-finder
description: Extract 15-60 second clip moments from source video transcripts or user-provided excerpts.
category: genx-marketing
version: 1.1.0
---

# Moment Finder

Goal: choose the shortest useful clip moment that would stop the scroll.

## Inputs

- source URL
- transcript or excerpt
- speaker/channel/title
- trend/category/audience angle

## Rules

- Duration: 15-60 seconds, optimal ~30s.
- Natural sentence start and end.
- No mid-sentence cuts.
- No full raw transcript storage.
- Validate timestamps with `goblin_recon.tools.clip_extractor`.
- Run Clip Vault dedup before recommending.

## Flow

```text
source + transcript -> candidate moments -> score -> dedup -> brand gate -> clip brief
```

## Score

0-100:
- hook strength: 25
- clarity without context: 20
- brand/audience fit: 20
- source proof: 15
- editability: 10
- novelty: 10

Include threshold: 60. If uncertain, shelve.

## Output

Use `templates/clip-mine-brief.md`.

Required:
- `## Decision`
- `## Background`
- source URL and publication date
- start/end timestamps
- short transcript quote
- why post
- engagement analytics
- brand gate
- vault check
- Instagram, LinkedIn, YouTube Shorts variants
- editor instructions
- next action

Save generated briefs to `vault/briefs/` only after human approval or explicit request.
