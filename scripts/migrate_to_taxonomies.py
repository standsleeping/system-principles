#!/usr/bin/env python3
"""Migrate from hierarchical content to flat content + taxonomies.

This script:
1. Scans the current content/<phase>/<category>/<id>.md structure
2. Generates taxonomies/default.yaml from the current organization
3. Flattens content/ by moving all .md files to the root
4. Removes empty subdirectories

Run with --dry-run to preview changes without making them.
"""

import argparse
import shutil
from pathlib import Path

import yaml


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate to flat content + taxonomies")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without making them")
    parser.add_argument("--no-backup", action="store_true", help="Skip creating backup")
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    content_dir = project_root / "content"
    taxonomies_dir = project_root / "taxonomies"
    backup_dir = project_root / "content_backup"

    if not content_dir.exists():
        print(f"Content directory not found: {content_dir}")
        return

    # 1. Scan current structure and build taxonomy
    print("Scanning current structure...")
    taxonomy_groups: dict[str, dict[str, list[str]]] = {}
    files_to_move: list[tuple[Path, Path]] = []

    for md_file in content_dir.rglob("*.md"):
        relative = md_file.relative_to(content_dir)
        parts = relative.parts

        if len(parts) >= 3:
            # content/<phase>/<category>/<file>.md
            phase, category = parts[0], parts[1]
            filename = md_file.name
            principle_id = filename.replace(".md", "")

            if phase not in taxonomy_groups:
                taxonomy_groups[phase] = {}
            if category not in taxonomy_groups[phase]:
                taxonomy_groups[phase][category] = []
            taxonomy_groups[phase][category].append(principle_id)

            dest = content_dir / filename
            if md_file != dest:
                files_to_move.append((md_file, dest))
        elif len(parts) == 1:
            # Already at root level, skip
            print(f"  Already flat: {md_file.name}")

    # Sort principle IDs within each category
    for phase in taxonomy_groups:
        for category in taxonomy_groups[phase]:
            taxonomy_groups[phase][category].sort()

    print(f"Found {len(files_to_move)} files to move")
    print(f"Found {len(taxonomy_groups)} phases")

    # 2. Generate taxonomy YAML structure
    taxonomy_data = {
        "name": "default",
        "description": "Original phase/category organization (migrated)",
        "groups": {},
    }

    # Define phase order
    phase_order = ["designing", "modeling", "structuring", "implementing", "verifying", "presenting"]

    for phase in phase_order:
        if phase not in taxonomy_groups:
            continue

        taxonomy_data["groups"][phase] = {"groups": {}}
        categories = taxonomy_groups[phase]

        for category in sorted(categories.keys()):
            principle_ids = categories[category]
            taxonomy_data["groups"][phase]["groups"][category] = {
                "principles": principle_ids
            }

    if args.dry_run:
        print("\n=== DRY RUN - No changes will be made ===\n")

        print("Would create taxonomy file:")
        print(f"  {taxonomies_dir / 'default.yaml'}")
        print("\nTaxonomy content preview:")
        print(yaml.dump(taxonomy_data, default_flow_style=False, sort_keys=False)[:500])
        print("...")

        print(f"\nWould move {len(files_to_move)} files:")
        for src, dst in files_to_move[:10]:
            print(f"  {src.name}")
        if len(files_to_move) > 10:
            print(f"  ... and {len(files_to_move) - 10} more")

        return

    # 3. Create backup
    if not args.no_backup:
        if backup_dir.exists():
            print(f"Removing existing backup: {backup_dir}")
            shutil.rmtree(backup_dir)
        print(f"Creating backup: {backup_dir}")
        shutil.copytree(content_dir, backup_dir)

    # 4. Create taxonomies directory and write default.yaml
    taxonomies_dir.mkdir(exist_ok=True)
    taxonomy_file = taxonomies_dir / "default.yaml"

    print(f"Writing taxonomy: {taxonomy_file}")
    with open(taxonomy_file, "w") as f:
        yaml.dump(taxonomy_data, f, default_flow_style=False, sort_keys=False)

    # 5. Move files to flat structure
    print(f"Moving {len(files_to_move)} files...")
    for src, dst in files_to_move:
        if dst.exists():
            print(f"  Warning: {dst.name} already exists, skipping {src}")
            continue
        shutil.move(src, dst)

    # 6. Remove empty directories
    print("Removing empty directories...")
    for dirpath in sorted(content_dir.rglob("*"), reverse=True):
        if dirpath.is_dir():
            try:
                dirpath.rmdir()  # Only removes if empty
                print(f"  Removed: {dirpath.relative_to(content_dir)}")
            except OSError:
                pass  # Directory not empty

    # Summary
    print("\n=== Migration Complete ===")
    print(f"  Principles flattened: {len(files_to_move)}")
    print(f"  Taxonomy created: {taxonomy_file}")
    if not args.no_backup:
        print(f"  Backup location: {backup_dir}")

    total_principles = sum(
        len(ids)
        for categories in taxonomy_groups.values()
        for ids in categories.values()
    )
    print(f"  Total principles in taxonomy: {total_principles}")


if __name__ == "__main__":
    main()
