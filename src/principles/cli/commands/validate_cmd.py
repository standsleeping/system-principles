"""Validate command — lint principles, taxonomies, and sets for broken references."""

import argparse
from pathlib import Path

from principles.translators import load_principles
from principles.translators.set_loader import load_set
from principles.translators.taxonomy_loader import load_taxonomy
from principles.types import (
    ParseError,
    Principle,
    PrincipleId,
    PrincipleSet,
    Taxonomy,
    ValidationError,
)
from principles.validation import (
    CheckFinding,
    check_duplicate_ids,
    check_filename_consistency,
    check_related_references,
    check_set_references,
    check_taxonomy_references,
)


def run_validate(args: argparse.Namespace) -> int:
    """Execute the validate command. Returns 0 if everything passes, 1 otherwise."""
    content_dir = Path(args.content_dir)
    taxonomies_dir = Path(args.taxonomies_dir)
    sets_dir = Path(args.sets_dir)

    sections: list[tuple[str, tuple[CheckFinding, ...]]] = []

    principles_list, load_errors = load_principles(content_dir, recursive=False)
    if not principles_list:
        principles_list, load_errors = load_principles(content_dir, recursive=True)

    sections.append(("Loadability", _load_errors_to_findings(load_errors)))

    id_to_paths = _index_files_by_id(content_dir)
    principles: dict[PrincipleId, Principle] = {p.id: p for p in principles_list}

    sections.append(("Duplicate IDs", check_duplicate_ids(id_to_paths)))
    sections.append(("Filename consistency", check_filename_consistency(id_to_paths)))
    sections.append(("Related references", check_related_references(principles)))

    known_ids = set(principles)

    for tax_path in sorted(taxonomies_dir.glob("*.yaml")):
        result = load_taxonomy(tax_path)
        section_name = f"Taxonomy references ({tax_path.stem})"
        if isinstance(result, Taxonomy):
            sections.append((section_name, check_taxonomy_references(result, known_ids)))
        else:
            sections.append((section_name, (_parse_error_to_finding(result, "taxonomy"),)))

    for set_path in sorted(sets_dir.glob("*.yaml")):
        result = load_set(set_path)
        section_name = f"Set references ({set_path.stem})"
        if isinstance(result, PrincipleSet):
            sections.append((section_name, check_set_references(result, known_ids)))
        else:
            sections.append((section_name, (_parse_error_to_finding(result, "set"),)))

    total_failures = sum(len(findings) for _, findings in sections)
    _print_report(sections, total_failures)

    return 0 if total_failures == 0 else 1


def _index_files_by_id(content_dir: Path) -> dict[PrincipleId, list[Path]]:
    """Map every principle id to the files that declare it.

    Re-parses frontmatter so duplicate ids across files are still indexed
    (load_principles only retains one per id).
    """
    from principles.translators.frontmatter import parse_frontmatter

    index: dict[PrincipleId, list[Path]] = {}
    if not content_dir.exists():
        return index

    for path in content_dir.glob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        result = parse_frontmatter(text, str(path))
        if isinstance(result, ParseError):
            continue
        raw_id = result.metadata.get("id")
        if raw_id is None:
            continue
        pid = PrincipleId(str(raw_id))
        index.setdefault(pid, []).append(path)
    return index


def _load_errors_to_findings(
    errors: list[ParseError | ValidationError],
) -> tuple[CheckFinding, ...]:
    findings: list[CheckFinding] = []
    for err in errors:
        if isinstance(err, ParseError):
            findings.append(
                CheckFinding(
                    check="loadability",
                    message=err.message,
                    location=err.file_path,
                )
            )
        else:
            findings.append(
                CheckFinding(
                    check="loadability",
                    message=err.message,
                    principle_id=str(err.principle_id) if err.principle_id else None,
                )
            )
    return tuple(findings)


def _parse_error_to_finding(err: ParseError, kind: str) -> CheckFinding:
    return CheckFinding(
        check=f"{kind}-load",
        message=err.message,
        location=err.file_path,
    )


def _print_report(
    sections: list[tuple[str, tuple[CheckFinding, ...]]],
    total_failures: int,
) -> None:
    print("Validation report")
    print("─────────────────")
    for name, findings in sections:
        if not findings:
            print(f"  ✓ {name}")
            continue
        print(f"  ✗ {name} — {len(findings)} finding(s):")
        for f in findings:
            prefix = f"[{f.principle_id}] " if f.principle_id else ""
            suffix = f" ({f.location})" if f.location else ""
            print(f"      {prefix}{f.message}{suffix}")
    print()
    print("All checks passed." if total_failures == 0 else f"{total_failures} finding(s).")
