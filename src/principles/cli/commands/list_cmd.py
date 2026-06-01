"""List command - display principles with optional filtering."""

import argparse
from pathlib import Path

from principles.translators import load_principles
from principles.translators.set_loader import load_set
from principles.translators.taxonomy_loader import load_taxonomy
from principles.types import (
    GroupPath,
    ParseError,
    Principle,
    PrincipleId,
    PrincipleSet,
    Taxonomy,
    TaxonomyGroup,
    ValidationError,
)


def _format_error(error: ParseError | ValidationError) -> str:
    """Format an error for display."""
    if isinstance(error, ParseError):
        return f"{error.message} ({error.file_path})"
    else:
        prefix = f"[{error.principle_id}] " if error.principle_id else ""
        return f"{prefix}{error.message}"


def run_list(args: argparse.Namespace) -> int:
    """Execute the list command."""
    content_dir = Path(args.content_dir)
    sets_dir = Path(args.sets_dir)
    taxonomies_dir = Path(args.taxonomies_dir)

    # Load all principles (try flat first, fall back to recursive for migration)
    principles, errors = load_principles(content_dir, recursive=False)
    if not principles:
        # Try recursive for backward compatibility during migration
        principles, errors = load_principles(content_dir, recursive=True)

    if errors:
        for error in errors:
            print(f"Warning: {_format_error(error)}")

    if not principles:
        print("No principles found.")
        return 0

    # Build lookup map
    principle_map: dict[PrincipleId, Principle] = {p.id: p for p in principles}

    # Load taxonomy if specified and not flat mode
    taxonomy: Taxonomy | None = None
    if not args.flat and args.taxonomy:
        taxonomy_path = taxonomies_dir / f"{args.taxonomy}.yaml"
        taxonomy_result = load_taxonomy(taxonomy_path)
        if isinstance(taxonomy_result, Taxonomy):
            taxonomy = taxonomy_result
        else:
            print(
                f"Warning: Could not load taxonomy '{args.taxonomy}': {taxonomy_result.message}"
            )

    # Filter by group path if specified (requires taxonomy)
    if args.group and taxonomy:
        allowed_ids = taxonomy.get_principles_by_path(GroupPath(args.group))
        principles = [p for p in principles if p.id in allowed_ids]

    # Filter by set if specified
    if args.set_name:
        set_path = sets_dir / f"{args.set_name}.yaml"
        set_result = load_set(set_path)
        if isinstance(set_result, PrincipleSet):
            allowed_ids = set(set_result.principle_ids)
            principles = [p for p in principles if p.id in allowed_ids]
        else:
            print(f"Error loading set: {set_result.message}")
            return 1

    # Display results
    if args.flat or taxonomy is None:
        _display_flat(principles)
    else:
        _display_with_taxonomy(principles, taxonomy, principle_map)

    return 0


def _display_flat(principles: list[Principle]) -> None:
    """Display principles as a flat list."""
    if not principles:
        print("No principles match the filter.")
        return

    for p in principles:
        print(f"  {p.id}: {p.title}")

    print(f"\nTotal: {len(principles)} principles")


def _display_with_taxonomy(
    principles: list[Principle],
    taxonomy: Taxonomy,
    principle_map: dict[PrincipleId, Principle],
) -> None:
    """Display principles grouped by taxonomy structure."""
    if not principles:
        print("No principles match the filter.")
        return

    # Build set of principle IDs we want to display
    display_ids = {p.id for p in principles}

    def display_group(group: TaxonomyGroup, depth: int) -> int:
        """Recursively display a group and its subgroups. Returns count displayed."""
        count = 0
        header_printed = False

        # Display principles in this group
        for pid in group.principle_ids:
            if pid in display_ids and pid in principle_map:
                if not header_printed:
                    prefix = "#" * (depth + 1)
                    print(f"\n{prefix} {group.name.replace('-', ' ').title()}")
                    header_printed = True
                p = principle_map[pid]
                print(f"  {p.id}: {p.title}")
                count += 1

        # Display subgroups
        for subgroup in group.subgroups:
            subcount = display_group(subgroup, depth + 1)
            count += subcount

        return count

    total = 0
    for group in taxonomy.groups:
        total += display_group(group, 1)

    # Show any principles not in taxonomy
    taxonomy_ids = taxonomy.get_all_principle_ids()
    uncategorized = [p for p in principles if p.id not in taxonomy_ids]
    if uncategorized:
        print("\n## Uncategorized")
        for p in uncategorized:
            print(f"  {p.id}: {p.title}")
        total += len(uncategorized)

    print(f"\nTotal: {total} principles")
