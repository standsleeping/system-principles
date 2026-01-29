"""Load principles from Markdown files."""

from pathlib import Path

from principles.translators.frontmatter import parse_frontmatter
from principles.types import (
    Category,
    CategoryCode,
    ParseError,
    Phase,
    Principle,
    PrincipleId,
    ValidationError,
)


def _infer_phase_and_category(
    file_path: Path,
) -> tuple[Phase, str, CategoryCode] | ValidationError:
    """Infer phase and category from file path.

    Expected structure: content/<phase>/<category>/<id>.md
    """
    parts = file_path.parts

    # Find content directory index
    try:
        content_idx = parts.index("content")
    except ValueError:
        return ValidationError(
            message=f"File not in content directory: {file_path}",
        )

    remaining = parts[content_idx + 1 :]
    if len(remaining) < 3:
        return ValidationError(
            message=f"Invalid path structure, expected content/<phase>/<category>/<file>.md: {file_path}",
        )

    phase_str, category_name = remaining[0], remaining[1]

    # Parse phase
    try:
        phase = Phase(phase_str)
    except ValueError:
        valid_phases = [p.value for p in Phase]
        return ValidationError(
            message=f"Invalid phase '{phase_str}', must be one of: {valid_phases}",
        )

    # Derive category code from principle ID prefix (will be validated later)
    # For now, use category name as a placeholder
    category_code = CategoryCode(category_name.upper().replace("-", ""))

    return phase, category_name, category_code


def load_principle(file_path: Path) -> Principle | ParseError | ValidationError:
    """Load a single principle from a Markdown file with YAML frontmatter.

    Expected frontmatter fields:
        id: BD1 (required)
        title: Start Simple (required)
        summary: Begin with minimal viable solution (required)
        tags: [simplicity, design] (optional)
        related: [PS1, PS2] (optional)

    Phase and category are inferred from directory path.
    """
    if not file_path.exists():
        return ParseError(
            file_path=str(file_path),
            message="File does not exist",
        )

    if file_path.suffix != ".md":
        return ParseError(
            file_path=str(file_path),
            message="File must be a .md file",
        )

    # Read file
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError as e:
        return ParseError(
            file_path=str(file_path),
            message=f"Failed to read file: {e}",
        )

    # Parse frontmatter
    result = parse_frontmatter(text, str(file_path))
    if isinstance(result, ParseError):
        return result

    metadata = result.metadata
    content = result.content

    # Validate required fields
    required_fields = ["id", "title", "summary"]
    for field_name in required_fields:
        if field_name not in metadata:
            return ValidationError(
                message=f"Missing required field: {field_name}",
                field=field_name,
            )

    # Infer phase and category from path
    path_result = _infer_phase_and_category(file_path)
    if isinstance(path_result, ValidationError):
        return path_result

    phase, category_name, category_code = path_result

    # Extract fields
    principle_id = PrincipleId(str(metadata["id"]))
    title = str(metadata["title"])
    summary = str(metadata["summary"])

    # Optional fields
    tags_raw = metadata.get("tags", [])
    tags = tuple(str(t) for t in tags_raw) if isinstance(tags_raw, list) else ()

    related_raw = metadata.get("related", [])
    related = (
        tuple(PrincipleId(str(r)) for r in related_raw)
        if isinstance(related_raw, list)
        else ()
    )

    # Build category
    category = Category(
        code=category_code,
        name=category_name.replace("-", " ").title(),
        phase=phase,
    )

    return Principle(
        id=principle_id,
        title=title,
        summary=summary,
        category=category,
        content=content,
        tags=tags,
        related=related,
    )


def load_principles(
    content_dir: Path,
) -> tuple[list[Principle], list[ParseError | ValidationError]]:
    """Load all principles from a content directory.

    Returns a tuple of (successfully loaded principles, errors).
    """
    principles: list[Principle] = []
    errors: list[ParseError | ValidationError] = []

    if not content_dir.exists():
        errors.append(
            ParseError(
                file_path=str(content_dir),
                message="Content directory does not exist",
            )
        )
        return principles, errors

    # Find all .md files recursively
    for md_file in content_dir.rglob("*.md"):
        result = load_principle(md_file)
        if isinstance(result, Principle):
            principles.append(result)
        else:
            errors.append(result)

    # Sort by phase, then category, then ID
    principles.sort(key=lambda p: (p.category.phase.value, p.category.code, p.id))

    return principles, errors
