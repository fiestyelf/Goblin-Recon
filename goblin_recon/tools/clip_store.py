"""Persistent Clip Mine store."""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT_DIR = Path(__file__).resolve().parents[2]
VAULT_DIR = ROOT_DIR / "vault"
DEFAULT_DB_PATH = VAULT_DIR / "clips.db"
YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}
VALID_STATUSES = {"pending_review", "approved", "in_production", "scheduled", "posted", "shelved"}
TEXT_SEARCH_COLUMNS = (
    "trend_headline",
    "source_title",
    "source_channel_or_account",
    "moment_summary",
    "why_post",
    "suggested_caption",
    "source_url",
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS clips (
    clip_id TEXT PRIMARY KEY,
    date_approved TEXT,
    status TEXT NOT NULL DEFAULT 'pending_review',
    brand_angle TEXT,
    brand_alignment_score INTEGER,
    trend_headline TEXT,
    source_title TEXT,
    source_channel_or_account TEXT,
    source_url TEXT NOT NULL,
    source_video_id TEXT,
    start_timestamp TEXT,
    end_timestamp TEXT,
    start_sec INTEGER NOT NULL,
    end_sec INTEGER NOT NULL,
    duration_seconds INTEGER NOT NULL,
    moment_summary TEXT,
    why_post TEXT,
    suggested_caption TEXT,
    blacklist_flags TEXT,
    human_decision TEXT,
    effort TEXT,
    confidence TEXT,
    vault_check TEXT,
    fallback_angle TEXT,
    ai_search_potential TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_clips_status ON clips(status);
CREATE INDEX IF NOT EXISTS idx_clips_source_video_id ON clips(source_video_id);
CREATE INDEX IF NOT EXISTS idx_clips_source_window ON clips(source_video_id, start_sec, end_sec);
"""

FTS_SCHEMA = """
CREATE VIRTUAL TABLE IF NOT EXISTS clips_fts USING fts5(
    clip_id UNINDEXED,
    trend_headline,
    source_title,
    source_channel_or_account,
    moment_summary,
    why_post,
    suggested_caption,
    source_url
);
"""

OPTIONAL_COLUMNS = {
    "effort": "TEXT",
    "confidence": "TEXT",
    "vault_check": "TEXT",
    "fallback_angle": "TEXT",
    "ai_search_potential": "TEXT",
    "brief_path": "TEXT",
    "tracker_provider": "TEXT",
    "tracker_entry_id": "TEXT",
    "tracker_entry_url": "TEXT",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def extract_youtube_id(source_url: str) -> str | None:
    parsed = urlparse(source_url)
    host = parsed.netloc.lower()
    if host not in YOUTUBE_HOSTS:
        return None
    video_id = ""
    if host == "youtu.be":
        video_id = parsed.path.strip("/").split("/")[0]
    elif parsed.path == "/watch":
        video_id = parse_qs(parsed.query).get("v", [""])[0]
    elif parsed.path.startswith("/embed/"):
        video_id = parsed.path.split("/embed/", 1)[1].split("/", 1)[0]
    elif parsed.path.startswith("/v/"):
        video_id = parsed.path.split("/v/", 1)[1].split("/", 1)[0]
    elif parsed.path.startswith("/shorts/"):
        video_id = parsed.path.split("/shorts/", 1)[1].split("/", 1)[0]
    return video_id if len(video_id) == 11 else None


def make_clip_id(source_url: str, start_sec: int, end_sec: int) -> str:
    source_key = extract_youtube_id(source_url) or source_url.strip().lower()
    digest = hashlib.sha1(f"{source_key}:{start_sec}:{end_sec}".encode()).hexdigest()[:12]
    return f"clip_{digest}"


def connect(db_path: str | Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    _ensure_optional_columns(conn)
    _ensure_fts(conn)
    return conn


def _ensure_optional_columns(conn: sqlite3.Connection) -> None:
    existing = {row[1] for row in conn.execute("PRAGMA table_info(clips)")}
    for column, column_type in OPTIONAL_COLUMNS.items():
        if column not in existing:
            conn.execute(f"ALTER TABLE clips ADD COLUMN {column} {column_type}")


def _ensure_fts(conn: sqlite3.Connection) -> bool:
    try:
        conn.executescript(FTS_SCHEMA)
        _rebuild_fts(conn)
    except sqlite3.OperationalError:
        return False
    return True


def _fts_enabled(conn: sqlite3.Connection) -> bool:
    row = conn.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'clips_fts'").fetchone()
    return row is not None


def _rebuild_fts(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM clips_fts")
    conn.execute(
        """
        INSERT INTO clips_fts (
            rowid, clip_id, trend_headline, source_title, source_channel_or_account,
            moment_summary, why_post, suggested_caption, source_url
        )
        SELECT rowid, clip_id, trend_headline, source_title, source_channel_or_account,
            moment_summary, why_post, suggested_caption, source_url
        FROM clips
        """
    )


def _sync_clip_fts(conn: sqlite3.Connection, clip_id: str) -> None:
    if not _fts_enabled(conn):
        return
    conn.execute("DELETE FROM clips_fts WHERE clip_id = ?", (clip_id,))
    conn.execute(
        """
        INSERT INTO clips_fts (
            rowid, clip_id, trend_headline, source_title, source_channel_or_account,
            moment_summary, why_post, suggested_caption, source_url
        )
        SELECT rowid, clip_id, trend_headline, source_title, source_channel_or_account,
            moment_summary, why_post, suggested_caption, source_url
        FROM clips WHERE clip_id = ?
        """,
        (clip_id,),
    )


def _fts_query(query: str | None) -> str | None:
    if not query:
        return None
    terms = re.findall(r"[A-Za-z0-9_]+", query)
    return " AND ".join(terms) if terms else None


def _json_or_text(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def _require_int(value: object, field: str) -> int:
    if value is None:
        raise ValueError(f"{field} is required")
    return int(value)


def save_clip(clip: dict, db_path: str | Path = DEFAULT_DB_PATH) -> str:
    source_url = str(clip.get("source_url") or "").strip()
    if not source_url:
        raise ValueError("source_url is required")
    start_sec = _require_int(clip.get("start_sec"), "start_sec")
    end_sec = _require_int(clip.get("end_sec"), "end_sec")
    if start_sec < 0 or end_sec <= start_sec:
        raise ValueError("clip window must be a positive range")
    duration_seconds = int(clip.get("duration_seconds") or end_sec - start_sec)
    status = str(clip.get("status") or "pending_review")
    if status not in VALID_STATUSES:
        raise ValueError(f"invalid status: {status}")

    now = utc_now()
    record = {
        "clip_id": clip.get("clip_id") or make_clip_id(source_url, start_sec, end_sec),
        "date_approved": clip.get("date_approved"),
        "status": status,
        "brand_angle": clip.get("brand_angle"),
        "brand_alignment_score": clip.get("brand_alignment_score"),
        "trend_headline": clip.get("trend_headline"),
        "source_title": clip.get("source_title"),
        "source_channel_or_account": clip.get("source_channel_or_account"),
        "source_url": source_url,
        "source_video_id": clip.get("source_video_id") or extract_youtube_id(source_url),
        "start_timestamp": clip.get("start_timestamp"),
        "end_timestamp": clip.get("end_timestamp"),
        "start_sec": start_sec,
        "end_sec": end_sec,
        "duration_seconds": duration_seconds,
        "moment_summary": clip.get("moment_summary"),
        "why_post": clip.get("why_post"),
        "suggested_caption": clip.get("suggested_caption"),
        "blacklist_flags": _json_or_text(clip.get("blacklist_flags")),
        "human_decision": clip.get("human_decision"),
        "effort": clip.get("effort"),
        "confidence": clip.get("confidence"),
        "vault_check": clip.get("vault_check"),
        "fallback_angle": clip.get("fallback_angle"),
        "ai_search_potential": clip.get("ai_search_potential"),
        "brief_path": clip.get("brief_path"),
        "tracker_provider": clip.get("tracker_provider"),
        "tracker_entry_id": clip.get("tracker_entry_id"),
        "tracker_entry_url": clip.get("tracker_entry_url"),
        "created_at": clip.get("created_at") or now,
        "updated_at": now,
    }
    columns = list(record)
    placeholders = ", ".join(f":{col}" for col in columns)
    updates = ", ".join(f"{col}=excluded.{col}" for col in columns if col not in {"clip_id", "created_at"})

    with connect(db_path) as conn:
        conn.execute(
            f"""
            INSERT INTO clips ({', '.join(columns)}) VALUES ({placeholders})
            ON CONFLICT(clip_id) DO UPDATE SET {updates}
            """,
            record,
        )
        _sync_clip_fts(conn, str(record["clip_id"]))
    return str(record["clip_id"])


def save_clip_kwargs(db_path: str | Path = DEFAULT_DB_PATH, **kwargs: object) -> str:
    """Compatibility wrapper for callers that pass clip fields as keywords."""
    return save_clip(dict(kwargs), db_path=db_path)


def get_clip_count(db_path: str | Path = DEFAULT_DB_PATH) -> int:
    """Return the number of stored clip records."""
    with connect(db_path) as conn:
        row = conn.execute("SELECT COUNT(*) FROM clips").fetchone()
    return int(row[0]) if row else 0


def get_clip(clip_id: str, db_path: str | Path = DEFAULT_DB_PATH) -> dict | None:
    with connect(db_path) as conn:
        row = conn.execute("SELECT * FROM clips WHERE clip_id = ?", (clip_id,)).fetchone()
    return dict(row) if row else None


def find_clips(
    *,
    status: str | None = None,
    query: str | None = None,
    limit: int = 20,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> list[dict]:
    clauses = []
    params: list[object] = []
    fts_query = _fts_query(query)
    if status:
        clauses.append("clips.status = ?")
        params.append(status)

    with connect(db_path) as conn:
        if fts_query and _fts_enabled(conn):
            clauses.append("clips_fts MATCH ?")
            params.append(fts_query)
            where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
            sql = f"""
            SELECT clips.* FROM clips
            JOIN clips_fts ON clips_fts.rowid = clips.rowid
            {where}
            ORDER BY bm25(clips_fts), clips.created_at DESC
            LIMIT ?
            """
        else:
            if query:
                like_clauses = [f"clips.{col} LIKE ?" for col in TEXT_SEARCH_COLUMNS]
                clauses.append(f"({' OR '.join(like_clauses)})")
                params.extend([f"%{query}%"] * len(TEXT_SEARCH_COLUMNS))
            where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
            sql = f"SELECT clips.* FROM clips {where} ORDER BY clips.created_at DESC LIMIT ?"
        params.append(limit)
        rows = conn.execute(sql, params).fetchall()
    return [dict(row) for row in rows]


def update_status(
    clip_id: str,
    status: str,
    *,
    human_decision: str | None = None,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> bool:
    if status not in VALID_STATUSES:
        raise ValueError(f"invalid status: {status}")
    with connect(db_path) as conn:
        result = conn.execute(
            """
            UPDATE clips
            SET status = ?, human_decision = COALESCE(?, human_decision), updated_at = ?
            WHERE clip_id = ?
            """,
            (status, human_decision, utc_now(), clip_id),
        )
    return result.rowcount > 0


def update_brief_path(clip_id: str, brief_path: str, db_path: str | Path = DEFAULT_DB_PATH) -> bool:
    with connect(db_path) as conn:
        result = conn.execute(
            "UPDATE clips SET brief_path = ?, updated_at = ? WHERE clip_id = ?",
            (brief_path, utc_now(), clip_id),
        )
    return result.rowcount > 0


def check_duplicate(
    source_url: str,
    start_sec: int,
    end_sec: int,
    *,
    tolerance_seconds: int = 5,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> list[dict]:
    source_video_id = extract_youtube_id(source_url)
    if not source_video_id:
        return []
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT * FROM clips
            WHERE source_video_id = ? AND start_sec <= ? AND end_sec >= ?
            ORDER BY ABS(start_sec - ?) ASC, created_at DESC
            """,
            (source_video_id, end_sec + tolerance_seconds, start_sec - tolerance_seconds, start_sec),
        ).fetchall()
    return [dict(row) for row in rows]


def init_db(db_path: str | Path = DEFAULT_DB_PATH) -> Path:
    with connect(db_path):
        pass
    return Path(db_path)


def before_clip_mine(topic_or_url: str, db_path: str | Path = DEFAULT_DB_PATH) -> dict:
    source_video_id = extract_youtube_id(topic_or_url) if topic_or_url.startswith(("http://", "https://")) else None
    if source_video_id:
        existing = find_clips(query=source_video_id, limit=10, db_path=db_path)
    else:
        existing = find_clips(query=topic_or_url, limit=10, db_path=db_path)
    approved = [clip for clip in existing if clip.get("status") == "approved"]
    shelved = [clip for clip in existing if clip.get("status") == "shelved"]
    if approved:
        status = "already_approved"
        recommendation = "differentiate"
    elif shelved:
        status = "similar_shelved"
        recommendation = "review_shelved_reason"
    elif existing:
        status = "similar_exists"
        recommendation = "differentiate"
    else:
        status = "no_overlap"
        recommendation = "proceed"
    return {
        "vault_status": status,
        "similar_clips": existing,
        "shelved_clips": shelved,
        "recommendation": recommendation,
    }


def format_timestamp(seconds: int) -> str:
    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours}:{minutes:02d}:{secs:02d}" if hours else f"{minutes}:{secs:02d}"


