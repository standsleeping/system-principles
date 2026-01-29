"""Load principle sets from YAML files."""

from pathlib import Path

import yaml

from principles.types import ParseError, PrincipleId, PrincipleSet, SetName


def load_set(file_path: Path) -> PrincipleSet | ParseError:
    """Load a principle set definition from YAML.

    Expected format:
        name: core
        description: Core design principles
        principles:
          - BD1
          - PS1
          - PS2
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
            message="Set file must be a YAML mapping",
        )

    # Validate required fields
    if "name" not in data:
        return ParseError(
            file_path=str(file_path),
            message="Missing required field: name",
        )

    if "principles" not in data:
        return ParseError(
            file_path=str(file_path),
            message="Missing required field: principles",
        )

    name = SetName(str(data["name"]))
    description = str(data.get("description", ""))

    principles_raw = data["principles"]
    if not isinstance(principles_raw, list):
        return ParseError(
            file_path=str(file_path),
            message="principles must be a list",
        )

    principle_ids = tuple(PrincipleId(str(p)) for p in principles_raw)

    return PrincipleSet(
        name=name,
        description=description,
        principle_ids=principle_ids,
    )


def load_sets(sets_dir: Path) -> tuple[list[PrincipleSet], list[ParseError]]:
    """Load all principle sets from a directory.

    Returns a tuple of (successfully loaded sets, errors).
    """
    sets: list[PrincipleSet] = []
    errors: list[ParseError] = []

    if not sets_dir.exists():
        return sets, errors

    for yaml_file in sets_dir.glob("*.yaml"):
        result = load_set(yaml_file)
        if isinstance(result, PrincipleSet):
            sets.append(result)
        else:
            errors.append(result)

    # Sort by name
    sets.sort(key=lambda s: s.name)

    return sets, errors
