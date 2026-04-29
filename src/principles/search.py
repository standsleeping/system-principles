"""Full-text search across principles.

Pure substring search over id, title, essence, content, and tags.
No I/O, no external indexes; the principle list is small enough that
linear scan is fine.
"""

from dataclasses import dataclass

from principles.types import Principle


SEARCHABLE_FIELDS = ("id", "title", "essence", "content", "tags")


@dataclass(frozen=True, slots=True)
class SearchHit:
    """One principle that matched a query, with the fields where it matched."""

    principle: Principle
    fields: tuple[str, ...]


def _field_text(principle: Principle, field: str) -> str:
    if field == "id":
        return str(principle.id)
    if field == "title":
        return principle.title
    if field == "essence":
        return principle.essence
    if field == "content":
        return principle.content
    if field == "tags":
        return " ".join(principle.tags)
    return ""


def _field_priority(field: str) -> int:
    """Lower number sorts earlier. Title beats essence beats content."""
    return {"title": 0, "id": 0, "essence": 1, "tags": 2, "content": 3}.get(field, 4)


def search_principles(
    principles: list[Principle],
    query: str,
    fields: tuple[str, ...] = SEARCHABLE_FIELDS,
) -> list[SearchHit]:
    """Return principles whose searchable text contains the query.

    Matching is case-insensitive substring. Results are sorted by best match
    field (title/id, then essence, then tags, then content), then by id.
    """
    needle = query.strip().lower()
    if not needle:
        return []

    hits: list[SearchHit] = []
    for p in principles:
        matched: list[str] = []
        for field in fields:
            if needle in _field_text(p, field).lower():
                matched.append(field)
        if matched:
            hits.append(SearchHit(principle=p, fields=tuple(matched)))

    def sort_key(hit: SearchHit) -> tuple[int, str]:
        best = min(_field_priority(f) for f in hit.fields)
        return (best, str(hit.principle.id))

    hits.sort(key=sort_key)
    return hits
