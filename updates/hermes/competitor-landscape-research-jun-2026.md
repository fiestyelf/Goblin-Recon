# Competitive Intelligence Landscape — Research Notes

> June 15, 2026 — Goblin Recon competitor-scout v2.0 research sprint.
> 7 open-source repos analyzed for patterns, techniques, and architectures.

---

## Repos Analyzed

### 1. drift (getdrift/drift) — ⭐ Closest Match

**URL:** https://github.com/getdrift/drift
**Stack:** Next.js 16 + libSQL + Gemini 2.5 Flash + Cheerio
**License:** MIT | **Stars:** 0 (brand new, May 2026)

**What it does:**
Weekly competitive intel for B2B SaaS. Scrapes pricing, changelog, blog, jobs, docs, homepage. Diffs snapshots week-over-week, uses Gemini to write a brief. Delivers via email/Slack/Discord/webhook.

**Key techniques we adapted:**
- **Content-hash dedup:** SHA256 hash per page — only stores actual diffs as history compounds. SQLite stays lean.
- **JSON-island extraction:** `__NEXT_DATA__`, Remix context, Apollo hydration, ld+json — walks hydration JSON for string values. Without this, Linear's changelog scrapes to ~zero useful content; with it, ~55KB.
- **Source types:** `--kind=pricing|changelog|blog|jobs|docs|homepage|about|other` — each URL has a type that determines how it's processed.
- **Structured LLM output:** `responseSchema` forces Gemini to return JSON matching the digest shape. No prompt-only adherence required.
- **Digest shape:** `summary`, `key_changes`, `strategic_signals`, `recommended_actions`, `urgency` rating.
- **Zero-cost stack:** Free Gemini tier (1,500 req/day) + self-host on any machine + SQLite file storage. Entire thing runs without paying anyone.

**Architecture:**
```
src/lib/
  db.ts            node:sqlite + schema migrations
  scraper.ts       fetch + cheerio → visible DOM + JSON-island content + sha256 hash
  synthesizer.ts   Gemini 2.5 Flash with structured output
  notify.ts        slack/discord/generic webhooks + resend email
  digest.ts        orchestration: fetch → snapshot → synthesize → store → deliver
```

**CLI:**
```
drift add <name> <domain>
drift source <competitor> <url> [--kind=...] [--label=...]
drift fetch [competitor]
drift digest <competitor> [--days=7]
```

---

### 2. ScopeHound (ZeroLupo/scopehound) — ⭐ Marketing-First

**URL:** https://github.com/ZeroLupo/scopehound
**Stack:** Cloudflare Workers + Workers AI (free) or Anthropic Claude + Cloudflare KV
**License:** MIT | **Stars:** 2

**What it does:**
AI-powered competitive intelligence for marketing teams. Monitors competitor pricing, features, SEO, blogs, and Product Hunt launches. Delivers prioritized, AI-analyzed alerts to Slack.

**Key techniques we adapted:**
- **Change priority scoring:** Every change gets HIGH/MEDIUM/LOW rating + impact analysis + recommended action.
- **"All clear" message:** Daily "all clear" Slack message when no changes detected. Prevents alert fatigue.
- **Competitor auto-discovery:** Weekly AI-powered suggestions for new competitors via DuckDuckGo/Brave Search. Seed competitor support (provide 2 known for better niche results).
- **Slack commands:** `/scopehound scan`, `/scopehound add <url>`, `/scopehound status`, `/scopehound ads <company>` — interactive competitor management from Slack.
- **Meta ad library integration:** `/ads` command surfaces Meta ad library data for any competitor.
- **SEO tracking:** Title tags, meta descriptions, OG tags, H1 changes.
- **Blog & RSS monitoring:** AI classification of blog posts (funding, partnerships, product launches).

**Cost:** $0 on Cloudflare free tier for ~25 competitors. Optional Anthropic API (~$0.10/day for 10 competitors).

