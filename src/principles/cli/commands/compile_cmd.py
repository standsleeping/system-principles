"""Compile command - compile principles to various output formats."""

import argparse
from pathlib import Path

from principles.translators import load_principles
from principles.translators.set_loader import load_set
from principles.types import ParseError, Principle, PrincipleSet, ValidationError


def _format_error(error: ParseError | ValidationError) -> str:
    """Format an error for display."""
    if isinstance(error, ParseError):
        return f"{error.message} ({error.file_path})"
    else:
        prefix = f"[{error.principle_id}] " if error.principle_id else ""
        return f"{prefix}{error.message}"


def run_compile(args: argparse.Namespace) -> int:
    """Execute the compile command."""
    content_dir = Path(args.content_dir)
    sets_dir = Path(args.sets_dir)

    # Load all principles
    principles, errors = load_principles(content_dir)

    if errors:
        for error in errors:
            print(f"Warning: {_format_error(error)}")

    if not principles:
        print("No principles found.")
        return 1

    # Filter by set if specified
    set_info: PrincipleSet | None = None
    if args.set_name:
        set_path = sets_dir / f"{args.set_name}.yaml"
        set_result = load_set(set_path)
        if isinstance(set_result, PrincipleSet):
            set_info = set_result
            allowed_ids = set(set_result.principle_ids)
            principles = [p for p in principles if p.id in allowed_ids]
        else:
            print(f"Error loading set: {set_result.message}")
            return 1

    # Compile based on format
    output_format = args.format

    if output_format == "markdown":
        output = _compile_markdown(principles, set_info)
    elif output_format == "agent-skill":
        output = _compile_agent_skill(principles, set_info)
    else:
        print(f"Unknown format: {output_format}")
        return 1

    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
        print(f"Compiled {len(principles)} principles to {output_path}")
    else:
        print(output)

    return 0


def _compile_markdown(
    principles: list[Principle],
    set_info: PrincipleSet | None,
) -> str:
    """Compile principles to Markdown format."""
    lines: list[str] = []

    # Header
    if set_info:
        lines.append(f"# {set_info.name}")
        if set_info.description:
            lines.append("")
            lines.append(set_info.description)
    else:
        lines.append("# Principles")

    lines.append("")

    # Group by phase and category
    current_phase = None
    current_category = None

    for p in principles:
        if p.category.phase != current_phase:
            current_phase = p.category.phase
            lines.append(f"## {current_phase.value.title()}")
            lines.append("")

        if p.category.code != current_category:
            current_category = p.category.code
            lines.append(f"### {p.category.name}")
            lines.append("")

        lines.append(f"#### [{p.id}] {p.title}")
        lines.append("")
        lines.append(f"*{p.summary}*")
        lines.append("")
        lines.append(p.content)
        lines.append("")

    return "\n".join(lines)


def _compile_agent_skill(
    principles: list[Principle],
    set_info: PrincipleSet | None,
) -> str:
    """Compile principles to Agent Skill format per agentskills.io spec."""
    lines: list[str] = []

    # YAML frontmatter
    name = set_info.name if set_info else "principles"
    description = (
        set_info.description
        if set_info and set_info.description
        else "System design principles for building maintainable software."
    )

    lines.append("---")
    lines.append(f"name: {name}")
    lines.append(f"description: {description}")
    lines.append("---")
    lines.append("")

    # Instructions header
    lines.append("# Design Principles")
    lines.append("")
    lines.append(
        "Apply these principles when designing and implementing code. "
        "Reference principles by their ID (e.g., BD1, TD3) when explaining decisions."
    )
    lines.append("")

    # Principles organized by phase
    current_phase = None

    for p in principles:
        if p.category.phase != current_phase:
            current_phase = p.category.phase
            lines.append(f"## {current_phase.value.title()}")
            lines.append("")

        lines.append(f"### {p.id}: {p.title}")
        lines.append("")
        lines.append(p.summary)
        lines.append("")

        # Include content but keep it concise for skill format
        content_lines = p.content.strip().split("\n")
        # Take first paragraph or up to 10 lines
        preview_lines: list[str] = []
        for line in content_lines:
            if not line.strip() and preview_lines:
                break
            preview_lines.append(line)
            if len(preview_lines) >= 10:
                break

        if preview_lines:
            lines.extend(preview_lines)
            lines.append("")

    return "\n".join(lines)
