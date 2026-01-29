"""List command - display principles with optional filtering."""

import argparse
from pathlib import Path

from principles.translators import load_principles
from principles.translators.set_loader import load_set
from principles.types import ParseError, Phase, Principle, PrincipleSet, ValidationError


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

    # Load all principles
    principles, errors = load_principles(content_dir)

    if errors:
        for error in errors:
            print(f"Warning: {_format_error(error)}")

    if not principles:
        print("No principles found.")
        return 0

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

    # Filter by phase if specified
    if args.phase:
        phase = Phase(args.phase)
        principles = [p for p in principles if p.category.phase == phase]

    # Filter by category if specified
    if args.category:
        category_upper = args.category.upper()
        principles = [p for p in principles if p.category.code == category_upper]

    # Display results
    _display_principles(principles)

    return 0


def _display_principles(principles: list[Principle]) -> None:
    """Display a list of principles in a formatted table."""
    if not principles:
        print("No principles match the filter.")
        return

    # Group by phase and category
    current_phase = None
    current_category = None

    for p in principles:
        if p.category.phase != current_phase:
            current_phase = p.category.phase
            print(f"\n## {current_phase.value.title()}")

        if p.category.code != current_category:
            current_category = p.category.code
            print(f"\n### {p.category.name}")

        print(f"  {p.id}: {p.title}")

    print(f"\nTotal: {len(principles)} principles")
