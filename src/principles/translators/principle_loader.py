"""Load principles from Markdown files."""

from pathlib import Path

from principles.translators.frontmatter import parse_frontmatter
from principles.types import (
    ParseError,
    Principle,
    PrincipleId,
    ValidationError,
)


def load_principle(file_path: Path) -> Principle | ParseError | ValidationError:
    """Load a single principle from a Markdown file with YAML frontmatter.

    Expected frontmatter fields:
        id: BD1 (required)
        title: Start Simple (required)
        essence: The core insight in one sentence (required)
        tags: [simplicity, design] (optional)
        related: [PS1, PS2] (optional)

    Principles are taxonomy-independent; organizational structure is defined
    separately in taxonomy files.
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
    required_fields = ["id", "title", "essence"]
    for field_name in required_fields:
        if field_name not in metadata:
            return ValidationError(
                message=f"Missing required field: {field_name}",
                field=field_name,
            )

    # Extract fields
    principle_id = PrincipleId(str(metadata["id"]))
    title = str(metadata["title"])
    essence = str(metadata["essence"])

    # Optional fields
    tags_raw = metadata.get("tags", [])
    tags = tuple(str(t) for t in tags_raw) if isinstance(tags_raw, list) else ()

    related_raw = metadata.get("related", [])
    related = (
        tuple(PrincipleId(str(r)) for r in related_raw)
        if isinstance(related_raw, list)
        else ()
    )

    return Principle(
        id=principle_id,
        title=title,
        essence=essence,
        content=content,
        tags=tags,
        related=related,
    )


def load_principles(
    content_dir: Path,
    recursive: bool = False,
) -> tuple[list[Principle], list[ParseError | ValidationError]]:
    """Load all principles from a content directory.

    Args:
        content_dir: Path to directory containing principle .md files
        recursive: If True, search subdirectories (for migration compatibility).
                   If False (default), only load from the directory root.

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

    # Find .md files (flat or recursive based on flag)
    pattern = "**/*.md" if recursive else "*.md"
    for md_file in content_dir.glob(pattern):
        result = load_principle(md_file)
        if isinstance(result, Principle):
            principles.append(result)
        else:
            errors.append(result)

    # Sort alphabetically by ID
    principles.sort(key=lambda p: p.id)

    return principles, errors
