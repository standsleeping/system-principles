"""Compile command - compile principles to various output formats."""

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


def run_compile(args: argparse.Namespace) -> int:
    """Execute the compile command."""
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
        return 1

    # Build lookup map
    principle_map: dict[PrincipleId, Principle] = {p.id: p for p in principles}

    # Load taxonomy if specified
    taxonomy: Taxonomy | None = None
    if args.taxonomy:
        taxonomy_path = taxonomies_dir / f"{args.taxonomy}.yaml"
        taxonomy_result = load_taxonomy(taxonomy_path)
        if isinstance(taxonomy_result, Taxonomy):
            taxonomy = taxonomy_result
        else:
            print(f"Warning: Could not load taxonomy '{args.taxonomy}': {taxonomy_result.message}")

    # Filter by group path if specified (requires taxonomy)
    if args.group and taxonomy:
        allowed_ids = taxonomy.get_principles_by_path(GroupPath(args.group))
        principles = [p for p in principles if p.id in allowed_ids]

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
        output = _compile_markdown(principles, principle_map, set_info, taxonomy)
    elif output_format == "agent-skill":
        output = _compile_agent_skill(principles, principle_map, set_info, taxonomy)
    elif output_format == "essences":
        output = _compile_essences(principles, principle_map, set_info, taxonomy)
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
    principle_map: dict[PrincipleId, Principle],
    set_info: PrincipleSet | None,
    taxonomy: Taxonomy | None,
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

    # Build set of principle IDs we want to include
    include_ids = {p.id for p in principles}

    if taxonomy:
        _compile_markdown_with_taxonomy(lines, taxonomy, principle_map, include_ids)
    else:
        _compile_markdown_flat(lines, principles)

    return "\n".join(lines)


def _compile_markdown_flat(lines: list[str], principles: list[Principle]) -> None:
    """Compile principles to flat Markdown without taxonomy grouping."""
    for p in principles:
        lines.append(f"## [{p.id}] {p.title}")
        lines.append("")
        lines.append(f"*{p.essence}*")
        lines.append("")
        lines.append(p.content)
        lines.append("")


def _compile_markdown_with_taxonomy(
    lines: list[str],
    taxonomy: Taxonomy,
    principle_map: dict[PrincipleId, Principle],
    include_ids: set[PrincipleId],
) -> None:
    """Compile principles to Markdown grouped by taxonomy structure."""

    def compile_group(group: TaxonomyGroup, depth: int) -> None:
        """Recursively compile a group and its subgroups."""
        # Check if this group has any principles we want to include
        group_ids = group.get_all_principle_ids()
        relevant_ids = group_ids & include_ids
        if not relevant_ids:
            return

        # Print group header
        prefix = "#" * (depth + 1)
        lines.append(f"{prefix} {group.name.replace('-', ' ').title()}")
        lines.append("")

        # Print principles in this group
        for pid in group.principle_ids:
            if pid in include_ids and pid in principle_map:
                p = principle_map[pid]
                lines.append(f"{'#' * (depth + 2)} [{p.id}] {p.title}")
                lines.append("")
                lines.append(f"*{p.essence}*")
                lines.append("")
                lines.append(p.content)
                lines.append("")

        # Recurse into subgroups
        for subgroup in group.subgroups:
            compile_group(subgroup, depth + 1)

    for group in taxonomy.groups:
        compile_group(group, 1)

    # Add any uncategorized principles
    taxonomy_ids = taxonomy.get_all_principle_ids()
    uncategorized = [principle_map[pid] for pid in include_ids if pid not in taxonomy_ids and pid in principle_map]
    if uncategorized:
        lines.append("## Uncategorized")
        lines.append("")
        for p in uncategorized:
            lines.append(f"### [{p.id}] {p.title}")
            lines.append("")
            lines.append(f"*{p.essence}*")
            lines.append("")
            lines.append(p.content)
            lines.append("")