def youtube_timestamp_url(source_url: str, start_sec: int) -> str:
    separator = "&" if "?" in source_url else "?"
    return f"{source_url.split('#', 1)[0]}{separator}t={int(start_sec)}"


def youtube_embed_url(source_url: str, start_sec: int, end_sec: int) -> str | None:
    video_id = extract_youtube_id(source_url)
    if not video_id:
        return None
    return f"https://www.youtube.com/embed/{video_id}?start={int(start_sec)}&end={int(end_sec)}"


def _value(clip: dict, key: str, fallback: str = "Not stored") -> str:
    value = clip.get(key)
    return fallback if value is None or value == "" else str(value)


def render_clip_brief(clip: dict) -> str:
    start_sec = int(clip["start_sec"])
    end_sec = int(clip["end_sec"])
    duration = int(clip.get("duration_seconds") or end_sec - start_sec)
    source_url = str(clip["source_url"])
    timestamp_url = youtube_timestamp_url(source_url, start_sec)
    embed_url = youtube_embed_url(source_url, start_sec, end_sec) or "Not available"
    source_title = _value(clip, "source_title")
    channel = _value(clip, "source_channel_or_account")
    brand_angle = _value(clip, "brand_angle")
    brand_score = _value(clip, "brand_alignment_score")
    blacklist_flags = _value(clip, "blacklist_flags", "none")
    status = _value(clip, "status")

    return f"""# Clip Mine Brief

## Decision

**Action:** {status.upper()}
**Category:** {_value(clip, "trend_headline")}
**Effort:** {_value(clip, "effort")}
**Confidence:** {_value(clip, "confidence")}
**Vault check:** {_value(clip, "vault_check")}
**Fallback angle:** {_value(clip, "fallback_angle")}
**AI search potential:** {_value(clip, "ai_search_potential")}
**Brief path:** {_value(clip, "brief_path")}

## Video Metadata

| Field | Value |
|-------|-------|
| **Video** | {source_title} - {channel} |
| **Channel** | {channel} |
| **Source URL** | {source_url} |
| **Tracker provider** | {_value(clip, "tracker_provider")} |
| **Tracker entry** | {_value(clip, "tracker_entry_url", _value(clip, "tracker_entry_id"))} |

## Background

{source_title} is the source video for this Clip Mine record. {channel} is the speaker or publishing channel. The selected moment matters because it connects the source to this content angle: {_value(clip, "trend_headline")}.

## The Clip

| Field | Value |
|-------|-------|
| **Start time** | {_value(clip, "start_timestamp", format_timestamp(start_sec))} ({start_sec} seconds) |
| **End time** | {_value(clip, "end_timestamp", format_timestamp(end_sec))} |
| **Duration** | {duration} seconds |
| **Direct link** | {timestamp_url} |
| **Embed preview** | {embed_url} |

## Source Access

| Field | Value |
|-------|-------|
| **Original source** | {source_url} |
| **Open at clip start** | {timestamp_url} |
| **Preview window** | {embed_url} |
| **Clip window** | {start_sec} -> {end_sec} |
| **Rights note** | Use the link to inspect and cut the moment. Do not download or repost copyrighted source footage without human rights review. |

### The Moment
> {_value(clip, "moment_summary")}

### Why This Moment
{_value(clip, "why_post")}

## Brand Gate

| Check | Result |
|-------|--------|
| Brand angle | {brand_angle} |
| Brand alignment score | {brand_score}/15 |
| Blacklist violations | {blacklist_flags} |
| Verdict | {"PASS" if status in {"approved", "in_production", "scheduled", "posted"} else "REVIEW"} |

## Platform Variants

### Instagram Reel
- **Caption:** {_value(clip, "suggested_caption")}

### YouTube Shorts
- **Title:** {source_title}
- **Description:** Watch the full source: {source_url}

### LinkedIn
- **Copy:** {_value(clip, "why_post")}

---

*Clip ID: {clip["clip_id"]} | Status: {status} | Retrieved from vault/clips.db*
"""


def main() -> int:
    path = init_db()
    print(f"Clip store ready: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
