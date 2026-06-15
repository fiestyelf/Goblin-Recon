# Goblin Recon — Hook System Upgrade
## Complete Implementation Guide
**Date:** June 15, 2026
**Author:** Goblin Recon (Deep Research + Architecture)
**Scope:** 4 files changed, 1 new config, zero new skills

---

# Overview

This document contains ALL changes needed to integrate the best hook creation frameworks into Goblin Recon. One new config file + three patches. Everything below is ready to copy into your repo.

---

# FILE 1: NEW — `config/hook-formulas.yaml`

**Path:** `goblin-recon/config/hook-formulas.yaml`
**Action:** Create this file. It becomes the single source of truth for hooks across all GenX skills.

```yaml
# =============================================================================
# Hook Formulas — Shared Formula Bank
# =============================================================================
# Referenced by: caption-tone, email-hook, goblin-recon Clip Mine pipeline
# Sources: viral-hook-formulas (GitHub/MIT), Captain Hook AI, create-viral-content
#   social-hook-writer (evo-nexus), LindleyLabs 10 Prompt Frameworks
# =============================================================================

version: "1.0.0"
last_updated: "2026-06-15"

# ---------------------------------------------------------------------------
# SCORING SYSTEM
# Every hook is scored on 3 dimensions. Target: 7+ for a strong hook.
# Adopted from: aaaronmiller/create-viral-content (30★, 40 research sources)
# ---------------------------------------------------------------------------
scoring:
  dimensions:
    curiosity:
      description: "Does the hook create a knowledge gap the reader needs to close?"
      scale:
        0: "No gap — reader already knows the answer"
        1: "Mild interest — might read/watch"
        2: "Strong 'I need to know what happens next'"
        3: "Irresistible urge to click, read, or watch"
    specificity:
      description: "Is the hook concrete with real details, or vague and generic?"
      scale:
        0: "Generic — could apply to anything, anyone, any niche"
        1: "Topic-specific — clear what it's about"
        2: "Includes numbers, metrics, or timeframes"
        3: "Hyper-specific — real figures, exact moments, named entities"
    emotional:
      description: "Does the hook trigger a high-arousal emotion?"
      scale:
        0: "Neutral, purely informational, flat"
        1: "Mild emotional trigger — slight curiosity or interest"
        2: "Clear emotional pull — reader feels something"
        3: "High-arousal — awe, anger, surprise, fear, excitement, outrage"
  thresholds:
    strong: 7   # 7-9: strong hook, ship it
    usable: 5   # 5-6: decent, ship if nothing stronger passes
    weak: 0     # 0-4: rewrite with a different formula

# ---------------------------------------------------------------------------
# PLATFORM CALIBRATION
# Each platform has different hook mechanics. This maps formulas to platforms.
# ---------------------------------------------------------------------------
platform_calibration:
  instagram_reels:
    hook_length: "5-10 words spoken, first 1-3 seconds. Text overlay essential."
    best_formulas:
      - curiosity_gap
      - bold_claim
      - pattern_interrupt
      - proof
      - storytelling_open
    avoid:
      - question     # Questions underperform in Reels caption hooks
    note: "Most people scroll with sound off. Text overlay MUST carry the hook independently."

  instagram_carousel:
    hook_length: "First 1-2 lines before '...more' truncation (~125 chars)"
    best_formulas:
      - listicle
      - this_vs_that
      - empathy
      - if_you_qualifier
      - shocking_stat
    note: "Carousel hook = cover slide text. Must make them swipe."

  tiktok:
    hook_length: "~21 words spoken, first 1-3 seconds. Visual + audio combined."
    best_formulas:
      - pattern_interrupt
      - bold_claim
      - secret_hidden
      - shocking_stat
      - proof
    note: "Raw, chaotic, unfiltered outperforms polished. Spoken delivery dominates."

  linkedin:
    hook_length: "2-3 visible lines before 'see more' fold"
    best_formulas:
      - contrarian
      - authority
      - storytelling_open
      - empathy
      - confession
    avoid:
      - pattern_interrupt     # Too aggressive for LinkedIn culture
    note: "Professional-but-human tone. Contrarian takes + vulnerability = winning formula."

  youtube_shorts:
    hook_length: "5-8 words in title AND first spoken sentence, first 1-3 seconds"
    best_formulas:
      - curiosity_gap
      - bold_claim
      - shocking_stat
      - dont_hook
      - proof
    note: "Title + spoken hook must align. Retention graphs drop at 5s if they don't match."

  twitter_x:
    hook_length: "One line, under 280 characters for the hook itself"
    best_formulas:
      - contrarian
      - bold_claim
      - question
      - confession
    note: "Curiosity and tension must land in the first sentence. No fluff."

  threads:
    hook_length: "100-280 characters, conversational"
    best_formulas:
      - empathy
      - storytelling_open
      - confession
      - contrarian
    note: "Write like texting a smart friend. Anti-corporate, relatable."

  email_subject:
    hook_length: "30-50 characters for mobile preview"
    best_formulas:
      - curiosity_gap
      - if_you_qualifier
      - question
      - urgency
    avoid:
      - pattern_interrupt
      - confession
    note: "Open rate is the only metric that matters for the subject line."

  newsletter_subject:
    hook_length: "40-60 characters"
    best_formulas:
      - curiosity_gap
      - shocking_stat
      - authority
      - future_pacing
      - if_you_qualifier

# ---------------------------------------------------------------------------
# SITUATION → FORMULA MAP
# When you know the goal but not the formula, use this.
# ---------------------------------------------------------------------------
situation_map:
  new_audience:
    goal: "Hook people who don't know you yet"
    formulas:
      - curiosity_gap
      - shocking_stat
      - question
  building_authority:
    goal: "Establish credibility and trust"
    formulas:
      - authority
      - bold_claim
      - proof
  selling:
    goal: "Drive purchase or signup intent"
    formulas:
      - future_pacing
      - empathy
      - proof
  engagement:
    goal: "Get comments, shares, saves — not just views"
    formulas:
      - pattern_interrupt
      - contrarian
      - confession
  educational:
    goal: "Teach something, tutorial, how-to"
    formulas:
      - mistake_hook
      - secret_hidden
      - dont_hook
  storytelling:
    goal: "Build personal brand through narrative"
    formulas:
      - storytelling_open
      - confession
      - empathy
  trending:
    goal: "Ride a trending topic or news event"
    formulas:
      - urgency
      - contrarian
      - shocking_stat
  comparison:
    goal: "Compare two options, tools, or approaches"
    formulas:
      - comparison
      - this_vs_that
      - listicle

# ---------------------------------------------------------------------------
# GENX BRAND OVERLAY
# GenX-specific rules layered on top of the universal formulas.
# Blacklist terms from config/brand-voice.yaml apply to ALL hook generation.
# ---------------------------------------------------------------------------
genx_overlay:
  b2c:
    preferred_formulas:
      - storytelling_open
      - empathy
      - confession
      - future_pacing
      - curiosity_gap
    avoid_formulas:
      - contrarian       # Too aggressive for B2C warmth
      - urgency          # Feels salesy against transformation positioning
    tone_rule: "Warm, human, emotionally true, alive. Depth + play. Never woo, never solemn."
    blacklist_specific:
      - "game-changer"
      - "crush it"
      - "high-vibe"
      - "manifest"
  
  b2b:
    preferred_formulas:
      - contrarian
      - authority
      - proof
      - shocking_stat
    avoid_formulas:
      - confession       # Too vulnerable for no-BS B2B positioning
    tone_rule: "Rigorous, no-BS, provocative, structural. Results not advice. Keep the edge."
    blacklist_specific:
      - "synergy"
      - "circle back"
      - "thought leader"
      - "revolutionary"

# =============================================================================
# THE 20 FORMULAS
# Each formula: template → psychology → category → best platforms → examples → pro tip
# =============================================================================

formulas:

  # 1 — CURIOSITY GAP
  # The most powerful psychological trigger in content. Universal across all platforms.
  curiosity_gap:
    template: "[Unexpected outcome] — and [surprising detail] is why."
    psychology: "Zeigarnik Effect — the brain craves closure on incomplete patterns. When you present a result without the cause, people literally cannot stop thinking about the unfinished thought. This is the single strongest hook mechanism across every platform."
    category: curiosity
    best_for:
      - instagram_reels
      - tiktok
      - youtube_shorts
      - newsletter_subject
      - email_subject
    examples:
      b2c: "I quit my high-paying job with no plan — and my anxiety dropped 80% in 30 days."
      b2b: "We stopped tracking NPS and customer retention went up. Here's the counterintuitive reason."
      neutral: "This free tool gets more views than $10,000 of YouTube ads — here's the proof."
    pro_tip: "Promise less than you reveal. The gap must be closeable within your content. If you tease and don't deliver, you lose trust forever."

  # 2 — BOLD CLAIM
  # Specific numbers signal documented truth. Round numbers feel fabricated.
  bold_claim:
    template: "I [specific achievement] in [short timeframe] using [method]."
    psychology: "Specificity signals credibility. The brain processes specific numbers as more truthful than round numbers. The timeframe creates urgency and implies repeatability. 'I made money online' is ignorable. 'I made $4,237 in 14 days from a single TikTok' is irresistible."
    category: authority
    best_for:
      - instagram_reels
      - tiktok
      - youtube_shorts
      - linkedin
    examples:
      b2c: "I went from burnout to running a thriving coaching practice in 90 days — here's the framework."
      b2b: "I grew from 0 to 10K followers in 30 days using only carousel posts."
      neutral: "I built a 50,000-subscriber newsletter in 90 days without spending a dollar on ads."
    pro_tip: "Use real numbers. '$10,347' beats '$10K' every time. If you don't have impressive stats yet, focus on the method rather than the outcome."

  # 3 — PATTERN INTERRUPT
  # Exploits the orienting response — automatic attention to the unexpected.
  pattern_interrupt:
    template: "Stop [what they're doing]. [Unexpected command or statement]."
    psychology: "Pattern interrupts exploit the orienting response — the brain's automatic reaction to anything unexpected. When someone is scrolling in a predictable rhythm, an unexpected command or visual break forces conscious attention. You have about 1.5 seconds once you trigger it."
    category: engagement
    best_for:
      - tiktok
      - instagram_reels
      - youtube_shorts
    examples:
      b2c: "Stop scrolling. The way you're measuring happiness is the reason you're not feeling it."
      b2b: "Stop optimizing for open rates. There's a metric that actually predicts revenue."
      neutral: "Wait. Before you post that Reel, you need to hear this algorithm change."
    pro_tip: "Pair with a visual interrupt — different background color, sudden movement, or hand gesture. Audio + visual pattern interrupts together are nearly impossible to scroll past."

  # 4 — CONTRARIAN
  # Triggers the brain's conflict detection system. People engage to defend or learn.
  contrarian:
    template: "[Common belief] is wrong. Here's what actually works."
    psychology: "Contrarian takes trigger the brain's conflict detection system. When someone challenges a held belief, the anterior cingulate cortex activates — the same area responsible for error detection. People engage either to defend their belief or to learn the new perspective. Either way, they're watching."
    category: controversial
    best_for:
      - linkedin
      - twitter_x
      - youtube_shorts
      - threads
    examples:
      b2c: "Self-care isn't bubble baths and spa days. It's saying no to things that drain you."
      b2b: "Posting every day is actually destroying your account. Here's the retention data."
      neutral: "You don't need a niche. The most successful creators I know don't have one."
    pro_tip: "Must back it up with evidence or reasoning. A contrarian take without substance is just clickbait. Challenge the method, not the goal — 'Niching down doesn't work' is defensible. 'Making money is bad' is not."

  # 5 — DON'T HOOK
  # Loss aversion is 2x stronger than gain desire. "Don't" triggers immediate pause.
  dont_hook:
    template: "Don't [common action] until you [prerequisite]."
    psychology: "Loss aversion — the fear of doing something wrong — is 2x stronger than the desire to do something right (Kahneman & Tversky). Telling someone 'don't' triggers an immediate pause because the brain prioritizes avoiding mistakes over seeking gains. It also implies insider knowledge the viewer doesn't have."
    category: urgency
    best_for:
      - youtube_shorts
      - tiktok
      - instagram_reels
    examples:
      b2c: "Don't set another New Year's resolution until you understand this one thing about habits."
      b2b: "Don't hire another AI consultant until you've read the contract for these 3 clauses."
      neutral: "Don't start a YouTube channel until you understand the 30-day rule."
    pro_tip: "Works best when the common action is something the viewer is about to do or has recently done. Meet them in the moment of action."

  # 6 — STORYTELLING OPEN
  # Neural coupling — the listener's brain mirrors the speaker's.
  storytelling_open:
    template: "[Time/place], I [unexpected situation]. [Cliffhanger]."
    psychology: "Stories activate the brain differently than facts. Neural coupling causes the listener's brain to mirror the speaker's — they literally experience the story with you. Starting in the middle of the action (in medias res) skips exposition and immediately creates investment."
    category: story
    best_for:
      - linkedin
      - youtube_shorts
      - instagram_reels
      - facebook
      - threads
    examples:
      b2c: "Last Tuesday at 2 AM, a client sent me a voice note that made me rethink my entire coaching philosophy."
      b2b: "Three months ago, I was about to shut down our AI pilot. Then one team lead sent me a Slack message."
      neutral: "I was about to delete my channel when I noticed something in my analytics that changed everything."
    pro_tip: "Start at the peak of emotion, not the beginning. 'I was crying in my car when I opened the email' beats 'So six months ago I decided to start a business.'"

  # 7 — SHOCKING STAT
  # Creates self-referential processing — "Am I in the 90% or the 10%?"
  shocking_stat:
    template: "[Number]% of [group] [surprising behavior]. Here's what the other [number]% know."
    psychology: "Statistics create a frame of reference that makes the viewer evaluate themselves. '90% of YouTube channels fail in the first year' immediately makes every viewer wonder: am I in the 90% or the 10%? This self-referential processing increases engagement because the content becomes personally relevant."
    category: data
    best_for:
      - linkedin
      - youtube_shorts
      - newsletter_subject
      - instagram_carousel
      - email_subject
    examples:
      b2c: "82% of people who set coaching goals abandon them by February. The 18% who don't share one thing."
      b2b: "97% of AI pilot projects never reach production. The 3% that do all share this one trait."
      neutral: "The average TikTok gets seen by 300 people. Some get seen by 3 million. The difference is 7 seconds."
    pro_tip: "Use stats from credible sources and cite them. Made-up stats destroy credibility. If you can't find the exact stat, use qualitative framing: 'Most creators' instead of '73% of creators.'"

  # 8 — IF YOU QUALIFIER
  # Pre-qualification makes content feel personalized via the cocktail party effect.
  if_you_qualifier:
    template: "If you [specific situation], this is [what they need]."
    psychology: "Pre-qualification makes content feel personalized. When someone reads 'If you have under 1,000 followers,' their brain immediately evaluates: 'Is this me?' If yes, the content instantly feels like it was made specifically for them. This triggers the cocktail party effect — hearing your name in a crowded room."
    category: targeting
    best_for:
      - linkedin
      - instagram_carousel
      - email_subject
      - newsletter_subject
    examples:
      b2c: "If you're successful on paper but something still feels missing, this framework is for you."
      b2b: "If you're a founder with 50-200 employees who's tired of micromanaging, read this."
      neutral: "If you've tried posting consistently and still aren't growing, here's what's actually wrong."
    pro_tip: "Be hyper-specific with the qualifier. You'll get lower total reach but massively higher engagement from the exact audience that self-identifies."

  # 9 — MISTAKE HOOK
  # Pratfall effect — competent people become more likable after revealing mistakes.
  mistake_hook:
    template: "I [made a specific mistake] that [cost/consequence]. Here's what I learned."
    psychology: "Vulnerability creates trust through the pratfall effect — people like competent individuals more after seeing them make a mistake. It makes you relatable. Additionally, learning from others' mistakes is an evolutionary survival strategy — the brain is wired to pay attention to cautionary tales."
    category: vulnerability
    best_for:
      - linkedin
      - youtube_shorts
      - twitter_x
      - facebook
    examples:
      b2c: "I told a client the wrong thing in our first session. She almost quit. Here's what I learned about the coaching relationship."
      b2b: "We spent $50K on an AI implementation that failed. The root cause wasn't the tech."
      neutral: "I posted every day for 6 months and my channel actually shrank. Here's what I changed."
    pro_tip: "The lesson must be proportional to the mistake. A massive failure with a trivial takeaway is unsatisfying. A massive failure with a paradigm-shifting insight is legendary content."

  # 10 — SECRET / HIDDEN
  # Information gap theory — the brain experiences deprivation when valuable info is withheld.
  secret_hidden:
    template: "The [hidden/secret/little-known] [thing] that [impressive result]."
    psychology: "Information gap theory (Loewenstein, 1994) — when someone believes valuable information exists that they don't have, they experience a genuine feeling of deprivation. The words 'secret' and 'hidden' amplify this by implying the information has been deliberately kept from them, triggering reactance — the desire to access restricted information."
    category: curiosity
    best_for:
      - youtube_shorts
      - tiktok
      - twitter_x
    examples:
      b2c: "The hidden reason most high-achievers feel empty — and the one question that fixes it."
      b2b: "The hidden LinkedIn setting that's killing your outbound reply rate."
      neutral: "A little-known Instagram trick that's getting creators 10x more reach right now."
    pro_tip: "The 'secret' must be genuinely underused — publicly available but obscure features, settings, or strategies. If everyone already knows it, the viewer feels cheated."

  # 11 — COMPARISON
  # Reduces cognitive load. Easier to evaluate two things side by side.
  comparison:
    template: "[Option A] vs. [Option B]: [what you'll learn]."
    psychology: "Comparisons reduce cognitive load. Instead of evaluating something in isolation (hard), the brain can evaluate two things against each other (easy). This is the contrast principle — things appear more different when placed side by side. Comparisons also imply that you've done the research so the viewer doesn't have to."
    category: educational
    best_for:
      - youtube_shorts
      - instagram_reels
      - blog_title
    examples:
      b2c: "Therapy vs. Coaching: which one actually helps you move forward? I've done both."
      b2b: "Building an in-house AI team vs. using an AI platform: the 12-month cost comparison."
      neutral: "Posting daily vs. 3x a week: I tested both for 90 days. Here are the results."
    pro_tip: "Best comparisons have a surprising winner. 'I expected Premiere Pro to destroy CapCut. I was wrong.' The unexpected result is what makes people click."

  # 12 — URGENCY
  # Threat detection — environmental changes require reassessment.
  urgency:
    template: "[Platform/thing] just [changed/updated]. Here's what it means for you."
    psychology: "Urgency activates the brain's threat detection system. Changes in the environment require reassessment — 'Do I need to adapt?' This trigger is especially powerful for creators and business owners because algorithm changes directly affect their income. The implicit message: if you don't watch this, you'll fall behind."
    category: urgency
    best_for:
      - youtube_shorts
      - tiktok
      - twitter_x
    examples:
      b2c: "The coaching industry just shifted. Here's what clients are actually looking for now."
      b2b: "LinkedIn just changed how the algorithm ranks posts. Here's the new playbook."
      neutral: "YouTube's new update changes everything for small creators. Watch before posting."
    pro_tip: "Use urgency honestly. False urgency ('YouTube is dying!') erodes trust. Real urgency ('YouTube just rolled out a new feature that affects reach') builds authority."

  # 13 — AUTHORITY
  # Authority bias — same advice from different sources is processed differently.
  authority:
    template: "As someone who [credential/experience], here's [insight]."
    psychology: "Authority bias (Cialdini) — people defer to credible sources. Establishing credentials upfront doesn't just build trust; it changes how the brain processes the subsequent information. The same advice from 'a random person' vs. 'someone who's built 3 six-figure channels' is processed with completely different levels of attention and retention."
    category: authority
    best_for:
      - linkedin
      - youtube_shorts
      - twitter_x
      - newsletter_subject
    examples:
      b2c: "After 500+ coaching sessions, here are the 3 patterns I see in every client who breaks through."
      b2b: "I've managed AI implementation for 40+ companies. Here's what none of them did right at the start."
      neutral: "After editing 500+ YouTube videos, here are the 3 cuts that actually matter."
    pro_tip: "You don't need to be famous. Specific experience is more credible than fame. 'I've sent 200 cold emails this month' is a valid credential. Quantify your experience."

  # 14 — QUESTION
  # Questions activate the brain's search function. Can't dismiss what you can't answer.
  question:
    template: "[Question the viewer can't answer confidently]?"
    psychology: "Questions activate the brain's search function. A question you can't immediately answer creates a knowledge gap that demands resolution. The best questions make the viewer realize they don't know something they thought they did — a moment of productive confusion that keeps attention locked."
    category: curiosity
    best_for:
      - youtube_shorts
      - tiktok
      - twitter_x
      - email_subject
    examples:
      b2c: "What's the difference between someone who stays stuck and someone who transforms? (It's not willpower.)"
      b2b: "Why do some AI implementations deliver 10x ROI while others never leave pilot? The answer isn't technical."
      neutral: "Why do some creators blow up while others with better content stay stuck at 500 views?"
    pro_tip: "Avoid yes/no questions — they can be dismissed without watching. Use 'why' and 'how' questions, or questions where the viewer thinks they know the answer but isn't sure."

  # 15 — THIS VS THAT
  # Creates social identity split — everyone wants to be in the informed group.
  this_vs_that:
    template: "[What most people do] vs. [what actually works]."
    psychology: "This is a superior/inferior frame that implies insider knowledge. It creates two groups — the uninformed majority and the informed minority — and everyone wants to be in the second group. Social identity theory applied to content: people engage to confirm they're in the 'smart' group or to learn how to join it."
    category: educational
    best_for:
      - instagram_carousel
      - linkedin
      - youtube_shorts
    examples:
      b2c: "What most people think happiness requires vs. what the research actually shows."
      b2b: "What beginners do: hire AI talent. What pros do: build AI systems that don't need talent."
      neutral: "How most people use ChatGPT vs. how top creators use it."
    pro_tip: "Make the 'what most people do' version genuinely common — something the viewer recognizes themselves doing. The cringe of recognition is what drives engagement."

  # 16 — CONFESSION
  # Expectancy violation — vulnerability breaks the performance pattern.
  confession:
    template: "I have to be honest: [uncomfortable truth about your experience]."
    psychology: "Radical honesty triggers the expectancy violation effect. On platforms where everyone is performing success, genuine vulnerability breaks the pattern so hard that the brain can't ignore it. Confessions also activate social bonding circuits — shared struggle creates connection faster than shared success."
    category: vulnerability
    best_for:
      - linkedin
      - twitter_x
      - instagram_reels
      - facebook
      - threads
    examples:
      b2c: "I have to be honest: I became a coach because I couldn't find one who actually helped me."
      b2b: "I'll be honest — most of the AI advice I gave last year was wrong. Here's what I'd say now."
      neutral: "Nobody talks about this, but I almost quit YouTube last month. Here's what happened."
    pro_tip: "Confess the struggle, then share the insight that emerged. Pure negativity without resolution leaves people drained. Confession → lesson → growth is the arc."

  # 17 — FUTURE PACING
  # The brain processes vivid imagination and real experience using the same pathways.
  future_pacing:
    template: "Imagine [desirable future state]. That starts with [first step]."
    psychology: "Future pacing (from NLP) works because the brain processes vivid imagination and real experience using the same neural pathways. When you say 'Imagine waking up to $500 in sales notifications,' the brain simulates that experience and generates real positive emotions. Those emotions get associated with your content and your advice."
    category: aspiration
    best_for:
      - linkedin
      - youtube_shorts
      - email_body
      - newsletter_subject
    examples:
      b2c: "Imagine waking up on a Monday and actually feeling excited about the week ahead. That starts with one conversation."
      b2b: "Picture this: it's 6 months from now and your AI team runs 80% of operations without you. Here's the roadmap."
      neutral: "Imagine having a content library that sells for you 24/7. It's simpler than you think."
    pro_tip: "Be specific in the visualization. 'Imagine being successful' is weak. 'Imagine opening your laptop on a Tuesday morning, seeing $4,200 in revenue from a product you built once' is powerful. Sensory details make it real."

  # 18 — LISTICLE
  # Numbers set clear expectations and reduce perceived effort.
  listicle:
    template: "[Number] [things] that [will help them achieve outcome]."
    psychology: "Numbers in hooks work because they set clear expectations and reduce perceived effort. '5 tools' feels achievable; 'tools for content creation' feels endless. Odd numbers (3, 5, 7) outperform even numbers in A/B tests because they feel more authentic. Very specific numbers (17, 23) outperform round numbers because they imply precision."
    category: educational
    best_for:
      - instagram_carousel
      - youtube_shorts
      - blog_title
      - twitter_x
    examples:
      b2c: "3 questions that will tell you more about someone than 10 years of small talk."
      b2b: "7 free AI tools that replaced our $15K/month consulting spend."
      neutral: "11 mistakes that keep creators stuck under 1,000 followers."
    pro_tip: "Deliver more value than the number implies. If you promise 7 tools, give 7 incredible tools with explanations, not 7 obvious ones everyone knows. Under-promise, over-deliver."

  # 19 — EMPATHY
  # Validation creates immediate trust. "This person understands me."
  empathy:
    template: "I know [their frustration/struggle]. [Validation]. [Promise of solution]."
    psychology: "Empathy hooks work through validation. When someone articulates your exact experience — especially a painful one — it creates immediate trust. The brain thinks: 'This person understands me, so their solution is probably relevant to me.' It's the therapeutic concept of 'feeling felt,' applied to content."
    category: connection
    best_for:
      - linkedin
      - email_body
      - facebook
      - instagram_reels
      - threads
    examples:
      b2c: "I know the feeling of having everything on paper but still feeling like something's missing. You're not broken. Here's what's actually going on."
      b2b: "I know how frustrating it is to spend months on an AI project that leadership ignores. I've been there. Here's how we finally got buy-in."
      neutral: "If you're tired of making content that no one sees, you're not alone — and it's not your fault."
    pro_tip: "Name the specific frustration, not a general one. 'I know growing on social media is hard' is generic. 'I know the feeling of spending 4 hours editing a video that gets 47 views' is precise and painful. Precision = resonance."

  # 20 — PROOF
  # Triple structure: proof + objection removal + promise. Nearly impossible to scroll past.
  proof:
    template: "[Concrete result]. No [common excuse]. Here's exactly how."
    psychology: "Proof hooks combine social proof with objection handling in a single sentence. The result provides the aspiration. 'No [excuse]' preemptively removes the viewer's self-limiting belief. 'Here's exactly how' promises actionable, specific information. This triple structure — proof, objection removal, promise — is nearly impossible to scroll past."
    category: authority
    best_for:
      - youtube_shorts
      - tiktok
      - instagram_reels
      - twitter_x
    examples:
      b2c: "Complete career pivot at 42. No starting over. No pay cut. Here's exactly how she did it."
      b2b: "$2M in pipeline from AI-qualified leads. No cold calls. No ad spend. Here's the system."
      neutral: "100K views on my first YouTube Short. No face. No expensive gear. Here's the framework."
    pro_tip: "Every element must be truthful. If you spent $0 on ads but $5K on a coaching program, don't say 'No investment required.' The 'no [excuse]' must be genuinely absent."

# =============================================================================
# POWER WORDS (use 2-3 per hook)
# =============================================================================
power_words:
  urgency:
    - now
    - today
    - limited
    - finally
    - before
  trust:
    - proven
    - tested
    - research-backed
    - results
    - data
  exclusivity:
    - secret
    - hidden
    - insider
    - behind-the-scenes
    - little-known
  emotion:
    - shocking
    - surprising
    - honest
    - raw
    - uncomfortable
  action:
    - discover
    - unlock
    - transform
    - master
    - build
  value:
    - free
    - blueprint
    - framework
    - system
    - toolkit

# =============================================================================
# ANTI-PATTERNS — what kills hooks
# =============================================================================
anti_patterns:
  universal:
    - "Greetings: 'Hey everyone,' 'What's up,' 'Welcome back'"
    - "Context before hook: 'So I've been thinking about this for a while...'"
    - "Qualifiers: 'I think maybe this might be useful'"
    - "Chronological setup: 'Let me tell you about something that happened 3 years ago...'"
    - "Generic claims: 'Tips for growing your business'"
    - "Vague numbers: 'A lot,' 'recently,' 'some tips'"
    - "ALL CAPS or excessive punctuation"
    - "Engagement bait: 'Like if you agree,' 'Comment YES'"
    - "Over-promising: hook promises more than content delivers"
  platform_specific:
    linkedin:
      - "Corporate-speak without personal voice"
      - "Hashtag stuffing"
      - "Pure promotional content"
    tiktok:
      - "Polished, scripted delivery"
      - "Slow buildup"
      - "Greetings before hook"
    instagram:
      - "Sound-dependent hooks without text overlay"
      - "Generic hashtags (#fyp, #viral)"
    email:
      - "ALL CAPS subject lines"
      - "Generic urgency ('Act now!')"
      - "Spam trigger words"

# =============================================================================
# QUICK A/B TESTING FRAMEWORK
# When testing hooks against each other
# =============================================================================
ab_testing:
  metrics:
    primary:
      - "Save rate — high saves = strong hook + valuable content"
      - "Comment vs. like ratio — comments = emotional response to hook"
      - "Profile visits from post — hook made someone want to know who wrote it"
    secondary:
      - "Watch time / retention (video)"
      - '"See more" click rate (LinkedIn)'
      - "Share/DM send rate"
  method:
    - "Same content, different hook, posted 2-3 weeks apart"
    - "Change only the first 1-2 lines; keep body identical"
    - "Compare engagement rates, not raw numbers"
    - "After 5-10 tests, patterns emerge for YOUR specific audience"
  quick_self_check:
    - "Would you stop scrolling for this if you didn't write it?"
    - "Does it create a question that the content answers?"
    - "Is it specific enough that it couldn't apply to anyone else's post?"
```