**Architecture:**
Single-file Cloudflare Worker. No build step. No dependencies.
```
workers/src/
  ai.js, auth.js, billing.js, browser.js, config.js, context.js,
  discovery.js, scanner.js, slack.js, state.js, templates.js, utils.js
  routes/api.js, routes/pages.js, routes/scheduled.js, routes/slack-commands.js
```

---

### 3. competitor-monitor (Keerthivasan-Venkitajalam) — ⭐ Semantic Diffing

**URL:** https://github.com/Keerthivasan-Venkitajalam/competitor-monitor
**Stack:** Python 3.10+ + Playwright + sentence-transformers + Pydantic v2
**License:** Apache 2.0 | **Stars:** 3

**What it does:**
AI-powered autonomous competitive intelligence for indie hackers and solo founders. Uses semantic embeddings to detect real strategic shifts — not typo fixes. 150+ hours saved per year.

**Key techniques we adapted:**
- **Semantic diffing (the core innovation):**
  1. Extract text from competitor websites using Playwright
  2. Generate 768-dimensional embeddings using sentence-transformers (all-MiniLM-L6-v2)
  3. Calculate cosine similarity vs. historical baseline
  4. Flag changes < 80% similarity as "Strategic Shift"
- **Noise categories that get ignored:** Typo fixes, date updates, rotating testimonials, footer changes
- **Signal categories that get flagged:** Pricing model changes, feature launches, positioning pivots, messaging updates
- **Privacy-first:** All processing runs locally. No data sent to external servers. Optional local LLM (Ollama/LM Studio).
- **Tunable threshold:** `STRATEGIC_SHIFT_THRESHOLD = 0.80` (adjustable — 0.85 = more sensitive, 0.75 = only major changes)

**Our adaptation:** We use LLM-prompt semantic diffing instead of embeddings — same principle, zero dependencies.

**Impact metrics they claim:**
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Time per check | 45 min | 2 min | 95.6% reduction |
| Competitors monitored | 3 | 5+ | 67% increase |
| Strategic shifts detected | ~20% | ~95% | 4.75x better |

---

### 4. Telnyx Competitor Monitor (team-telnyx) — ⭐ Sitemap Discovery

**URL:** https://github.com/team-telnyx/Competitor-Monitor
**Stack:** Python + TypeScript + OpenAI + SQLite + Next.js dashboard
**License:** Proprietary | **Stars:** 0

**What it does:**
Daily automated monitoring of 12 AI/voice competitors. Fetches sitemaps, detects new pages via lastmod or snapshot diffs, LLM classifies by focus area, generates executive digest.

**Key techniques we adapted:**
- **Sitemap auto-discovery:** Fetches competitor sitemaps and detects new pages via `lastmod` or snapshot diffs. Also handles Atom/RSS feeds as sitemap alternatives.
- **Atom/RSS feed support:** `fetch_sitemap()` detects `<feed>` (Atom) and `<rss>` roots, normalizes entries to `{url, lastmod}`. Modal publishes no sitemap.xml — found via blog Atom feed (113 entries).
- **Structured relevance scoring:** 0-100 score + signal_type against a versioned rubric. Threshold 40. Relevance = score >= threshold.
- **Product category taxonomy:** Per-competitor product registry with canonicalization. Maps competitor features to your own product categories.
- **Training/feedback loop:** Queue mirrors feed, per-page feedback with immediate correction. Operator guidance (global/per-competitor).
- **Multi-inference provider:** OpenAI API + ChatGPT-OAuth (Codex) — classification runs on ChatGPT subscription with no API credits.

**Competitors tracked (12):**
Voice AI: Vapi, ElevenLabs, Retell AI, Bland AI | Transcription: AssemblyAI | Platform: Twilio | AI Inference: Together AI, Baseten, Fireworks AI, RunPod, Modal, Replicate

**Pipeline:**
```
Sitemap fetch → New page detection → Scrape → LLM classify → LLM digest → Slack/email
```

