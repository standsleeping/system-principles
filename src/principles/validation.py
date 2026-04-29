"""Validation checks over principles, taxonomies, and sets.

Each check function takes already-loaded data and returns a tuple of findings.
Checks are pure: they do not load files, do not print, and do not raise.
The CLI command (validate_cmd) is responsible for loading inputs and rendering
the report.
"""

from dataclasses import dataclass
from pathlib import Path

from principles.types import (
    Principle,
    PrincipleId,
    PrincipleSet,
    Taxonomy,
    TaxonomyGroup,
)


@dataclass(frozen=True, slots=True)
class CheckFinding:
    """A single validation finding. Always represents a problem."""

    check: str
    message: str
    principle_id: str | None = None
    location: str | None = None


def _all_taxonomy_principle_ids(
    group: TaxonomyGroup,
    prefix: str,
) -> tuple[tuple[PrincipleId, str], ...]:
    """Walk a group recursively, yielding (principle_id, group_path) pairs."""
    here = f"{prefix}/{group.name}" if prefix else group.name
    pairs: list[tuple[PrincipleId, str]] = [(pid, here) for pid in group.principle_ids]
    for sub in group.subgroups:
        pairs.extend(_all_taxonomy_principle_ids(sub, here))
    return tuple(pairs)


def check_duplicate_ids(
    id_to_paths: dict[PrincipleId, list[Path]],
) -> tuple[CheckFinding, ...]:
    """Flag any principle ID that appears in more than one file."""
    findings: list[CheckFinding] = []
    for pid, paths in id_to_paths.items():
        if len(paths) > 1:
            files = ", ".join(p.name for p in paths)
            findings.append(
                CheckFinding(
                    check="duplicate-ids",
                    message=f"id {pid} declared in multiple files: {files}",
                    principle_id=pid,
                )
            )
    return tuple(findings)


def check_filename_consistency(
    id_to_paths: dict[PrincipleId, list[Path]],
) -> tuple[CheckFinding, ...]:
    """Filename stem (without .md) must equal id.lower()."""
    findings: list[CheckFinding] = []
    for pid, paths in id_to_paths.items():
        expected = pid.lower()
        for path in paths:
            if path.stem != expected:
                findings.append(
                    CheckFinding(
                        check="filename-consistency",
                        message=f"id {pid} expects filename {expected}.md, found {path.name}",
                        principle_id=pid,
                        location=path.name,
                    )
                )
    return tuple(findings)


def check_related_references(
    principles: dict[PrincipleId, Principle],
) -> tuple[CheckFinding, ...]:
    """Every id in a principle's `related` must exist; no self-references."""
    findings: list[CheckFinding] = []
    known = set(principles)
    for pid, p in principles.items():
        for rel in p.related:
            if rel == pid:
                findings.append(
                    CheckFinding(
                        check="related-references",
                        message=f"{pid} lists itself in related",
                        principle_id=pid,
                    )
                )
                continue
            if rel not in known:
                findings.append(
                    CheckFinding(
                        check="related-references",
                        message=f"{pid} references unknown principle {rel}",
                        principle_id=pid,
                    )
                )
    return tuple(findings)


def check_taxonomy_references(
    taxonomy: Taxonomy,
    known_ids: set[PrincipleId],
) -> tuple[CheckFinding, ...]:
    """Every principle id listed in a taxonomy group must exist in content."""
    findings: list[CheckFinding] = []
    for group in taxonomy.groups:
        for pid, group_path in _all_taxonomy_principle_ids(group, ""):
            if pid not in known_ids:
                findings.append(
                    CheckFinding(
                        check="taxonomy-references",
                        message=f"taxonomy {taxonomy.name} group {group_path} references unknown principle {pid}",
                        principle_id=pid,
                        location=f"{taxonomy.name}:{group_path}",
                    )
                )
    return tuple(findings)


def check_set_references(
    principle_set: PrincipleSet,
    known_ids: set[PrincipleId],
) -> tuple[CheckFinding, ...]:
    """Every principle id listed in a set must exist in content."""
    findings: list[CheckFinding] = []
    for pid in principle_set.principle_ids:
        if pid not in known_ids:
            findings.append(
                CheckFinding(
                    check="set-references",
                    message=f"set {principle_set.name} references unknown principle {pid}",
                    principle_id=pid,
                    location=str(principle_set.name),
                )
            )
    return tuple(findings)