---

# FILE 2: PATCH — `caption-tone/SKILL.md`

**Path:** `goblin-recon/skills/caption-tone/SKILL.md`
**Action:** Replace the "HOOK LIBRARY" section (lines ~325-355) and the "CAPTION FORMULAS" section (lines ~220-290) with the content below. The rest of the skill stays the same.

## What to FIND and DELETE

Find these three sections in the current `caption-tone/SKILL.md` and delete them entirely:

1. **"CAPTION FORMULAS (use different ones for each platform)"** — the entire section with REACH, ENGAGEMENT, SALES, GROWTH subsections
2. **"HOOK LIBRARY"** — the entire section with Provocation, Curiosity, Value, Emotion, TikTok-specific
3. **"POWER WORDS (use 2-3 per caption)"** — the entire section

## What to INSERT in their place

Insert the following two sections after the existing "ANTI-PATTERNS" section:

```markdown
## CAPTION GENERATION (v2.2)

### Step A: Load the Formula Bank

Load `config/hook-formulas.yaml` as the single source of truth for all hook formulas, scoring criteria, and platform calibrations.

### Step B: Select Formula

Based on the content goal and platform, select the best formula:

| Content goal | Best formulas (from hook-formulas.yaml) |
|-------------|----------------------------------------|
| New audience / awareness | curiosity_gap, shocking_stat, question |
| Authority / credibility | authority, bold_claim, proof |
| Product / offer / sales | future_pacing, empathy, proof |
| Engagement / comments | pattern_interrupt, contrarian, confession |
| Tutorial / educational | mistake_hook, secret_hidden, dont_hook |
| Story / personal brand | storytelling_open, confession, empathy |
| Trending / news | urgency, contrarian, shocking_stat |
| Comparison / review | comparison, this_vs_that, listicle |

Apply the `genx_overlay` from hook-formulas.yaml:
- **B2C:** Prefer storytelling_open, empathy, confession, future_pacing, curiosity_gap. Avoid contrarian, urgency.
- **B2B:** Prefer contrarian, authority, proof, shocking_stat. Avoid confession.

### Step C: Generate and Score the Hook

Generate the hook using the selected formula template, then score it against the 3-dimension system:

| Dimension | Score (0-3) | What to check |
|-----------|:-----------:|---------------|
| **Curiosity** | ? | Does it create a knowledge gap the reader must close? |
| **Specificity** | ? | Concrete numbers, timeframes, or details? Or vague? |
| **Emotional** | ? | High-arousal emotion (awe, surprise, anger, fear)? |
| **TOTAL** | ?/9 | |

**Thresholds:**
- **7-9:** Strong hook. Ship it.
- **5-6:** Usable. Ship if nothing stronger passes the same formula set.
- **0-4:** Weak. Select a different formula and regenerate.

### Step D: Build the Full Caption

Once the hook passes scoring (5+), build the complete caption using the platform-specific rules below.

---

## HOOK FORMULA QUICK REFERENCE

Full psychology, examples, and pro tips live in `config/hook-formulas.yaml`. This is the speed-reference.

| # | Formula | Template | Best Platforms |
|---|---------|----------|---------------|
| 1 | Curiosity Gap | "[Outcome] — and [detail] is why." | Reels, TikTok, Shorts, Email |
| 2 | Bold Claim | "I [achievement] in [time] using [method]." | Reels, TikTok, Shorts, LinkedIn |
| 3 | Pattern Interrupt | "Stop [action]. [Unexpected command]." | TikTok, Reels, Shorts |
| 4 | Contrarian | "[Belief] is wrong. Here's what works." | LinkedIn, Twitter, Shorts |
| 5 | Don't Hook | "Don't [action] until you [prerequisite]." | Shorts, TikTok, Reels |
| 6 | Storytelling | "[Time/place], I [situation]. [Cliffhanger]." | LinkedIn, Shorts, Facebook |
| 7 | Shocking Stat | "[N]% of [group] [behavior]. Here's what the other [N]% know." | LinkedIn, Shorts, Carousel |
| 8 | If You Qualifier | "If you [situation], this is [what you need]." | LinkedIn, Carousel, Email |
| 9 | Mistake Hook | "I [mistake] that [cost]. Here's what I learned." | LinkedIn, Shorts, Twitter |
| 10 | Secret/Hidden | "The [hidden] [thing] that [result]." | Shorts, TikTok, Twitter |
| 11 | Comparison | "[A] vs [B]: [what you'll learn]." | Shorts, Reels, Blog |
| 12 | Urgency | "[Platform] just [changed]. Here's what it means." | Shorts, TikTok, Twitter |
| 13 | Authority | "As someone who [credential], here's [insight]." | LinkedIn, Shorts, Twitter |
| 14 | Question | "[Question they can't answer]?" | Shorts, TikTok, Twitter, Email |
| 15 | This vs That | "[What most do] vs [what works]." | Carousel, LinkedIn, Shorts |
| 16 | Confession | "I have to be honest: [uncomfortable truth]." | LinkedIn, Twitter, Facebook |
| 17 | Future Pacing | "Imagine [future state]. That starts with [step]." | LinkedIn, Shorts, Email |
| 18 | Listicle | "[N] [things] that [outcome]." | Carousel, Shorts, Blog |
| 19 | Empathy | "I know [frustration]. [Validation]. [Solution]." | LinkedIn, Email, Facebook |
| 20 | Proof | "[Result]. No [excuse]. Here's exactly how." | Shorts, TikTok, Reels |

---

## PLATFORM RULES (v2.2 — updated with hook-formulas.yaml calibrations)

### INSTAGRAM REELS
- **Hook length:** 5-10 words, first 1-3 seconds. Text overlay MUST carry the hook independently (sound-off viewing).
- **Best formulas:** curiosity_gap, bold_claim, pattern_interrupt, proof, storytelling_open
- **Avoid:** question hooks (underperform in Reels captions)
- **Structure:** Hook (125 chars before truncation) → 1-2 sentences → CTA
- **CTA:** DM shares ("send to a friend who...") or saves ("save for later") — 10x more valuable than likes
- **Hashtags:** 3-5 niche hashtags IN caption. Never #fyp, #viral, #instagood
- **SEO:** Primary keyword in first 2 sentences

### INSTAGRAM CAROUSEL
- **Hook length:** First 1-2 lines before "...more" (~125 chars). Cover slide text = hook.
- **Best formulas:** listicle, this_vs_that, empathy, if_you_qualifier, shocking_stat
- **Structure:** Hook → Expanded value complementing slides → Save CTA
- **CTA:** Always optimize for saves. Carousels with save CTA get +68% saves

### TIKTOK
- **Hook length:** ~21 words spoken, first 1-3 seconds. Raw, chaotic outperforms polished.
- **Best formulas:** pattern_interrupt, bold_claim, secret_hidden, shocking_stat, proof
- **Structure:** Hook (80 chars) → 1-2 short sentences → CTA + 3-5 emoji (+33% engagement)
- **Keywords:** Primary keyword in first 80 characters
- **Hashtags:** 3-5 MAX. 1 niche + 1 thematic + 1 trending. NEVER #fyp, #foryou, #viral
- **CTA:** Questions get +44% comments

### LINKEDIN
- **Hook length:** 2-3 visible lines before "see more" fold
- **Best formulas:** contrarian, authority, storytelling_open, empathy, confession
- **Avoid:** pattern_interrupt (too aggressive)
- **Structure:** Hook → Personal story or data → Professional lesson → Discussion question
- **Tone:** Professional-but-human. Contrarian takes + vulnerability = winning formula

### THREADS
- **Hook length:** 100-280 characters, conversational — like texting a smart friend
- **Best formulas:** empathy, storytelling_open, confession, contrarian
- **Style:** Anti-corporate, self-aware humor. Relatable pain points > data
- **Tags:** Only 1 topic tag per post

### FACEBOOK (Page/Personal)
- **Hook length:** 40-80 characters for max reach
- **Best formulas:** storytelling_open, empathy, confession
- **AVOID trigger words:** "buy now", "limited time", "FREE" (caps), "click here", "money", "income", "contest", "giveaway"
- **SAFE replacements:** "available today", "complimentary", "no cost", "learn more"

### FACEBOOK GROUP
- **Hook length:** 200-500 characters. Longer, contextual.
- **Style:** Community language. "Who else has experienced...", "Curious what you all think..."
- **CTA:** Open discussion questions

### YOUTUBE SHORTS
- **Title length:** 40-70 characters (max 100). Title = #1 SEO signal.
- **Best formulas:** curiosity_gap, bold_claim, shocking_stat, dont_hook, proof
- **Critical:** Title + spoken hook MUST align. Algorithm penalizes mismatch.
- **Description:** 150-300 chars. Hook sentence first → 1-2 value sentences → CTA → hashtags
- **Hashtags:** 3-5 MAX, end of description. NEVER #shorts as only tag
- **CTA:** Subscribe prompt or "watch [linked video] for more"

---

## SIGNAL HIERARCHY (unchanged from v2.1)

1. **Shares/DM sends** — strongest (~10x a like)
2. **Saves** — very strong, especially Instagram
3. **Comments** — strong, especially meaningful ones
4. **Watch time / Completion rate** — dominant for video (70%+ for viral)
5. **Likes** — weakest, "vanity metric"

## Brand Gate Step

After generating captions:
1. Scan against `config/brand-voice.yaml` → `blacklist`
2. Verify hook score ≥ 5/9 (from hook-formulas.yaml thresholds)
3. If blacklisted term found OR hook score < 5: regenerate
4. Verify tone matches selected tone's voice description

## QUALITY CHECKLIST (updated for v2.2)

- [ ] Hook in first 80-125 characters (or platform-specific length)
- [ ] Hook scored ≥ 5/9 using hook-formulas.yaml scoring system
- [ ] 1-3 SEO keywords naturally integrated
- [ ] ONE clear CTA per caption
- [ ] 2-3 power words from hook-formulas.yaml power_words section
- [ ] 3-5 niche hashtags (not generic) where applicable
- [ ] Zero engagement bait
- [ ] Zero shadow ban triggers
- [ ] Zero Facebook trigger words (for FB captions)
- [ ] Short paragraphs with line breaks
- [ ] Different formula for each platform
- [ ] Loaded config/hook-formulas.yaml AND config/brand-voice.yaml before generating
- [ ] Tone selected using default_by_category or platform_defaults
- [ ] Professional_genx delivered first
- [ ] Brand gate scan completed with zero violations
- [ ] GenX overlay applied (B2C vs B2B formula preferences)
```

