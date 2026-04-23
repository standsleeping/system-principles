"""Tests for the site markdown renderer."""

from principles.site.markdown import extract_headings, heading_slug


# === heading_slug ===


def test_heading_slug_basic() -> None:
    """Lowercases and hyphenates a plain heading."""
    assert heading_slug("The Fix: Flatten") == "the-fix-flatten"


def test_heading_slug_collapses_whitespace() -> None:
    """Collapses multiple spaces and trims edges."""
    assert heading_slug("  Leading    and  trailing  ") == "leading-and-trailing"


def test_heading_slug_strips_markdown_markers() -> None:
    """Strips bold, italic, and inline code markers before slugging."""
    assert heading_slug("Use **strong** _types_") == "use-strong-types"
    assert heading_slug("Call `foo()` in bar") == "call-foo-in-bar"


def test_heading_slug_drops_punctuation() -> None:
    """Non-alphanumeric characters (except hyphens and spaces) are dropped."""
    assert heading_slug("What's next?") == "whats-next"
    assert heading_slug("A/B testing, etc.") == "ab-testing-etc"


def test_heading_slug_preserves_existing_hyphens() -> None:
    """Existing hyphens are preserved, not duplicated."""
    assert heading_slug("multi-part-slug") == "multi-part-slug"


def test_heading_slug_empty_input_fallback() -> None:
    """Returns 'section' when the cleaned result would be empty."""
    assert heading_slug("") == "section"
    assert heading_slug("!!!") == "section"


# === extract_headings ===


def test_extract_headings_h2_and_h3() -> None:
    """Captures h2 and h3 headings with their level, cleaned text, and anchor."""
    text = "## First\n\nSome body\n\n### Nested\n\nMore"
    assert extract_headings(text) == [
        (2, "First", "first"),
        (3, "Nested", "nested"),
    ]


def test_extract_headings_ignores_h1_and_h4() -> None:
    """h1 and h4+ are outside the TOC range."""
    text = "# Page title\n\n## Section\n\n#### Deep\n\n##### Deeper"
    assert extract_headings(text) == [(2, "Section", "section")]


def test_extract_headings_excludes_code_block_hashes() -> None:
    """Lines inside fenced code blocks are not treated as headings."""
    text = "## Real heading\n\n```python\n## not a heading\n### also not\n```\n\n## Another"
    assert extract_headings(text) == [
        (2, "Real heading", "real-heading"),
        (2, "Another", "another"),
    ]


def test_extract_headings_deduplicates_anchors() -> None:
    """Identical heading text gets unique anchors via a numeric suffix."""
    text = "## Overview\n\nstuff\n\n## Overview\n\nmore\n\n## Overview"
    assert extract_headings(text) == [
        (2, "Overview", "overview"),
        (2, "Overview", "overview-1"),
        (2, "Overview", "overview-2"),
    ]


def test_extract_headings_strips_inline_markup_from_text() -> None:
    """Cleaned heading text has markdown markers removed."""
    text = "## Use `Proof` _carefully_"
    assert extract_headings(text) == [(2, "Use Proof carefully", "use-proof-carefully")]


def test_extract_headings_empty_input() -> None:
    """No headings produces an empty list."""
    assert extract_headings("") == []
    assert extract_headings("just a paragraph with no headings") == []
