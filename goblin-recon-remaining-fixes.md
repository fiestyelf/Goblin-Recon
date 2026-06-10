# Goblin Recon — Remaining Fixes (3 Items)

Three issues I found in the repo. Each is a find-and-replace patch. Apply in OpenCode.

---

## Fix 1: Add Engagement Analytics to the Clip Mine Workflow

**File:** `skills/goblin-recon/SKILL.md`

### 1A — End-to-End Process (lines 459-473)

**Find:**
```
Goblin Recon:
  ├─ Scans Instagram/TikTok/X for trending AI stories
  ├─ Searches YouTube for podcasts covering those stories
  ├─ Pulls transcripts from the best videos
  ├─ Finds the strongest 30-60 second moments
  └─ Outputs a CLIP BRIEF with:
      - Timestamped URL (youtube.com/watch?v=XXX&t=308)
      - Transcript quote
      - Category tag
      - 7-dimension scores
      - Brand gate result
      - Caption for Instagram
```

**Replace with:**
```
Goblin Recon:
  ├─ Scans Instagram/TikTok/X for trending AI stories
  ├─ Searches YouTube for podcasts covering those stories
  ├─ Pulls transcripts from the best videos
  ├─ Fetches video metadata (views, likes, comments via get_video_metadata)
  ├─ Computes engagement velocity (via score_engagement)
  ├─ Finds the strongest 30-60 second moments
  └─ Outputs a CLIP BRIEF with:
      - Timestamped URL (youtube.com/watch?v=XXX&t=308)
      - Transcript quote
      - Category tag
      - Engagement analytics (views, likes, view velocity, like ratio)
      - 7-dimension scores
      - Brand gate result
      - Caption for Instagram
```

### 1B — Testing Workflow (lines 552-560)

**Find:**
```
1. **Layer 1** — Browser-based IG creator scan + TikTok hashtags + news sites
2. **Score stories** — Apply social_velocity first, then remaining dimensions. Confirm all >60.
3. **Layer 2** — Browser-based YouTube/IG/TikTok search for top 2–3 stories
4. **Pick best source** — Prioritize podcast/interview, English captions available, high scroll_stop
5. **Layer 3** — Extract transcript, find best moment, validate with extract_clip.py
6. **Brand gate** — Check blacklist, nuance words, brand angle. Score ≥8/15.
7. **Clip brief** — Follow template with platform variants
```

**Replace with:**
```
1. **Layer 1** — Browser-based IG creator scan + TikTok hashtags + news sites
2. **Score stories** — Apply social_velocity first, then remaining dimensions. Confirm all >60.
3. **Layer 2** — Browser-based YouTube/IG/TikTok search for top 2–3 stories
4. **Pick best source** — Prioritize podcast/interview, English captions available, high scroll_stop
5. **Layer 3** — Extract transcript, find best moment, validate with extract_clip.py
6. **Collect engagement data** — Fetch video metadata (views, likes, comments) via get_video_metadata, compute velocity via score_engagement
7. **Brand gate** — Check blacklist, nuance words, brand angle. Score ≥8/15.
8. **Clip brief** — Follow template with platform variants, fill Engagement Analytics section
```

### 1C — "Clip Brief Must Include" (lines 527-536)

**Find:**
```
### Clip Brief Must Include
- Decision (approve/shelve/modify)
- Background (2-3 sentences explaining source, speaker, and why the moment matters)
- Video metadata (title, channel, views, URL)
- The moment text with exact timestamps
- Why post
- Scores by dimension (including scroll_stop)
- Brand gate result (angle, alignment score, blacklist violations)
- Platform variants (Instagram Reel, LinkedIn, YouTube Shorts)
- Fallback angle if rejected
```

**Replace with:**
```
### Clip Brief Must Include
- Decision (approve/shelve/modify)
- Background (2-3 sentences explaining source, speaker, and why the moment matters)
- Video metadata (title, channel, views, URL)
- Engagement analytics (views, likes, view velocity, like ratio, comment count)
- The moment text with exact timestamps
- Why post
- Scores by dimension (including scroll_stop)
- Brand gate result (angle, alignment score, blacklist violations)
- Platform variants (Instagram Reel, LinkedIn, YouTube Shorts)
- Fallback angle if rejected
```

---

## Fix 2: Add Engagement Fields to clip_store Schema

**File:** `goblin_recon/tools/clip_store.py`

### 2A — Add columns to SCHEMA (around line 57)

**Find:**
```
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

**Replace with:**
```
    view_count INTEGER,
    like_count INTEGER,
    comment_count INTEGER,
    velocity_score REAL,
    engagement_rate REAL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