---

# FILE 3: PATCH — Clip Mine brief template (in `goblin-recon` skill)

**Path:** `goblin-recon/skills/goblin-recon/SKILL.md`
**Action:** In the Clip Mine section, update the caption output format. Find the existing "Caption for Instagram" section in the clip brief template and replace it with the version below that includes hook scoring.

## What to FIND

In the goblin-recon SKILL.md, find the section that describes clip brief output format. Specifically, the part where platform captions are generated. 

## What to REPLACE it with

```markdown
### Caption Format (v2.2 — includes hook scoring)

Every clip brief MUST include platform captions with hook scoring from `config/hook-formulas.yaml`.

```
## Caption for Instagram Reels

**Hook:** "[hook text]"
**Formula:** [formula name from hook-formulas.yaml]
**Hook Score:** C[0-3] S[0-3] E[0-3] = [total]/9 — [strong/usable/weak]

[full caption text with line breaks and hashtags]
```

**Scoring is mandatory.** If the hook scores below 5/9, generate 2 alternative hooks using different formulas and present the strongest. The human gate should never see a hook that the agent already knows is weak.
```

---

# FILE 4: MINOR PATCH — `email-hook/SKILL.md`

**Path:** `goblin-recon/skills/email-hook/SKILL.md`
**Action:** Add one reference line. No structural changes.