---

### 5. RivalEye (Bharath-code/rivaleye) — ⭐ Full SaaS

**URL:** https://github.com/Bharath-code/rivaleye
**Stack:** Next.js 16 + React 19 + Tailwind CSS 4 + Supabase + Gemini Vision + Trigger.dev
**License:** Proprietary | **Stars:** 0

**What it does:**
Full SaaS competitive intelligence platform. Monitors pricing, tech stack, and branding across 4 global regions.

**Notable features (not adapted — overkill for our use case):**
- **Geo-aware pricing monitoring:** US, EU, India, Global — detects regional discounts and hidden pricing strategies.
- **Tech stack detection:** Alerts when competitors add Stripe, switch to Next.js, adopt new analytics (Wappalyzer-style).
- **Branding analysis:** Catches color, font, and logo changes that signal repositioning. Uses Gemini Vision on screenshots.
- **Core Web Vitals tracking:** Track competitor performance and capitalize on UX gaps.
- **3-scraper fallback chain:** Firecrawl → Playwright → Cheerio.
- **AI Tactical Briefs:** Every change comes with what happened, why it matters, and what to do next.

**Architecture:**
```
src/lib/
  ai/        Vision analyzer, insight generator, AI provider
  alerts/    Email, Slack, branding/tech/performance alerts
  crawler/   Firecrawl, Playwright, Cheerio, geo-proxy, guardrails
  diff/      Pricing diff engine, meaningfulness checks, alert rules
trigger/     Background jobs (daily analysis, pricing checks, retention)
```

---

### 6. Specter (adyhafetz/specter) — ⭐ Enterprise

**URL:** https://github.com/adyhafetz/specter
**Stack:** Next.js + PostgreSQL + Bright Data + AIMLAPI
**License:** Proprietary

**Notable features (not adapted — enterprise-grade):**
- **Certificate transparency logs:** Discovers subdomains via crt.sh.
- **Multi-geo scraping:** US, UK, SG — regional product rollouts, beta pages, pricing tests.
- **Bright Data:** Residential proxies, Web Unlocker for blocked pages, Scraping Browser for screenshots, SERP API.
- **Agentic workflow:** Plans tool calls (discover_subdomains, fetch_dns_records, scrape_page) autonomously.
- **Semantic diffing before LLM classification:** If no meaningful change, skip LLM entirely (saves cost).

---

### 7. changedetection.io (dgtlmoon) — ⭐ General Purpose

**URL:** https://github.com/dgtlmoon/changedetection.io
**Stack:** Python + Playwright + Selenium
**License:** Apache 2.0 | **Stars:** 15k+

**What it does:**
General-purpose website change detection and alerts. Not competitor-specific, but the most established open-source tool in the category.

**Notable features (reference only — general purpose, not adapted):**
- AI visual selector (GPT-4o analyzes page screenshots)
- Plain-language change summaries
- 40+ site templates (Amazon, eBay, GitHub, LinkedIn, etc.)
- Chrome extension (right-click → "Monitor this page")
- Multi-channel notifications: email, push, Slack, Discord, webhooks
- REST API for custom integrations

---

## Patterns Across All Repos

### Universal Patterns (everyone does this)
1. **Scheduled scraping** — Cron, Vercel Cron, Cloudflare Cron, GitHub Actions. Nobody runs manually.
2. **Diff-based change detection** — Whether text diff, hash diff, or semantic diff. Everyone compares against a baseline.
3. **LLM summarization** — Raw diffs are noise. The LLM writes the digest. Everyone does this.
4. **Multi-channel delivery** — Email, Slack, Discord, webhooks. Reports must reach the human where they are.
5. **Noise filtering** — Typos, dates, rotating testimonials — everyone filters these out.

