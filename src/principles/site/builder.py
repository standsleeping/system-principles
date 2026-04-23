"""Site builder."""

from pathlib import Path

from principles.logging import get_logger
from principles.translators import load_principles
from principles.translators.taxonomy_loader import load_taxonomy
from principles.types import (
    ParseError,
    Principle,
    PrincipleId,
    Taxonomy,
    ValidationError,
)

from .scripts import FILTER_JS
from .styles import CSS
from .templates import group_page, index_page, principle_page, slug

logger = get_logger(__name__)


def format_error(error: ParseError | ValidationError) -> str:
    """Format an error for display."""
    if isinstance(error, ParseError):
        return f"{error.message} ({error.file_path})"
    prefix = f"[{error.principle_id}] " if error.principle_id else ""
    return f"{prefix}{error.message}"


def build_site(
    content_dir: Path,
    taxonomies_dir: Path,
    output_dir: Path,
    taxonomy_name: str,
) -> int:
    """Build the static site.

    Returns 0 on success, 1 on error.
    """
    # Load principles
    principles, errors = load_principles(content_dir, recursive=False)
    if not principles:
        principles, errors = load_principles(content_dir, recursive=True)

    if errors:
        for error in errors:
            print(f"Warning: {format_error(error)}")

    if not principles:
        print("No principles found.")
        return 1

    principle_map: dict[PrincipleId, Principle] = {p.id: p for p in principles}

    # Load taxonomy
    taxonomy_path = taxonomies_dir / f"{taxonomy_name}.yaml"
    taxonomy_result = load_taxonomy(taxonomy_path)
    if not isinstance(taxonomy_result, Taxonomy):
        print(f"Error loading taxonomy '{taxonomy_name}': {taxonomy_result.message}")
        return 1
    taxonomy = taxonomy_result

    # Create output structure
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write CSS
    css_dir = output_dir / "css"
    css_dir.mkdir(exist_ok=True)
    (css_dir / "style.css").write_text(CSS, encoding="utf-8")

    # Write JS
    js_dir = output_dir / "js"
    js_dir.mkdir(exist_ok=True)
    (js_dir / "filter.js").write_text(FILTER_JS, encoding="utf-8")

    # Write index page
    (output_dir / "index.html").write_text(
        index_page(taxonomy, principle_map), encoding="utf-8"
    )

    # Write group pages
    group_count = 0
    for group in taxonomy.groups:
        group_dir = output_dir / group.name
        group_dir.mkdir(exist_ok=True)
        (group_dir / "index.html").write_text(
            group_page(group, principle_map, taxonomy), encoding="utf-8"
        )
        group_count += 1

    # Write principle pages
    principles_dir = output_dir / "principles"
    principles_dir.mkdir(exist_ok=True)
    principle_count = 0
    for principle in principles:
        p_dir = principles_dir / slug(principle.id)
        p_dir.mkdir(exist_ok=True)
        (p_dir / "index.html").write_text(
            principle_page(principle, taxonomy, principle_map), encoding="utf-8"
        )
        principle_count += 1

    parts = [
        f"{group_count} groups",
        f"{principle_count} principles",
    ]
    print(f"Built site: {', '.join(parts)} → {output_dir}/")
    return 0
