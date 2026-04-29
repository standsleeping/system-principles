"""Unit tests for validation check functions."""

from pathlib import Path

from principles.types import (
    Principle,
    PrincipleId,
    PrincipleSet,
    SetName,
    Taxonomy,
    TaxonomyGroup,
    TaxonomyName,
)
from principles.validation import (
    check_duplicate_ids,
    check_filename_consistency,
    check_related_references,
    check_set_references,
    check_taxonomy_references,
)


def _principle(
    pid: str,
    related: tuple[str, ...] = (),
) -> Principle:
    return Principle(
        id=PrincipleId(pid),
        title=f"{pid} title",
        essence="essence",
        content="body",
        related=tuple(PrincipleId(r) for r in related),
    )


def test_duplicate_ids_passes_when_unique() -> None:
    index: dict[PrincipleId, list[Path]] = {
        PrincipleId("FOO"): [Path("foo.md")],
        PrincipleId("BAR"): [Path("bar.md")],
    }
    assert check_duplicate_ids(index) == ()


def test_duplicate_ids_flags_collisions() -> None:
    index: dict[PrincipleId, list[Path]] = {
        PrincipleId("FOO"): [Path("foo.md"), Path("foo_alt.md")],
    }
    findings = check_duplicate_ids(index)
    assert len(findings) == 1
    assert findings[0].principle_id == "FOO"
    assert "foo.md" in findings[0].message
    assert "foo_alt.md" in findings[0].message


def test_filename_consistency_passes_when_lowercase_matches() -> None:
    index: dict[PrincipleId, list[Path]] = {
        PrincipleId("TABLE_CELL_DISCIPLINE"): [Path("table_cell_discipline.md")],
    }
    assert check_filename_consistency(index) == ()


def test_filename_consistency_flags_mismatch() -> None:
    index: dict[PrincipleId, list[Path]] = {
        PrincipleId("FOO_BAR"): [Path("wrong_name.md")],
    }
    findings = check_filename_consistency(index)
    assert len(findings) == 1
    assert findings[0].principle_id == "FOO_BAR"
    assert "wrong_name.md" in findings[0].message


def test_related_references_passes_for_valid_refs() -> None:
    principles: dict[PrincipleId, Principle] = {
        PrincipleId("A"): _principle("A", related=("B",)),
        PrincipleId("B"): _principle("B"),
    }
    assert check_related_references(principles) == ()


def test_related_references_flags_unknown() -> None:
    principles: dict[PrincipleId, Principle] = {
        PrincipleId("A"): _principle("A", related=("GHOST",)),
    }
    findings = check_related_references(principles)
    assert len(findings) == 1
    assert findings[0].principle_id == "A"
    assert "GHOST" in findings[0].message


def test_related_references_flags_self_reference() -> None:
    principles: dict[PrincipleId, Principle] = {
        PrincipleId("A"): _principle("A", related=("A",)),
    }
    findings = check_related_references(principles)
    assert len(findings) == 1
    assert "itself" in findings[0].message


def test_taxonomy_references_passes_when_all_resolve() -> None:
    taxonomy = Taxonomy(
        name=TaxonomyName("test"),
        description="",
        groups=(
            TaxonomyGroup(
                name="g",
                principle_ids=(PrincipleId("A"),),
            ),
        ),
    )
    findings = check_taxonomy_references(taxonomy, {PrincipleId("A")})
    assert findings == ()


def test_taxonomy_references_flags_unknown_in_subgroup() -> None:
    taxonomy = Taxonomy(
        name=TaxonomyName("test"),
        description="",
        groups=(
            TaxonomyGroup(
                name="g",
                subgroups=(
                    TaxonomyGroup(name="sub", principle_ids=(PrincipleId("GHOST"),)),
                ),
            ),
        ),
    )
    findings = check_taxonomy_references(taxonomy, {PrincipleId("A")})
    assert len(findings) == 1
    assert findings[0].principle_id == "GHOST"
    assert "g/sub" in findings[0].message


def test_set_references_passes_when_all_resolve() -> None:
    pset = PrincipleSet(
        name=SetName("core"),
        description="",
        principle_ids=(PrincipleId("A"), PrincipleId("B")),
    )
    findings = check_set_references(pset, {PrincipleId("A"), PrincipleId("B")})
    assert findings == ()


def test_set_references_flags_unknown() -> None:
    pset = PrincipleSet(
        name=SetName("core"),
        description="",
        principle_ids=(PrincipleId("GHOST"),),
    )
    findings = check_set_references(pset, {PrincipleId("A")})
    assert len(findings) == 1
    assert findings[0].principle_id == "GHOST"
