# Competitor Snapshots

Goblin Recon stores competitor data here for change detection.

---

## Format

Each snapshot:
```
### [DATE] — [COMPETITOR NAME]

**Pricing:**
- Plan 1: [price]
- Plan 2: [price]

**Features:**
- [Feature]: [description]

**Marketing:**
- Messaging: "[tagline]"
- Blacklist signals: [none / hype / woo / corporate filler / empty generic]

**Emotional signature:**
- Dominant emotional register: [e.g., heroic, urgent, clinical, aspirational, authoritative]
- How it lands on a first-time viewer: [first-touch feeling]

**Competitor gap mapping:**
- What GenX can say/do that this competitor structurally cannot: [gap]
- B2C gap: [science+soul/truly-seen opportunity]
- B2B gap: [results-not-advice / operators-not-advisors opportunity]

**Ownable angle extraction:**
- Angles genuinely ownable by GenX (not just different): [list]
- Angles the competitor already owns: [list]

**Voice calibration:**
- Advisor or operator tone: [advisor / operator / mixed]
- Truly-seen signal for B2C: [present / absent / partial]
- Brand voice overlap with GenX: [none / low / medium / high]

**Changes since last scan:**
- [What changed]

**Extraction method:**
- Normal public fetch / Scrapling JS fallback / Not extracted
```

---

## Snapshots

### 2026-06-13 — CrewAI

**Features (17 extracted):**
- No-code visual editor, role-based agents, deterministic workflows
- Enterprise IAM, human-in-the-loop, PII redaction, runtime hooks
- Multi-LLM testing, evaluation partners (Arize, Galileo, DataDog, Patronus)
- Automated training, real-time tracing, code-first API

**Marketing:** "Agentic use case generator powered by billions of agent runs"
**Emotional signature:** Authoritative + comprehensive — "we handle everything"
**Gap:** No operational adoption story. All tools, no operators.
**B2B gap:** "Results not advice" — they sell infrastructure, not implementation outcomes.
**Extraction method:** ScrapeGraph v2 (`--schema features`)

### 2026-06-13 — LangChain

**Features (10 extracted):**
- Engine (auto-diagnose), Observability, Evaluation, Deployment
- Fleet, Sandboxes, Deep Agents, LangChain, LangGraph, LangSmith

**Marketing:** "Improve agents faster with LangSmith Engine"
**Emotional signature:** Clinical + developer-centric — "engineering platform"
**Gap:** Zero mention of the human who runs the system post-deployment.
**B2B gap:** "Operators not advisors" — they're a platform, not a partner.
**Extraction method:** ScrapeGraph v2 (`--schema features`)

### GenX opportunity (from this scan)
Neither competitor talks about operational adoption — getting teams to trust, use, and change workflow around AI agents. That's GenX's lane: "Results, not advice. Practical implementation, not opinions."
