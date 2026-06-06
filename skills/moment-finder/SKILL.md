# Moment Finder — Layer 3

## Purpose
Extract the exact clip moment (15-60 seconds) from source videos.

## Triggers
- Automatic chain from Layer 2 (source-hunter)
- "find the moment in [video URL]"
- "extract clip from [url]"

## Tools Required
- terminal (python scripts)
- browser (for Instagram caption extraction)
- config/scoring.yaml
- config/brand-voice.yaml
- memory/brand-rules.md
- scripts/get_youtube_transcript.py
- scripts/extract_clip.py

## Optional Helpers
- MCP Memory: compare candidate moments with previously approved/shelved clips
- FunASR: not enabled by default; consider later only when captionless videos regularly block useful sources

## Execution Flow

### Step 0: Security and Rights Preflight
- Read config/security.yaml
- Use transcripts only from public sources or approved APIs
- Do not store full raw transcripts unless explicitly approved
- Include source attribution and timestamp in every clip brief
- Human review is required before publishing any clip
- Shelve clips when copyright, context, or quote accuracy is unclear

### Step 0.5: Brand Preflight
- Load memory/brand-rules.md
- Load config/brand-voice.yaml
- Every clip must have Brand Angle: B2C, B2B, or Both
- Every clip must pass brand_alignment >= 8/15
- Blacklisted words in quoted transcript are allowed only as source material; GenX-written hook, caption, and explanation must not use them

### Step 1: Receive Sources
```
For each source from Layer 2:
  - If has transcript: proceed to Step 2
  - If no transcript: skip, note "no transcript available"
```

### Step 2: Scan for "Hot Zones"

Read transcript and mark moments where:

**Bold Claims:**
- Keywords: "will", "never", "always", "guarantee", "100%", "definitely"
- Example: "AI will replace all jobs by 2030"

**Predictions:**
- Keywords: "by 2028", "in 2 years", "inevitably", "the future is"
- Example: "In 5 years, every company will have an AI CEO"

**Controversy:**
- Keywords: "I disagree", "that's wrong", "unpopular opinion", "the truth is"
- Example: "Everyone is wrong about AI safety"

**Revelations:**
- Keywords: "nobody talks about", "the secret is", "here's what...", "insider"
- Example: "The secret nobody tells you about ChatGPT"

**Statistics:**
- Pattern: numbers followed by "%", "billion", "million"
- Example: "80% of startups will fail", "3 billion users"

**Emotional Peaks:**
- Keywords: "wow", "oh my god", "incredible", "unbelievable"
- Indicators: laughter, gasps, exclamation marks

**Debate:**
- Pattern: two people disagreeing, heated exchange
- Example: "You're completely wrong" / "No, you are"

**Truly Seen Moments:**
- The speaker names a private frustration, identity tension, or emotional truth the audience rarely hears described accurately.
- B2C example pattern: successful externally, numb or disconnected internally.
- B2B example pattern: operator looks functional from outside while the business runs on exhaustion.

**Operator Moments:**
- The speaker explains what actually has to change in behavior, systems, delivery, or decision-making.
- Prefer proof, mechanism, and operational detail over motivational advice.

### Step 3: Context Window

For each hot zone found:

```
1. Read 60 seconds before and after for context
2. Ask: does this moment LAND? Is there setup → payoff?
3. Ask: would someone stop scrolling for this?
4. Score the moment:
   - Quotability: 0-30 (would someone quote this?)
   - Emotion: 0-20 (does it evoke strong reaction?)
   - Clarity: 0-20 (is the point clear without context?)
   - Controversy: 0-15 (does it challenge thinking?)
   - Visual potential: 0-10 (faceless reel with text overlay?)
   - Brand alignment: 0-15 (B2C science+soul/truly-seen or B2B results-not-advice)
5. Add qualitative checks:
   - Truly-seen signal: strong/medium/weak
   - Emotional signature: named emotion the viewer should feel
   - Operator framing: strong/medium/weak
```

