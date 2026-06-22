"""Tiny SQLite vault for Clip Mine records."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import hashlib

ROOT_DIR = Path(__file__).resolve().parents[2]
VAULT_DIR = ROOT_DIR / "vault"
DEFAULT_DB_PATH = VAULT_DIR / "clips.db"
YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}
VALID_STATUSES = {"pending_review", "approved", "in_production", "scheduled", "posted", "shelved"}

COLUMNS = {
    "clip_id": "TEXT PRIMARY KEY",
    "created_at": "TEXT NOT NULL",
    "updated_at": "TEXT NOT NULL",
    "status": "TEXT NOT NULL DEFAULT 'pending_review'",
    "human_decision": "TEXT",
    "brand_angle": "TEXT",
    "brand_alignment_score": "INTEGER",
    "blacklist_flags": "TEXT",
    "trend_headline": "TEXT",
    "source_title": "TEXT",
    "source_channel_or_account": "TEXT",
    "source_url": "TEXT NOT NULL",
    "source_video_id": "TEXT",
    "start_timestamp": "TEXT",
    "end_timestamp": "TEXT",
    "start_sec": "INTEGER NOT NULL",
    "end_sec": "INTEGER NOT NULL",
    "duration_seconds": "INTEGER",
    "moment_summary": "TEXT",
    "transcript_excerpt": "TEXT",
    "why_post": "TEXT",
    "suggested_caption": "TEXT",
    "effort": "TEXT",
    "confidence": "TEXT",
    "vault_check": "TEXT",
    "fallback_angle": "TEXT",
    "ai_search_potential": "TEXT",
    "view_count": "INTEGER",
    "like_count": "INTEGER",
    "comment_count": "INTEGER",
    "velocity_score": "REAL",
    "engagement_rate": "REAL",
    "brief_path": "TEXT",
}
TEXT_SEARCH_COLUMNS = [
    "clip_id", "trend_headline", "source_title", "source_channel_or_account",
    "moment_summary", "transcript_excerpt", "why_post", "suggested_caption", "brand_angle",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def extract_youtube_id(url: str) -> str | None:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if host not in YOUTUBE_HOSTS:
        return None
    if host == "youtu.be":
        return parsed.path.strip("/") or None
    if parsed.path.startswith("/shorts/") or parsed.path.startswith("/embed/"):
        return parsed.path.split("/")[2] or None
    return parse_qs(parsed.query).get("v", [None])[0]


def make_clip_id(source_url: str, start_sec: int, end_sec: int) -> str:
    video = extract_youtube_id(source_url) or source_url
    return "clip_" + hashlib.sha1(f"{video}:{start_sec}:{end_sec}".encode()).hexdigest()[:12]


def connect(db_path: str | Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE IF NOT EXISTS clips (clip_id TEXT PRIMARY KEY)")
    existing = {row[1] for row in conn.execute("PRAGMA table_info(clips)")}
    for name, spec in COLUMNS.items():
        if name not in existing:
            conn.execute(f"ALTER TABLE clips ADD COLUMN {name} {spec.replace('PRIMARY KEY', '').replace('NOT NULL', '')}")
    conn.commit()
    return conn


def _json_or_text(value: object) -> object:
    return json.dumps(value, ensure_ascii=False) if isinstance(value, (list, dict)) else value


def _as_int(value: object, field: str) -> int:
    if value is None or value == "":
        raise ValueError(f"{field} is required")
    return int(value)


def save_clip(clip: dict, db_path: str | Path = DEFAULT_DB_PATH) -> str:
    start = _as_int(clip.get("start_sec"), "start_sec")
    end = _as_int(clip.get("end_sec"), "end_sec")
    if end <= start:
        raise ValueError("end_sec must be greater than start_sec")
    if end - start > 60:
        raise ValueError("clip duration must be 60 seconds or less")

    now = utc_now()
    data = {name: _json_or_text(clip.get(name)) for name in COLUMNS}
    data.update(
        clip_id=clip.get("clip_id") or make_clip_id(str(clip.get("source_url")), start, end),
        created_at=clip.get("created_at") or now,
        updated_at=now,
        status=clip.get("status") or "pending_review",
        source_url=clip["source_url"],
        source_video_id=clip.get("source_video_id") or extract_youtube_id(str(clip["source_url"])),
        start_sec=start,
        end_sec=end,
        duration_seconds=clip.get("duration_seconds") or end - start,
    )

    cols = list(COLUMNS)
    placeholders = ", ".join("?" for _ in cols)
    updates = ", ".join(f"{col}=excluded.{col}" for col in cols if col != "clip_id")
    sql = f"INSERT INTO clips ({', '.join(cols)}) VALUES ({placeholders}) ON CONFLICT(clip_id) DO UPDATE SET {updates}"
    with connect(db_path) as conn:
        conn.execute(sql, [data.get(col) for col in cols])
    return str(data["clip_id"])


def save_clip_kwargs(db_path: str | Path = DEFAULT_DB_PATH, **kwargs: object) -> str:
    return save_clip(dict(kwargs), db_path=db_path)


def get_clip_count(db_path: str | Path = DEFAULT_DB_PATH) -> int:
    with connect(db_path) as conn:
        return int(conn.execute("SELECT COUNT(*) FROM clips").fetchone()[0])


def _rows(sql: str, params: tuple = (), db_path: str | Path = DEFAULT_DB_PATH) -> list[dict]:
    with connect(db_path) as conn:
        return [dict(row) for row in conn.execute(sql, params).fetchall()]


def get_clip(clip_id: str, db_path: str | Path = DEFAULT_DB_PATH) -> dict | None:
    rows = _rows("SELECT * FROM clips WHERE clip_id = ?", (clip_id,), db_path)
    return rows[0] if rows else None


def find_clips(status: str | None = None, query: str | None = None, limit: int = 20, db_path: str | Path = DEFAULT_DB_PATH) -> list[dict]:
    clauses: list[str] = []
    params: list[object] = []
    if status:
        clauses.append("status = ?")
        params.append(status)
    if query:
        like = f"%{query.lower()}%"
        clauses.append("(" + " OR ".join(f"LOWER(COALESCE({col}, '')) LIKE ?" for col in TEXT_SEARCH_COLUMNS) + ")")
        params.extend([like] * len(TEXT_SEARCH_COLUMNS))
    sql = "SELECT * FROM clips" + (" WHERE " + " AND ".join(clauses) if clauses else "") + " ORDER BY created_at DESC LIMIT ?"
    return _rows(sql, (*params, limit), db_path)


def update_status(clip_id: str, status: str, human_decision: str | None = None, db_path: str | Path = DEFAULT_DB_PATH) -> bool:
    if status not in VALID_STATUSES:
        raise ValueError(f"invalid status: {status}")
    with connect(db_path) as conn:
        cur = conn.execute(
            "UPDATE clips SET status = ?, human_decision = COALESCE(?, human_decision), updated_at = ? WHERE clip_id = ?",
            (status, human_decision, utc_now(), clip_id),
        )
        return cur.rowcount > 0


def update_brief_path(clip_id: str, brief_path: str, db_path: str | Path = DEFAULT_DB_PATH) -> bool:
    with connect(db_path) as conn:
        cur = conn.execute("UPDATE clips SET brief_path = ?, updated_at = ? WHERE clip_id = ?", (brief_path, utc_now(), clip_id))
        return cur.rowcount > 0


def check_duplicate(source_url: str, start_sec: int, end_sec: int, db_path: str | Path = DEFAULT_DB_PATH) -> list[dict]:
    video = extract_youtube_id(source_url) or source_url
    return _rows(
        """
        SELECT * FROM clips
        WHERE (source_video_id = ? OR source_url = ?)
          AND NOT (end_sec <= ? OR start_sec >= ?)
        ORDER BY created_at DESC
        """,
        (video, source_url, start_sec, end_sec),
        db_path,
    )


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def check_novelty(summary: str, threshold: float = 0.8, db_path: str | Path = DEFAULT_DB_PATH) -> dict:
    matches = []
    for clip in find_clips(status="approved", limit=200, db_path=db_path):
        score = _similarity(summary, str(clip.get("moment_summary") or ""))
        if score >= threshold:
            matches.append({"clip_id": clip["clip_id"], "similarity_score": round(score, 3), "moment_summary": clip.get("moment_summary")})
    return {
        "novelty_status": "near_duplicate" if matches else "novel",
        "similarity_score": matches[0]["similarity_score"] if matches else 0,
        "similar_clips": matches,
    }


def init_db(db_path: str | Path = DEFAULT_DB_PATH) -> Path:
    with connect(db_path):
        return Path(db_path)


def before_clip_mine(topic_or_url: str, db_path: str | Path = DEFAULT_DB_PATH) -> dict:
    clips = find_clips(query=topic_or_url, db_path=db_path)
    return {"vault_check": "possible overlap" if clips else "no overlap", "matches": clips[:5]}


def format_timestamp(seconds: int) -> str:
    minutes, sec = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}:{minutes:02d}:{sec:02d}" if hours else f"{minutes}:{sec:02d}"


def youtube_timestamp_url(source_url: str, start_sec: int) -> str:
    return f"{source_url}{'&' if '?' in source_url else '?'}t={int(start_sec)}"


def youtube_embed_url(source_url: str, start_sec: int, end_sec: int) -> str | None:
    video = extract_youtube_id(source_url)
    return f"https://www.youtube.com/embed/{video}?start={int(start_sec)}&end={int(end_sec)}" if video else None


def _value(clip: dict, key: str, fallback: str = "Not specified") -> str:
    value = clip.get(key)
    return fallback if value in (None, "", []) else str(value)


def render_clip_brief(clip: dict) -> str:
    start = int(clip["start_sec"])
    end = int(clip["end_sec"])
    duration = int(clip.get("duration_seconds") or end - start)
    source_url = str(clip["source_url"])
    direct = youtube_timestamp_url(source_url, start)
    embed = youtube_embed_url(source_url, start, end) or "Not available"
    status = _value(clip, "status")
    clip_id = _value(clip, "clip_id")

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

## Background

{_value(clip, "source_title")} is the source video from {_value(clip, "source_channel_or_account")}. The selected moment matters because it connects to: {_value(clip, "trend_headline")}.

## Source Access

- Clip ID: {clip_id}
- Direct link: {direct}
- Embed preview: {embed}
- Source URL: {source_url}

## The Clip

| Field | Value |
|---|---|
| Start | {_value(clip, "start_timestamp", format_timestamp(start))} ({start}s) |
| End | {_value(clip, "end_timestamp", format_timestamp(end))} ({end}s) |
| Duration | {duration}s |
| Summary | {_value(clip, "moment_summary")} |
| Transcript quote | {_value(clip, "transcript_excerpt")} |

## Engagement Analytics

Views: {_value(clip, "view_count")}
Likes: {_value(clip, "like_count")}
Comments: {_value(clip, "comment_count")}
Velocity score: {_value(clip, "velocity_score")}

## Brand Gate

Brand angle: {_value(clip, "brand_angle")}
Brand score: {_value(clip, "brand_alignment_score")}
Blacklist flags: {_value(clip, "blacklist_flags", "none")}

## Platform Variants

- Instagram: {_value(clip, "suggested_caption")}
- LinkedIn: Use the operator lesson and source context.
- YouTube Shorts: Use the strongest quote as the hook.

## Why Post

{_value(clip, "why_post")}

## Human Gate

Review status: {_value(clip, "human_decision", "pending")}
"""


def main() -> None:
    print(f"Clip store ready: {init_db()}")


if __name__ == "__main__":
    main()
