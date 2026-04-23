"""Tests for site template helpers."""

from principles.site.templates import find_container
from principles.types import PrincipleId, Taxonomy, TaxonomyGroup, TaxonomyName


def _make_taxonomy(groups: tuple[TaxonomyGroup, ...]) -> Taxonomy:
    return Taxonomy(
        name=TaxonomyName("test"),
        description="",
        groups=groups,
    )


# === find_container ===


def test_find_container_direct_group() -> None:
    """Locates a principle that lives directly in a top-level group."""
    pid = PrincipleId("ALPHA")
    group = TaxonomyGroup(name="types", principle_ids=(pid,))
    taxonomy = _make_taxonomy((group,))

    found, path = find_container(pid, taxonomy)
    assert found is group
    assert path == ("types",)


def test_find_container_nested_subgroup() -> None:
    """Locates a principle inside a subgroup and returns the full path."""
    pid = PrincipleId("BETA")
    subgroup = TaxonomyGroup(name="abstraction", principle_ids=(pid,))
    group = TaxonomyGroup(name="conceptual", subgroups=(subgroup,))
    taxonomy = _make_taxonomy((group,))

    found, path = find_container(pid, taxonomy)
    assert found is subgroup
    assert path == ("conceptual", "abstraction")


def test_find_container_returns_innermost() -> None:
    """When a principle appears in both a group and its subgroup, returns the group's copy first."""
    pid = PrincipleId("GAMMA")
    subgroup = TaxonomyGroup(name="inner", principle_ids=(pid,))
    group = TaxonomyGroup(name="outer", principle_ids=(pid,), subgroups=(subgroup,))
    taxonomy = _make_taxonomy((group,))

    found, path = find_container(pid, taxonomy)
    # Outer match is found first during the walk.
    assert found is group
    assert path == ("outer",)


def test_find_container_not_found() -> None:
    """Returns (None, ()) when the principle is absent from the taxonomy."""
    pid = PrincipleId("MISSING")
    group = TaxonomyGroup(name="types", principle_ids=(PrincipleId("OTHER"),))
    taxonomy = _make_taxonomy((group,))

    found, path = find_container(pid, taxonomy)
    assert found is None
    assert path == ()


def test_find_container_deep_nesting() -> None:
    """Walks beyond one subgroup level when needed."""
    pid = PrincipleId("DELTA")
    leaf = TaxonomyGroup(name="leaf", principle_ids=(pid,))
    mid = TaxonomyGroup(name="mid", subgroups=(leaf,))
    root = TaxonomyGroup(name="root", subgroups=(mid,))
    taxonomy = _make_taxonomy((root,))

    found, path = find_container(pid, taxonomy)
    assert found is leaf
    assert path == ("root", "mid", "leaf")
