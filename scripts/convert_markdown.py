#!/usr/bin/env python3
"""Convert markdown/*.md files to individual principle files in content/."""

import re
from pathlib import Path


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text


def parse_markdown_file(file_path: Path) -> list[dict]:
    """Parse a phase markdown file and extract principles."""
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    phase = None
    current_category = None
    principles = []
    current_principle = None
    in_code_block = False

    for line in lines:
        # Track code blocks to avoid parsing comments as headers
        if line.startswith("```"):
            in_code_block = not in_code_block
            if current_principle is not None:
                current_principle["content_lines"].append(line)
            continue

        # Skip header detection inside code blocks
        if in_code_block:
            if current_principle is not None:
                current_principle["content_lines"].append(line)
            continue

        # Phase header: # Designing (only at start, not ## or ###)
        if re.match(r"^# [^#]", line):
            phase = line[2:].strip().lower()
            continue

        # Category header: ## Boundaries
        if line.startswith("## "):
            # Save any pending principle
            if current_principle:
                current_principle["content"] = "\n".join(
                    current_principle["content_lines"]
                ).strip()
                del current_principle["content_lines"]
                principles.append(current_principle)
                current_principle = None

            current_category = line[3:].strip()
            continue

        # Principle header: ### [BD1] Title
        match = re.match(r"^### \[([A-Z]+\d+)\] (.+)$", line)
        if match:
            # Save any pending principle
            if current_principle:
                current_principle["content"] = "\n".join(
                    current_principle["content_lines"]
                ).strip()
                del current_principle["content_lines"]
                principles.append(current_principle)

            principle_id = match.group(1)
            title = match.group(2).strip()

            current_principle = {
                "id": principle_id,
                "title": title,
                "phase": phase,
                "category": current_category,
                "content_lines": [],
            }
            continue

        # Content lines
        if current_principle is not None:
            current_principle["content_lines"].append(line)

    # Save final principle
    if current_principle:
        current_principle["content"] = "\n".join(
            current_principle["content_lines"]
        ).strip()
        del current_principle["content_lines"]
        principles.append(current_principle)

    return principles


def extract_summary(content: str) -> str:
    """Extract the first sentence or paragraph as summary."""
    # Take first non-empty line(s) until we hit a blank line or list
    lines = content.split("\n")
    summary_lines = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if summary_lines:
                break
            continue
        if stripped.startswith(("1.", "-", "*", "#", "```")):
            break
        summary_lines.append(stripped)
        # Stop after first sentence if it ends with period
        if stripped.endswith(".") and len(summary_lines) >= 1:
            break

    summary = " ".join(summary_lines)
    # Truncate if too long
    if len(summary) > 200:
        summary = summary[:197] + "..."
    return summary


def write_principle(principle: dict, content_dir: Path) -> Path:
    """Write a principle to its own file."""
    phase = principle["phase"]
    category = slugify(principle["category"])
    principle_id = principle["id"]

    # Create directory
    dir_path = content_dir / phase / category
    dir_path.mkdir(parents=True, exist_ok=True)

    # Generate summary
    summary = extract_summary(principle["content"])

    # Escape quotes in summary for YAML
    summary_escaped = summary.replace('"', '\\"')

    # Build frontmatter (quote summary to handle colons)
    frontmatter = f'''---
id: {principle_id}
title: "{principle["title"]}"
summary: "{summary_escaped}"
---
'''

    file_path = dir_path / f"{principle_id}.md"
    file_path.write_text(frontmatter + "\n" + principle["content"], encoding="utf-8")

    return file_path


def main() -> None:
    """Convert all markdown files to individual principle files."""
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    markdown_dir = project_dir / "markdown"
    content_dir = project_dir / "content"

    # Clear existing content
    if content_dir.exists():
        import shutil

        shutil.rmtree(content_dir)

    content_dir.mkdir(exist_ok=True)

    # Phase files to process
    phase_files = [
        "designing.md",
        "modeling.md",
        "structuring.md",
        "implementing.md",
        "verifying.md",
        "presenting.md",
    ]

    total_principles = 0

    for filename in phase_files:
        file_path = markdown_dir / filename
        if not file_path.exists():
            print(f"Warning: {file_path} not found, skipping")
            continue

        principles = parse_markdown_file(file_path)
        print(f"{filename}: {len(principles)} principles")

        for principle in principles:
            write_principle(principle, content_dir)
            total_principles += 1

    print(f"\nTotal: {total_principles} principles converted")
    print(f"Output: {content_dir}")


if __name__ == "__main__":
    main()
