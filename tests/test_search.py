"""Unit tests for principle search."""

from principles.search import search_principles
from principles.types import Principle, PrincipleId


def _principle(
    pid: str,
    title: str = "Title",
    essence: str = "Essence text.",
    content: str = "Body content.",
    tags: tuple[str, ...] = (),
) -> Principle:
    return Principle(
        id=PrincipleId(pid),
        title=title,
        essence=essence,
        content=content,
        tags=tags,
    )


def test_empty_query_returns_no_hits() -> None:
    assert search_principles([_principle("FOO")], "") == []
    assert search_principles([_principle("FOO")], "   ") == []


def test_substring_match_in_title() -> None:
    p = _principle("FOO", title="Patterns of Dispatch")
    hits = search_principles([p], "dispatch")
    assert len(hits) == 1
    assert "title" in hits[0].fields


def test_substring_match_is_case_insensitive() -> None:
    p = _principle("FOO", essence="The Quick Brown Fox.")
    hits = search_principles([p], "QUICK")
    assert len(hits) == 1
    assert "essence" in hits[0].fields


def test_match_in_id() -> None:
    p = _principle("DATA_DRIVEN_DISPATCH", title="x", essence="x", content="x")
    hits = search_principles([p], "DRIVEN")
    assert len(hits) == 1
    assert "id" in hits[0].fields


def test_match_in_tags() -> None:
    p = _principle("FOO", tags=("python", "types"))
    hits = search_principles([p], "python")
    assert len(hits) == 1
    assert "tags" in hits[0].fields


def test_match_in_content_only() -> None:
    p = _principle("FOO", title="x", essence="x", content="Mentions immutability somewhere.")
    hits = search_principles([p], "immutability")
    assert len(hits) == 1
    assert hits[0].fields == ("content",)


def test_no_match_returns_empty() -> None:
    p = _principle("FOO")
    assert search_principles([p], "nothing-matches") == []


def test_title_match_sorts_before_content_only_match() -> None:
    title_match = _principle("AAA", title="dispatch tables")
    content_match = _principle("ZZZ", content="something about dispatch")
    hits = search_principles([content_match, title_match], "dispatch")
    assert [h.principle.id for h in hits] == ["AAA", "ZZZ"]


def test_field_restriction() -> None:
    p = _principle("FOO", title="dispatch", essence="dispatch", content="dispatch")
    hits = search_principles([p], "dispatch", fields=("title",))
    assert len(hits) == 1
    assert hits[0].fields == ("title",)


def test_alphabetical_within_same_priority() -> None:
    a = _principle("ZULU", title="Pattern A")
    b = _principle("ALPHA", title="Pattern B")
    hits = search_principles([a, b], "Pattern")
    assert [h.principle.id for h in hits] == ["ALPHA", "ZULU"]