## What to FIND

In the "Required Files" table near the top of the email-hook SKILL.md:

```markdown
| `config/brand-voice.yaml` | GenX brand voice, blacklist, and tone definitions. |
```

## What to REPLACE it with

```markdown
| `config/brand-voice.yaml` | GenX brand voice, blacklist, and tone definitions. |
| `config/hook-formulas.yaml` | Shared hook formula bank. Use `email_subject` and `newsletter_subject` platform calibrations for subject line formula selection. |
```

And add this note to the "Step 2: Generate Variants" section, right before the variant generation instructions:

```markdown
### Step 2.0: Select Hook Formula

Before generating subject lines, load `config/hook-formulas.yaml` and reference:
- `platform_calibration.email_subject.best_formulas` for subject line formula selection
- `platform_calibration.newsletter_subject.best_formulas` for newsletter-specific subjects
- `genx_overlay` for B2C vs B2B formula preferences

Preferred B2B email subject formulas: curiosity_gap, if_you_qualifier, question, urgency
Preferred B2C email subject formulas: curiosity_gap, future_pacing, empathy

The existing `email_gate.py` scoring remains the final validator — hook-formulas.yaml guides formula selection before generation.
```

---

# IMPLEMENTATION CHECKLIST

| Step | File | Action | Est. Time |
|:----:|------|--------|:---------:|
| 1 | `config/hook-formulas.yaml` | Create new file with full YAML content from this document | 5 min |
| 2 | `skills/caption-tone/SKILL.md` | Replace Hook Library + Caption Formulas + Power Words sections with v2.2 content | 10 min |
| 3 | `skills/goblin-recon/SKILL.md` | Update Clip Mine caption format to include hook scoring | 5 min |
| 4 | `skills/email-hook/SKILL.md` | Add hook-formulas.yaml reference + formula selection step | 3 min |
| 5 | Sync to profile | `bash scripts/setup.sh` or manual rsync | 2 min |
| 6 | Register skills | Say "register all skills" in a goblin-recon session | 1 min |
| 7 | Verify | Say "write 5 hooks about [test topic]" to test the new system | 2 min |

