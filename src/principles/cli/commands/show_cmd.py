"""Show command - display a single principle in detail."""

import argparse
from pathlib import Path

from principles.translators import load_principles
from principles.types import Principle, PrincipleId


def run_show(args: argparse.Namespace) -> int:
    """Execute the show command."""
    content_dir = Path(args.content_dir)
    principle_id = PrincipleId(args.id.upper())

    # Load all principles and find the matching one
    principles, errors = load_principles(content_dir)

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
    _display_principle(principle)

    return 0


def _display_principle(principle: Principle) -> None:
    """Display a single principle in detail."""
    print(f"# [{principle.id}] {principle.title}")
    print()
    print(f"**Phase:** {principle.category.phase.value.title()}")
    print(f"**Category:** {principle.category.name}")
    print()
    print(f"**Summary:** {principle.summary}")
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