### 2B — Add engagement fields to save_clip() INSERT (around line 215)

**Find:**
```
        "effort", "confidence", "vault_check", "fallback_angle", "ai_search_potential",
        "created_at", "updated_at",
```

**Replace with:**
```
        "effort", "confidence", "vault_check", "fallback_angle", "ai_search_potential",
        "view_count", "like_count", "comment_count", "velocity_score", "engagement_rate",
        "created_at", "updated_at",
```

### 2C — Add engagement fields to VALUES placeholders (around line 226)

**Find:**
```
        :effort, :confidence, :vault_check, :fallback_angle, :ai_search_potential,
        :created_at, :updated_at,
```

**Replace with:**
```
        :effort, :confidence, :vault_check, :fallback_angle, :ai_search_potential,
        :view_count, :like_count, :comment_count, :velocity_score, :engagement_rate,
        :created_at, :updated_at,
```

### 2D — Add engagement fields to UPDATE SET (around line 243)

**Find:**
```
        effort = :effort,
        confidence = :confidence,
        vault_check = :vault_check,
        fallback_angle = :fallback_angle,
        ai_search_potential = :ai_search_potential,
```

**Replace with:**
```
        effort = :effort,
        confidence = :confidence,
        vault_check = :vault_check,
        fallback_angle = :fallback_angle,
        ai_search_potential = :ai_search_potential,
        view_count = :view_count,
        like_count = :like_count,
        comment_count = :comment_count,
        velocity_score = :velocity_score,
        engagement_rate = :engagement_rate,
```

### 2E — Add nullable(INTEGER) entries for engagement fields in schema upgrade (around line 62)

**Find:**
```
def _nullable(t: str) -> str:
    return t
```

**Replace with:**
```
def _nullable(t: str) -> str:
    return t


NEW_ENGAGEMENT_COLUMNS = [
    ("view_count", "INTEGER"),
    ("like_count", "INTEGER"),
    ("comment_count", "INTEGER"),
    ("velocity_score", "REAL"),
    ("engagement_rate", "REAL"),
]
```

**Also find and add a migration function after `_nullable`:**

**Find the line:**
```
def get_db_path() -> str:
```

**Replace with:**
```
def _upgrade_schema_add_engagement(conn: sqlite3.Connection) -> None:
    """Add engagement analytics columns if missing."""
    cursor = conn.execute("PRAGMA table_info(clips)")
    existing = {row[1] for row in cursor.fetchall()}
    for col_name, col_type in NEW_ENGAGEMENT_COLUMNS:
        if col_name not in existing:
            conn.execute(f"ALTER TABLE clips ADD COLUMN {col_name} {col_type}")


def get_db_path() -> str:
```

Then **find** in `init_db()`:
```
    _ensure_vault_dirs()
    conn = _connect()
    conn.executescript(SCHEMA)
    conn.executescript(FTS_SCHEMA)
    conn.commit()
```

**Replace with:**
```
    _ensure_vault_dirs()
    conn = _connect()
    conn.executescript(SCHEMA)
    _upgrade_schema_add_engagement(conn)
    conn.executescript(FTS_SCHEMA)
    conn.commit()
```

---

## Fix 3: Remove Duplicate scripts/

**Files to delete:**

| File | Why |
|---|---|
| `scripts/clip_store.py` | Identical to `goblin_recon/tools/clip_store.py` (17,594 bytes both) |
| `scripts/social_intake.py` | Superseded by `goblin_recon/tools/social_intake.py` (10,624 vs 7,283 bytes — the tools/ version is the canonical one) |

Run:
```bash
git rm scripts/clip_store.py scripts/social_intake.py
git commit -m "chore: remove duplicate scripts now in goblin_recon/tools/"
```

The remaining scripts are all non-duplicates and should stay:
- `scripts/check_secrets.py` — standalone security scan
- `scripts/dev_check.sh` — dev env validation
- `scripts/query_clips.py` — standalone clip query CLI
- `scripts/setup.sh` — profile installer

---

## Summary

| Fix | File | Type | Lines Changed |
|-----|------|------|--------------|
| 1A | `skills/goblin-recon/SKILL.md` | Edit end-to-end pipeline | ~5 lines |
| 1B | `skills/goblin-recon/SKILL.md` | Edit testing workflow | ~2 lines |
| 1C | `skills/goblin-recon/SKILL.md` | Add to clip brief requirements | ~1 line |
| 2A-E | `goblin_recon/tools/clip_store.py` | Schema + save + migration | ~20 lines |
| 3 | `scripts/clip_store.py`, `scripts/social_intake.py` | Delete duplicates | 2 files |

Total effort: ~15 minutes in OpenCode.
