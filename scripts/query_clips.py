#!/usr/bin/env python3
"""
Goblin Recon - Clip Store CLI

Search local Clip Mine history, update clip status, and export stored clips as
editor-ready markdown briefs.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from clip_store import (
    DEFAULT_DB_PATH,
    VALID_STATUSES,
    find_clips,
    get_clip,
    init_db,
    render_clip_brief,
    update_brief_path,
    update_status,
)


def _db_path(value: str | None) -> Path:
    return Path(value) if value else DEFAULT_DB_PATH


def _print_json(data: object) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def _print_table(clips: list[dict]) -> None:
    if not clips:
        print("No clips found.")
        return

    rows = []
    for clip in clips:
        rows.append(
            (
                clip["clip_id"],
                clip["status"],
                str(clip.get("brand_angle") or ""),
                str(clip.get("duration_seconds") or ""),
                str(clip.get("trend_headline") or clip.get("source_title") or "")[:64],
            )
        )

    headers = ("clip_id", "status", "angle", "secs", "headline/source")
    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    def render(row: tuple[str, ...]) -> str:
        return "  ".join(value.ljust(widths[index]) for index, value in enumerate(row))

    print(render(headers))
    print(render(tuple("-" * width for width in widths)))
    for row in rows:
        print(render(row))


def list_clips(args: argparse.Namespace) -> int:
    clips = find_clips(
        status=args.status,
        query=args.query,
        limit=args.limit,
        db_path=_db_path(args.db),
    )
    if args.json:
        _print_json(clips)
    else:
        _print_table(clips)
    return 0


def show_clip(args: argparse.Namespace) -> int:
    clip = get_clip(args.clip_id, _db_path(args.db))
    if not clip:
        print(f"Clip not found: {args.clip_id}")
        return 1
    _print_json(clip)
    return 0


def set_status(args: argparse.Namespace) -> int:
    updated = update_status(
        args.clip_id,
        args.status,
        human_decision=args.decision,
        db_path=_db_path(args.db),
    )
    if not updated:
        print(f"Clip not found: {args.clip_id}")
        return 1
    print(f"Updated {args.clip_id} -> {args.status}")
    return 0


def export_brief(args: argparse.Namespace) -> int:
    clip = get_clip(args.clip_id, _db_path(args.db))
    if not clip:
        print(f"Clip not found: {args.clip_id}")
        return 1
    if args.output:
        output = Path(args.output)
        clip["brief_path"] = str(output)
        brief = render_clip_brief(clip)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(brief, encoding="utf-8")
        update_brief_path(args.clip_id, str(output), db_path=_db_path(args.db))
        print(f"Brief written: {output}")
    else:
        brief = render_clip_brief(clip)
        print(brief)
    return 0


def init_store(args: argparse.Namespace) -> int:
    path = init_db(_db_path(args.db))
    print(f"Clip store ready: {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search and manage local Clip Mine history.")
    parser.add_argument("--db", help="Path to clips.db. Defaults to vault/clips.db.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize the local clip database.")
    init_parser.set_defaults(func=init_store)

    list_parser = subparsers.add_parser("list", help="List or search clips.")
    list_parser.add_argument("--status", choices=sorted(VALID_STATUSES), help="Filter by status.")
    list_parser.add_argument("--query", help="Full-text search query.")
    list_parser.add_argument("--limit", type=int, default=20, help="Maximum clips to return.")
    list_parser.add_argument("--json", action="store_true", help="Print raw JSON records.")
    list_parser.set_defaults(func=list_clips)

    show_parser = subparsers.add_parser("show", help="Show one clip as JSON.")
    show_parser.add_argument("clip_id")
    show_parser.set_defaults(func=show_clip)

    status_parser = subparsers.add_parser("update-status", help="Update a clip workflow status.")
    status_parser.add_argument("clip_id")
    status_parser.add_argument("status", choices=sorted(VALID_STATUSES))
    status_parser.add_argument("--decision", help="Optional human decision note.")
    status_parser.set_defaults(func=set_status)

    brief_parser = subparsers.add_parser("brief", help="Export a stored clip as markdown brief.")
    brief_parser.add_argument("clip_id")
    brief_parser.add_argument("--output", help="Write markdown brief to this path instead of stdout.")
    brief_parser.set_defaults(func=export_brief)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
