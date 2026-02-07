"""Show command - display a single principle in detail."""

import argparse
from pathlib import Path

from principles.translators import load_principles
from principles.translators.taxonomy_loader import load_taxonomies
from principles.types import Principle, PrincipleId, Taxonomy


def run_show(args: argparse.Namespace) -> int:
    """Execute the show command."""
    content_dir = Path(args.content_dir)
    taxonomies_dir = Path(args.taxonomies_dir)
    principle_id = PrincipleId(args.id.upper())

    # Load all principles (try flat first, fall back to recursive for migration)
    principles, errors = load_principles(content_dir, recursive=False)
    if not principles:
        # Try recursive for backward compatibility during migration
        principles, errors = load_principles(content_dir, recursive=True)

    # Find by ID
    matching = [p for p in principles if p.id == principle_id]

    if not matching:
        print(f"Principle not found: {principle_id}")
        if errors:
            print("\nThere were errors loading some principles:")
            for error in errors:
                print(f"  - {error.message}")
        return 1

    principle = matching[0]

    # Load taxonomies for context
    taxonomies, _ = load_taxonomies(taxonomies_dir)

    _display_principle(principle, taxonomies)

    return 0


def _display_principle(principle: Principle, taxonomies: list[Taxonomy]) -> None:
    """Display a single principle in detail."""
    print(f"# [{principle.id}] {principle.title}")
    print()

    # Show where this principle appears in taxonomies
    for taxonomy in taxonomies:
        paths = taxonomy.get_paths_for_principle(principle.id)
        if paths:
            paths_str = ", ".join(paths)
            print(f"**{taxonomy.name}:** {paths_str}")

    if taxonomies:
        print()

    print(f"**Essence:** {principle.essence}")
    print()

    if principle.tags:
        print(f"**Tags:** {', '.join(principle.tags)}")
        print()

    if principle.related:
        print(f"**Related:** {', '.join(principle.related)}")
        print()

    print("---")
    print()
    print(principle.content)
