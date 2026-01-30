#!/usr/bin/env python3
"""Rename principle files and update IDs based on mapping file."""

import re
from pathlib import Path


def parse_mapping(mapping_file: Path) -> dict[str, str]:
    """Parse the id-mapping.txt file into old_id -> new_id dict."""
    mapping = {}
    for line in mapping_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 3:
            old_id, _, new_id = parts[0], parts[1], parts[2]
            mapping[old_id] = new_id
    return mapping


def update_principle_file(old_path: Path, new_path: Path, new_id: str) -> None:
    """Update the id in frontmatter and rename the file."""
    content = old_path.read_text()

    # Update the id field in frontmatter
    content = re.sub(
        r"^id: .+$",
        f"id: {new_id}",
        content,
        count=1,
        flags=re.MULTILINE,
    )

    # Write to new path
    new_path.write_text(content)

    # Remove old file if different
    if old_path != new_path:
        old_path.unlink()


def update_taxonomy(taxonomy_path: Path, mapping: dict[str, str]) -> None:
    """Update principle IDs in taxonomy file."""
    content = taxonomy_path.read_text()

    # Sort by length descending to avoid partial replacements
    for old_id, new_id in sorted(mapping.items(), key=lambda x: -len(x[0])):
        # Only replace when it's a standalone ID (preceded by "- " in YAML list)
        content = content.replace(f"- {old_id}\n", f"- {new_id}\n")

    taxonomy_path.write_text(content)


def main() -> None:
    root = Path(__file__).parent.parent
    mapping_file = root / "planning" / "id-mapping.txt"
    content_dir = root / "content"
    taxonomy_file = root / "taxonomies" / "default.yaml"

    mapping = parse_mapping(mapping_file)
    print(f"Loaded {len(mapping)} mappings")

    # Rename and update principle files
    renamed = 0
    for old_id, new_id in mapping.items():
        old_path = content_dir / f"{old_id}.md"
        new_filename = new_id.lower() + ".md"
        new_path = content_dir / new_filename

        if old_path.exists():
            update_principle_file(old_path, new_path, new_id)
            print(f"  {old_id}.md -> {new_filename}")
            renamed += 1
        else:
            print(f"  WARNING: {old_path} not found")

    print(f"\nRenamed {renamed} files")

    # Update taxonomy
    update_taxonomy(taxonomy_file, mapping)
    print("Updated taxonomy")


if __name__ == "__main__":
    main()