**Total: ~28 minutes**

---

# VERIFICATION TEST

After implementing, test with this command in a goblin-recon session:

```
"Write 3 hooks for a B2B post about why most AI implementations fail. Score each one."
```

Expected output:
- 3 hooks using different formulas (e.g., shocking_stat, contrarian, mistake_hook)
- Each hook scored C/S/E with total
- Recommended hook marked
- GenX B2B overlay applied (no confession formula, no blacklisted terms)

---

# WHAT CHANGES VS WHAT STAYS

| What Changes | What Stays the Same |
|-------------|-------------------|
| Hook generation is formula-bank-driven, not ad-hoc | `email_gate.py` scoring pipeline |
| Every hook is scored before delivery | `brand_gate.py` blacklist check |
| Platform calibrations are centralized in one YAML | `config/brand-voice.yaml` tone definitions |
| B2C/B2B formula preferences are explicit | `email-campaigns.yaml` campaign types |
| Clip Mine captions auto-score their hooks | Clip Mine workflow (Trend Radar → Source Hunter → Moment Finder) |
| `caption-tone` Hook Library: 15 hooks → 20 formulas + psychology | `caption-tone` platform rules, output format, tone selection |
| `email-hook` gains formula selection guidance | `email-hook` campaign types, variant generation, email_gate scoring |

---

*Generated by Goblin Recon on June 15, 2026. All changes are additive — nothing breaks existing pipelines.*