def _compile_agent_skill(
    principles: list[Principle],
    principle_map: dict[PrincipleId, Principle],
    set_info: PrincipleSet | None,
    taxonomy: Taxonomy | None,
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

    # Build set of principle IDs we want to include
    include_ids = {p.id for p in principles}

    if taxonomy:
        _compile_agent_skill_with_taxonomy(lines, taxonomy, principle_map, include_ids)
    else:
        _compile_agent_skill_flat(lines, principles)

    return "\n".join(lines)


def _compile_agent_skill_flat(lines: list[str], principles: list[Principle]) -> None:
    """Compile principles to flat Agent Skill format without taxonomy grouping."""
    for p in principles:
        lines.append(f"## {p.id}: {p.title}")
        lines.append("")
        lines.append(p.essence)
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


def _compile_agent_skill_with_taxonomy(
    lines: list[str],
    taxonomy: Taxonomy,
    principle_map: dict[PrincipleId, Principle],
    include_ids: set[PrincipleId],
) -> None:
    """Compile principles to Agent Skill format grouped by taxonomy structure."""

    def compile_group(group: TaxonomyGroup, depth: int) -> None:
        """Recursively compile a group and its subgroups."""
        # Check if this group has any principles we want to include
        group_ids = group.get_all_principle_ids()
        relevant_ids = group_ids & include_ids
        if not relevant_ids:
            return

        # Print group header
        prefix = "#" * (depth + 1)
        lines.append(f"{prefix} {group.name.replace('-', ' ').title()}")
        lines.append("")

        # Print principles in this group
        for pid in group.principle_ids:
            if pid in include_ids and pid in principle_map:
                p = principle_map[pid]
                lines.append(f"{'#' * (depth + 2)} {p.id}: {p.title}")
                lines.append("")
                lines.append(p.essence)
                lines.append("")

                # Include content but keep it concise for skill format
                content_lines = p.content.strip().split("\n")
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

        # Recurse into subgroups
        for subgroup in group.subgroups:
            compile_group(subgroup, depth + 1)

    for group in taxonomy.groups:
        compile_group(group, 1)


def _compile_essences(
    principles: list[Principle],
    principle_map: dict[PrincipleId, Principle],
    set_info: PrincipleSet | None,
    taxonomy: Taxonomy | None,
) -> str:
    """Compile principles to essences-only format (ID, title, one-line summary)."""
    lines: list[str] = []

    include_ids = {p.id for p in principles}

    if taxonomy:
        _compile_essences_with_taxonomy(lines, taxonomy, principle_map, include_ids)
    else:
        _compile_essences_flat(lines, principles)

    return "\n".join(lines)


def _compile_essences_flat(lines: list[str], principles: list[Principle]) -> None:
    """Compile essences without taxonomy grouping."""
    for p in principles:
        lines.append(f"- **{p.id}** {p.title}: {p.essence}")


def _compile_essences_with_taxonomy(
    lines: list[str],
    taxonomy: Taxonomy,
    principle_map: dict[PrincipleId, Principle],
    include_ids: set[PrincipleId],
) -> None:
    """Compile essences grouped by taxonomy structure."""

    def compile_group(group: TaxonomyGroup, depth: int) -> None:
        group_ids = group.get_all_principle_ids()
        relevant_ids = group_ids & include_ids
        if not relevant_ids:
            return

        prefix = "#" * (depth + 1)
        lines.append(f"{prefix} {group.name.replace('-', ' ').title()}")
        if group.description:
            lines.append(f"*{group.description}*")
        lines.append("")

        for pid in group.principle_ids:
            if pid in include_ids and pid in principle_map:
                p = principle_map[pid]
                lines.append(f"- **{p.id}** {p.title}: {p.essence}")

        lines.append("")

        for subgroup in group.subgroups:
            compile_group(subgroup, depth + 1)

    for group in taxonomy.groups:
        compile_group(group, 1)