### Divergent Patterns (different approaches to the same problem)
| Problem | Approach A | Approach B | Which We Chose |
|---------|-----------|-----------|---------------|
| Change detection | Text diff (drift, Telnyx) | Semantic diff (competitor-monitor, Specter) | Semantic (LLM-prompt) |
| Scraping | Cheerio + JSON islands (drift) | Playwright headless (competitor-monitor) | Firecrawl MCP (our existing tool) |
| Storage | SQLite (drift, Telnyx) | Cloudflare KV (ScopeHound) | Markdown files + memory snapshots |
| AI model | Gemini 2.5 Flash (drift) | sentence-transformers (competitor-monitor) | Agent's LLM (no extra API) |
| Delivery | Email/Slack/Discord (drift, ScopeHound) | Markdown reports on disk (competitor-monitor) | Response + auto-save to vault |
| Competitor discovery | Manual YAML config (most) | AI-powered search (ScopeHound) | Exa semantic search |
| Pricing | Free/self-host (drift, ScopeHound) | SaaS plans $29-199/mo (ScopeHound, RivalEye) | Free (part of Goblin Recon) |

### What Nobody Does (Gap Opportunities)
1. **Operational adoption monitoring** — Nobody tracks whether competitors help customers actually *use* the product. They track features, not outcomes.
2. **Brand voice gap analysis** — Nobody flags competitor language that conflicts with your brand voice. This is GenX's unique "What NOT to copy" section.
3. **Positioning gap, not feature gap** — Most tools compare feature lists. Nobody asks "what can we say that they structurally cannot?"
4. **Founder story comparison** — RivalEye tracks branding (colors, fonts) but nobody compares founder narratives.

---

## Adaptation Decisions

### What We Stole (v2.0)
| From | Technique | Adaptation |
|------|-----------|-----------|
| drift | Content-hash dedup | SHA256 per page → skip unchanged |
| drift | Source types (`--kind`) | Added to competitors.yaml schema |
| ScopeHound | Priority scoring (HIGH/MED/LOW) | Added to change detection tables |
| ScopeHound | "All clear" message | `[SILENT]` for cron, "all clear" for ad-hoc |
| ScopeHound | Competitor auto-discovery | New `discover competitors` command via Exa |
| competitor-monitor | Semantic diffing concept | LLM-prompt semantic diff (no embeddings needed) |
| Telnyx Monitor | Sitemap auto-discovery | `firecrawl_map` as step 1 of deep scans |
| Telnyx Monitor | Atom/RSS feed support | Added `rss_feed` to competitor config |
| drift | Executive digest format | New top section: signal, urgency, key change, action |
| drift + ScopeHound | Multi-source delivery | Post-scan delivery routing |

### What We Skipped (and Why)
| Technique | Why Skipped |
|-----------|------------|
| sentence-transformers embeddings | Zero-dependency LLM-prompt approach achieves same result |
| Bright Data / enterprise proxies | Firecrawl handles our 2-3 competitors fine |
| Geo-aware pricing (4 regions) | GenX doesn't compete on global pricing |
| Tech stack detection (Wappalyzer) | Irrelevant — we care about positioning, not CDN choice |
| SaaS dashboard + Stripe billing | We're an agent, not a product |
| Cloudflare Workers runtime | We run on Hermes |
| Chrome extension | Not an agent feature |
| Playwright headless | Firecrawl already handles JS rendering |

---

## References

- drift: https://github.com/getdrift/drift
- ScopeHound: https://github.com/ZeroLupo/scopehound
- competitor-monitor: https://github.com/Keerthivasan-Venkitajalam/competitor-monitor
- Telnyx Monitor: https://github.com/team-telnyx/Competitor-Monitor
- RivalEye: https://github.com/Bharath-code/rivaleye
- Specter: https://github.com/adyhafetz/specter
- changedetection.io: https://github.com/dgtlmoon/changedetection.io

---

*Research compiled June 15, 2026 by Goblin Recon.*
*Source: Live Firecrawl MCP scraping of all 7 GitHub repos + Exa semantic search for discovery.*
