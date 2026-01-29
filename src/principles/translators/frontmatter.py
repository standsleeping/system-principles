"""Parse YAML frontmatter from Markdown files."""

from dataclasses import dataclass
from typing import Any

import yaml

from principles.types import ParseError


@dataclass(frozen=True, slots=True)
class FrontmatterResult:
    """Result of parsing frontmatter from a Markdown file."""

    metadata: dict[str, Any]
    content: str


def parse_frontmatter(
    text: str,
    file_path: str,
) -> FrontmatterResult | ParseError:
    """Extract YAML frontmatter and Markdown content from text.

    Expected format:
        ---
        key: value
        ---
        Markdown content here...

    Returns ParseError if frontmatter is missing or malformed.
    """
    if not text.startswith("---"):
        return ParseError(
            file_path=file_path,
            message="File must start with YAML frontmatter (---)",
        )

    # Find the closing ---
    end_marker = text.find("---", 3)
    if end_marker == -1:
        return ParseError(
            file_path=file_path,
            message="No closing --- found for frontmatter",
        )

    yaml_content = text[3:end_marker].strip()
    markdown_content = text[end_marker + 3 :].strip()

    try:
        metadata = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        return ParseError(
            file_path=file_path,
            message=f"Invalid YAML in frontmatter: {e}",
        )

    if not isinstance(metadata, dict):
        return ParseError(
            file_path=file_path,
            message="Frontmatter must be a YAML mapping",
        )

    return FrontmatterResult(metadata=metadata, content=markdown_content)
