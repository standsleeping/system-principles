"""Export command — compile principles into Claude Code config files."""

import argparse
from pathlib import Path

from principles.cli.commands.compile_cmd import compile_principles_to_string
from principles.export.claude_code import COMPILE_SPECS
from principles.types import CompileSpec


def run_export(args: argparse.Namespace) -> int:
    """Execute the export command."""
    principles_dir = Path(args.principles_dir).resolve()
    output_dir = principles_dir / "config" / "claude"

    content_dir = principles_dir / "content"
    taxonomies_dir = principles_dir / "taxonomies"
    sets_dir = principles_dir / "sets"

    compiled_count = 0

    # Generate the principles fragment with the baked path
    principles_fragment = (
        "# Design Principles\n"
        "\n"
        f"The system-principles repository is at `{principles_dir}`.\n"
        "\n"
        "Before beginning any significant coding task, consult the design "
        "principles. When creating a design, if you find that two or more "
        "principles are in tension or direct conflict, raise this for "
        "discussion before making tradeoffs.\n"
    )
    fragment_path = output_dir / "fragments" / "principles.md"
    fragment_path.parent.mkdir(parents=True, exist_ok=True)
    fragment_path.write_text(principles_fragment, encoding="utf-8")
    compiled_count += 1

    # Compile principle groups into output files
    for spec in COMPILE_SPECS:
        result = _compile_spec(spec, content_dir, taxonomies_dir, sets_dir)
        if result is None:
            print(f"Warning: no principles matched for {spec.output_path}")
            continue

        dest = output_dir / spec.output_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(result, encoding="utf-8")
        compiled_count += 1

    print(f"Compiled {compiled_count} files to {output_dir}")
    return 0


def _compile_spec(
    spec: CompileSpec,
    content_dir: Path,
    taxonomies_dir: Path,
    sets_dir: Path,
) -> str | None:
    """Compile a single spec by running each group and assembling the output."""
    group_outputs: list[str] = []

    for group in spec.groups:
        output = compile_principles_to_string(
            content_dir=content_dir,
            taxonomies_dir=taxonomies_dir,
            sets_dir=sets_dir,
            output_format="essences",
            taxonomy_name="default",
            group_path=group,
        )
        if output:
            group_outputs.append(output.rstrip("\n"))

    if not group_outputs:
        return None

    content = "\n".join(group_outputs)

    # Build the file: optional frontmatter + header + content
    parts: list[str] = []
    if spec.paths_frontmatter is not None:
        paths_yaml = "\n".join(f'  - "{p}"' for p in spec.paths_frontmatter)
        parts.append(f"---\npaths:\n{paths_yaml}\n---")
    parts.append(spec.header)
    parts.append(content)

    return "\n\n".join(parts) + "\n"
