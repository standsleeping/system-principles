"""Search command — full-text search across principles."""

import argparse
from pathlib import Path

from principles.search import SEARCHABLE_FIELDS, SearchHit, search_principles
from principles.translators import load_principles


def run_search(args: argparse.Namespace) -> int:
    """Execute the search command."""
    content_dir = Path(args.content_dir)

    principles, errors = load_principles(content_dir, recursive=False)
    if not principles:
        principles, errors = load_principles(content_dir, recursive=True)

    for err in errors:
        print(f"Warning: {err.message}")

    if not principles:
        print("No principles found.")
        return 0

    fields = (args.field,) if args.field else SEARCHABLE_FIELDS
    hits = search_principles(principles, args.query, fields=fields)

    if not hits:
        print(f'No matches for "{args.query}".')
        return 0

    limit = args.limit if args.limit > 0 else len(hits)
    _print_hits(hits[:limit], args.query)

    if len(hits) > limit:
        print(f"\n({len(hits) - limit} more — pass --limit to widen.)")
    else:
        print(f"\n{len(hits)} match{'es' if len(hits) != 1 else ''}.")

    return 0


def _print_hits(hits: list[SearchHit], query: str) -> None:
    """Render hits one per block: id, title, where it matched, essence."""
    needle = query.lower()
    for hit in hits:
        p = hit.principle
        print(f"{p.id}: {p.title}")
        print(f"  matched in: {', '.join(hit.fields)}")
        snippet = _snippet(p.essence, needle) if p.essence else ""
        if snippet:
            print(f"  {snippet}")
        print()


def _snippet(text: str, needle: str, radius: int = 60) -> str:
    """Show a window around the first occurrence of needle in text.

    Falls back to the leading slice if the needle isn't in this field.
    """
    lower = text.lower()
    idx = lower.find(needle)
    if idx == -1:
        return text if len(text) <= 2 * radius else text[: 2 * radius] + "…"
    start = max(0, idx - radius)
    end = min(len(text), idx + len(needle) + radius)
    prefix = "…" if start > 0 else ""
    suffix = "…" if end < len(text) else ""
    return f"{prefix}{text[start:end]}{suffix}"
