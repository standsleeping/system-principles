"""Load taxonomies from YAML files."""

from pathlib import Path
from typing import cast

import yaml

from principles.types import (
    ParseError,
    PrincipleId,
    Taxonomy,
    TaxonomyGroup,
    TaxonomyName,
)


def _parse_group(name: str, data: object, file_path: str) -> TaxonomyGroup | ParseError:
    """Recursively parse a taxonomy group from YAML data.

    Expected format:
        group_name:
          description: Optional description
          principles: [ID1, ID2]  # Direct children
          groups:                  # Nested subgroups
            subgroup_name:
              principles: [ID3]
    """
    if not isinstance(data, dict):
        return ParseError(
            file_path=file_path,
            message=f"Group '{name}' must be a mapping",
        )

    fields = cast(dict[str, object], data)
    description = str(fields.get("description", ""))

    # Parse direct principle IDs
    principles_raw = fields.get("principles", [])
    if not isinstance(principles_raw, list):
        return ParseError(
            file_path=file_path,
            message=f"Group '{name}' principles must be a list",
        )
    principle_ids = tuple(PrincipleId(str(p)) for p in principles_raw)

    # Parse nested subgroups
    subgroups: list[TaxonomyGroup] = []
    groups_raw = fields.get("groups", {})
    if not isinstance(groups_raw, dict):
        return ParseError(
            file_path=file_path,
            message=f"Group '{name}' groups must be a mapping",
        )

    for subgroup_name, subgroup_data in groups_raw.items():
        subgroup_result = _parse_group(str(subgroup_name), subgroup_data, file_path)
        if isinstance(subgroup_result, ParseError):
            return subgroup_result
        subgroups.append(subgroup_result)

    return TaxonomyGroup(
        name=name,
        description=description,
        principle_ids=principle_ids,
        subgroups=tuple(subgroups),
    )


def load_taxonomy(file_path: Path) -> Taxonomy | ParseError:
    """Load a taxonomy from YAML.

    Expected format:
        name: default
        description: Original phase/category organization
        groups:
          designing:
            groups:
              abstraction:
                principles: [AB1, AB2]
          modeling:
            groups:
              type-design:
                principles: [TD1, TD2]
    """
    if not file_path.exists():
        return ParseError(
            file_path=str(file_path),
            message="File does not exist",
        )

    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError as e:
        return ParseError(
            file_path=str(file_path),
            message=f"Failed to read file: {e}",
        )

    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        return ParseError(
            file_path=str(file_path),
            message=f"Invalid YAML: {e}",
        )

    if not isinstance(data, dict):
        return ParseError(
            file_path=str(file_path),
            message="Taxonomy file must be a YAML mapping",
        )

    # Validate required fields
    if "name" not in data:
        return ParseError(
            file_path=str(file_path),
            message="Missing required field: name",
        )

    if "groups" not in data:
        return ParseError(
            file_path=str(file_path),
            message="Missing required field: groups",
        )

    name = TaxonomyName(str(data["name"]))
    description = str(data.get("description", ""))

    groups_raw = data["groups"]
    if not isinstance(groups_raw, dict):
        return ParseError(
            file_path=str(file_path),
            message="groups must be a mapping",
        )

    # Parse top-level groups
    groups: list[TaxonomyGroup] = []
    for group_name, group_data in groups_raw.items():
        group_result = _parse_group(group_name, group_data, str(file_path))
        if isinstance(group_result, ParseError):
            return group_result
        groups.append(group_result)

    return Taxonomy(
        name=name,
        description=description,
        groups=tuple(groups),
    )


def load_taxonomies(
    taxonomies_dir: Path,
) -> tuple[list[Taxonomy], list[ParseError]]:
    """Load all taxonomies from a directory.

    Returns a tuple of (successfully loaded taxonomies, errors).
    """
    taxonomies: list[Taxonomy] = []
    errors: list[ParseError] = []

    if not taxonomies_dir.exists():
        return taxonomies, errors

    for yaml_file in taxonomies_dir.glob("*.yaml"):
        result = load_taxonomy(yaml_file)
        if isinstance(result, Taxonomy):
            taxonomies.append(result)
        else:
            errors.append(result)

    # Sort by name
    taxonomies.sort(key=lambda t: t.name)

    return taxonomies, errors
