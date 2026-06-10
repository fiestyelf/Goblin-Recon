"""Normalize social signals before scoring."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


ROOT_DIR = Path(__file__).resolve().parents[2]
VAULT_DIR = ROOT_DIR / "vault"
DEFAULT_STORE_PATH = VAULT_DIR / "social-signals.jsonl"
SOCIAL_FIELDS = (
    "platform",
    "creator",
    "url",
    "published_date",
    "views",
    "likes",
    "comments",
    "shares",
    "caption",
    "hook",
    "format_type",
    "sound_trend",
    "topic",
    "category",
    "why_it_is_trending",
    "can_genx_adapt_this",
    "confidence",
    "access_status",
    "capture_method",
    "user_notes",
)
METRIC_FIELDS = {"views", "likes", "comments", "shares"}
ACCESS_STATUSES = {"api_ok", "public_ok", "manual_ok", "blocked", "partial", "unknown"}
CAPTURE_METHODS = {"approved_api", "public_browser", "manual_assisted", "unknown"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def infer_platform(url: str | None) -> str:
    if not url:
        return "unknown"
    host = urlparse(url).netloc.lower()
    if "instagram.com" in host:
        return "instagram"
    if "tiktok.com" in host:
        return "tiktok"
    if host in {"x.com", "twitter.com", "www.x.com", "www.twitter.com"}:
        return "x_twitter"
    if "reddit.com" in host:
        return "reddit"
    if "youtube.com" in host or "youtu.be" in host:
        return "youtube"
    if "linkedin.com" in host:
        return "linkedin"
    return "web"


def _clean_text(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _clean_int(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, str) and value.strip() == "":
        return None
    if isinstance(value, int):
        return value if value >= 0 else None
    if isinstance(value, float):
        return int(value) if value >= 0 else None
    if isinstance(value, str):
        text = value.replace(",", "").strip().lower()
        match = re.fullmatch(r"(\d+(?:\.\d+)?)\s*([kmb])?(?:\s+[a-z]+)?", text)
        if not match:
            return None
        number = float(match.group(1))
        multiplier = {"k": 1_000, "m": 1_000_000, "b": 1_000_000_000}.get(match.group(2), 1)
        return int(number * multiplier)
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _metric_was_provided(value: object) -> bool:
    return value is not None and not (isinstance(value, str) and value.strip() == "")


def _normalize_access_status(value: object) -> str:
    status = _clean_text(value) or "unknown"
    return status if status in ACCESS_STATUSES else "unknown"


def _normalize_capture_method(value: object) -> str:
    method = _clean_text(value) or "unknown"
    return method if method in CAPTURE_METHODS else "unknown"


def normalize_social_record(record: dict) -> dict:
    normalized = {field: None for field in SOCIAL_FIELDS}
    for field in SOCIAL_FIELDS:
        if field in record:
            normalized[field] = record[field]

    normalized["url"] = _clean_text(normalized.get("url"))
    normalized["platform"] = _clean_text(normalized.get("platform")) or infer_platform(normalized["url"])
    normalized["access_status"] = _normalize_access_status(normalized.get("access_status"))
    normalized["capture_method"] = _normalize_capture_method(normalized.get("capture_method"))

    invalid_metrics = []
    for field in METRIC_FIELDS:
        raw_value = normalized.get(field)
        normalized[field] = _clean_int(raw_value)
        if _metric_was_provided(raw_value) and normalized[field] is None:
            invalid_metrics.append(field)

    for field in SOCIAL_FIELDS:
        if field not in METRIC_FIELDS and field not in {"access_status", "capture_method"}:
            normalized[field] = _clean_text(normalized.get(field))

    normalized["captured_at"] = _clean_text(record.get("captured_at")) or utc_now()
    normalized["source_type"] = "social_signal"
    normalized["validation"] = validate_social_record(normalized, invalid_metrics)
    normalized["recommendation"] = recommend_next_step(normalized)
    return normalized


def validate_social_record(record: dict, invalid_metrics: list[str] | None = None) -> dict:
    missing = []
    warnings = []
    invalid_metrics = invalid_metrics or []
    for field in ("platform", "url", "published_date", "topic", "access_status"):
        if not record.get(field):
            missing.append(field)
    if record.get("access_status") == "blocked":
        warnings.append("source blocked; use manual assisted input only if essential")
    if not any(record.get(field) is not None for field in METRIC_FIELDS):
        warnings.append("no visible metrics captured")
    if not any(record.get(field) for field in ("caption", "hook", "user_notes")):
        warnings.append("caption, hook, or user_notes needed for scoring")
    if invalid_metrics:
        warnings.append("invalid metric values rejected: " + ", ".join(sorted(invalid_metrics)))
    return {
        "ok": not missing and not invalid_metrics,
        "missing": missing,
        "warnings": warnings,
        "invalid_metrics": sorted(invalid_metrics),
    }


def recommend_next_step(record: dict) -> str:
    validation = record.get("validation") or validate_social_record(record)
    if "url" in validation["missing"]:
        return "shelve"
    if record.get("access_status") == "blocked" and not record.get("user_notes"):
        return "manual_assisted_input"
    if not validation["ok"]:
        return "needs_review"
    if record.get("platform") == "youtube" and record.get("url") and record.get("topic"):
        return "move_to_clip_mine"
    if record.get("topic") and any(record.get(field) for field in ("caption", "hook", "format_type", "user_notes")):
        return "use_in_social_pulse"
    return "needs_review"


def load_records(path: str | Path) -> list[dict]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list):
        if not all(isinstance(item, dict) for item in data):
            raise ValueError("input JSON list must contain only objects")
        return data
    if isinstance(data, dict):
        return [data]
    raise ValueError("input JSON must be an object or list of objects")


def append_records(records: list[dict], store_path: str | Path = DEFAULT_STORE_PATH) -> Path:
    store_path = Path(store_path)
    store_path.parent.mkdir(parents=True, exist_ok=True)
    with store_path.open("a", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return store_path


def _print_json(data: object) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True))


def _records_from_args(args: argparse.Namespace) -> list[dict]:
    if args.input:
        raw_records = load_records(args.input)
    else:
        raw_records = [
            {
                "platform": args.platform,
                "creator": args.creator,
                "url": args.url,
                "published_date": args.published_date,
                "views": args.views,
                "likes": args.likes,
                "comments": args.comments,
                "shares": args.shares,
                "caption": args.caption,
                "hook": args.hook,
                "format_type": args.format_type,
                "sound_trend": args.sound_trend,
                "topic": args.topic,
                "category": args.category,
                "why_it_is_trending": args.why_it_is_trending,
                "can_genx_adapt_this": args.can_genx_adapt_this,
                "confidence": args.confidence,
                "access_status": args.access_status,
                "capture_method": args.capture_method,
                "user_notes": args.user_notes,
            }
        ]
    return [normalize_social_record(record) for record in raw_records]


def normalize_command(args: argparse.Namespace) -> int:
    records = _records_from_args(args)
    invalid_records = [record for record in records if not record["validation"]["ok"]]
    if invalid_records:
        _print_json(records if len(records) != 1 else records[0])
        print("Invalid social signal(s); not stored.", file=sys.stderr)
        return 1
    if args.store:
        path = append_records(records, args.store)
        print(f"Stored {len(records)} social signal(s): {path}")
    else:
        _print_json(records if len(records) != 1 else records[0])
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Normalize social signals from APIs, public pages, or manual inputs."
    )
    parser.add_argument("--input", help="JSON object/list with social signal fields.")
    parser.add_argument("--store", nargs="?", const=str(DEFAULT_STORE_PATH), help="Append JSONL to store path.")
    parser.add_argument("--platform")
    parser.add_argument("--creator")
    parser.add_argument("--url")
    parser.add_argument("--published-date")
    parser.add_argument("--views")
    parser.add_argument("--likes")
    parser.add_argument("--comments")
    parser.add_argument("--shares")
    parser.add_argument("--caption")
    parser.add_argument("--hook")
    parser.add_argument("--format-type")
    parser.add_argument("--sound-trend")
    parser.add_argument("--topic")
    parser.add_argument("--category")
    parser.add_argument("--why-it-is-trending")
    parser.add_argument("--can-genx-adapt-this")
    parser.add_argument("--confidence")
    parser.add_argument("--access-status", default="manual_ok", choices=sorted(ACCESS_STATUSES))
    parser.add_argument("--capture-method", default="manual_assisted", choices=sorted(CAPTURE_METHODS))
    parser.add_argument("--user-notes")
    parser.set_defaults(func=normalize_command)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