**Threshold:** 60/100 to include

**Brand gate:**
- B2C clips should feel emotionally true, alive, and grounded; avoid woo and empty transformation language.
- B2B clips should express rigor, implementation, operations, proof, or results; avoid advice-merchant tone.
- If the best caption would require hype, fake urgency, or generic filler to work, shelve the clip.

**First-touch feeling check:**
- Ask what the audience feels in the first 3 seconds: recognized, challenged, relieved, provoked, or nothing.
- If the honest answer is "nothing" or "generic interest," shelve unless the clip has exceptional proof or utility.

### Step 4: Determine Clip Boundaries

For each moment that passes scoring:

```
START POINT:
  - Find natural sentence beginning
  - Go ~5 seconds before the "moment"
  - Ensure no mid-sentence cut

END POINT:
  - Find natural pause or topic change
  - Go ~5-10 seconds after the moment
  - Ensure complete thought

DURATION CHECK:
  - Must be 15-60 seconds
  - Optimal: 30 seconds
  - If too long: tighten boundaries
  - If too short: extend to natural pause
```

### Step 5: Generate Clip Brief

Use template: templates/clip-brief.md

For each clip:

```
CLIP BRIEF: "[headline]"

Source: [video title] | Channel: [name]
URL: youtube.com/watch?v=XXX&t=[START] → t=[END]
Duration: [X] seconds
Brand Angle: [B2C/B2B/Both]
Brand Alignment: [X]/15
Voice Category: [alive/awakening/limitless/provocative/structural]
Truly-Seen Signal: [strong/medium/weak]
Emotional Signature: [recognized/challenged/relieved/provoked/other]
Operator Framing: [strong/medium/weak]
Blacklist Flags: [none/list]

THE MOMENT:
"[exact transcript of the clip]"

THE HOOK (first 3 seconds):
"[what the speaker says in the first 3 seconds]"

WHY POST:
[1-2 sentences: why this will get engagement]

SUGGESTED CAPTION:
"[hook-based caption for social media]"

FORMAT: [faceless reel type]
- Text overlay with key quote
- Podcast audio as background
- Waveform animation

HASHTAGS:
#[tag1] #[tag2] #[tag3] #[tag4] #[tag5]

SCORE: [X]/100
- Quotability: [X]/30
- Emotion: [X]/20
- Clarity: [X]/20
- Controversy: [X]/15
- Visual potential: [X]/10
- Brand alignment: [X]/15
```

### Step 6: Quality Check

Before finalizing, verify:
- [ ] Clip is 15-60 seconds
- [ ] No mid-sentence cuts
- [ ] Transcript is accurate (not hallucinated)
- [ ] URL with timestamp works
- [ ] Hook is compelling (first 3 seconds)
- [ ] Caption is scroll-stopping
- [ ] Brand Angle is identified
- [ ] Brand alignment is at least 8/15
- [ ] Truly-seen signal, emotional signature, and operator framing are documented
- [ ] First-touch feeling is specific, not generic
- [ ] GenX-written hook/caption/reasoning has zero blacklist violations

## Output
- 2-3 clip briefs per source video
- Each brief includes: timestamps, transcript, hook, caption, format suggestion
- All clips scored and ranked

## Error Handling
- If no hot zones found, report "No quotable moments in this video"
- If clip can't fit 15-60 seconds, skip and note reason
- If transcript is garbled/inaccurate, flag and skip

## Quality Checks
- [ ] Source is public or approved
- [ ] All clips have working URLs with timestamps
- [ ] All transcripts are accurate (from API, not fabricated)
- [ ] All clips are 15-60 seconds
- [ ] All clips have natural start/end points
- [ ] No fabricated content
- [ ] Transcript excerpt is short and necessary for the brief
- [ ] Brand gate passed before presenting to human approval
- [ ] Human review required before publishing
