"""Minimal markdown-to-HTML renderer.

Handles: headings (with stable anchor ids on h2/h3), fenced code blocks,
unordered/ordered lists, tables, blockquotes, horizontal rules, paragraphs,
and inline code/bold/italic.

Exports:
- render_markdown(text) -> (html, headings): renders and returns h2/h3 headings
- extract_headings(text): collect h2/h3 heading records for TOC generation
- markdown_to_html(text): core renderer
- inline_markup(text): convert inline code/bold/italic in a single line
- strip_markup(text): remove markdown markers (for <title> tags, etc.)
- heading_slug(text): URL-safe anchor id from heading text
"""

import re
from html import escape


def render_markdown(text: str) -> tuple[str, list[tuple[int, str, str]]]:
    """Render markdown to HTML and return collected h2/h3 headings for TOC."""
    html = markdown_to_html(text)
    headings = extract_headings(text)
    return html, headings


def extract_headings(text: str) -> list[tuple[int, str, str]]:
    """Extract (level, clean_text, anchor_id) tuples for h2/h3 headings.

    Anchors are deduplicated to match the ids emitted by markdown_to_html.
    Fenced code blocks are skipped so that ``# comments`` inside code are not
    picked up as headings.
    """
    headings: list[tuple[int, str, str]] = []
    seen: dict[str, int] = {}
    in_code = False
    for line in text.split("\n"):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(#{2,3})\s+(.+)$", line)
        if not m:
            continue
        level = len(m.group(1))
        raw = m.group(2).strip()
        clean = strip_markup(raw)
        base = heading_slug(raw)
        n = seen.get(base, 0)
        anchor = base if n == 0 else f"{base}-{n}"
        seen[base] = n + 1
        headings.append((level, clean, anchor))
    return headings


def markdown_to_html(text: str) -> str:
    """Convert simple markdown to HTML."""
    lines = text.split("\n")
    html_parts: list[str] = []
    seen_anchors: dict[str, int] = {}
    i = 0

    while i < len(lines):
        line = lines[i]

        # Fenced code block
        if line.strip().startswith("```"):
            lang = line.strip()[3:].strip()
            code_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(escape(lines[i]))
                i += 1
            i += 1  # skip closing ```
            code_content = "\n".join(code_lines)
            if lang:
                html_parts.append(
                    f'<pre><code class="language-{escape(lang)}">'
                    f"{code_content}</code></pre>"
                )
            else:
                html_parts.append(f"<pre><code>{code_content}</code></pre>")
            continue

        # Heading
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading_match:
            level = len(heading_match.group(1))
            raw_text = heading_match.group(2)
            inner = inline_markup(raw_text)
            if 2 <= level <= 3:
                base = heading_slug(raw_text)
                n = seen_anchors.get(base, 0)
                anchor = base if n == 0 else f"{base}-{n}"
                seen_anchors[base] = n + 1
                html_parts.append(
                    f'<h{level} id="{escape(anchor)}">'
                    f'<a class="heading-anchor" href="#{escape(anchor)}">{inner}</a>'
                    f"</h{level}>"
                )
            else:
                html_parts.append(f"<h{level}>{inner}</h{level}>")
            i += 1
            continue

        # Table
        if re.match(r"^\|.+\|$", line):
            table_lines: list[str] = []
            while i < len(lines) and re.match(r"^\|.+\|$", lines[i]):
                table_lines.append(lines[i])
                i += 1
            html_parts.append(parse_table(table_lines))
            continue

        # Blockquote
        if line.startswith("> "):
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].startswith("> "):
                quote_lines.append(lines[i][2:])
                i += 1
            inner = " ".join(quote_lines)
            html_parts.append(f"<blockquote><p>{inline_markup(inner)}</p></blockquote>")
            continue

        # Horizontal rule
        if re.match(r"^---+\s*$", line):
            html_parts.append("<hr>")
            i += 1
            continue

        # Unordered list
        if re.match(r"^[\-\*]\s+", line):
            html_parts.append("<ul>")
            while i < len(lines) and re.match(r"^[\-\*]\s+", lines[i]):
                item_text = re.sub(r"^[\-\*]\s+", "", lines[i])
                html_parts.append(f"<li>{inline_markup(item_text)}</li>")
                i += 1
            html_parts.append("</ul>")
            continue

        # Ordered list
        if re.match(r"^\d+\.\s+", line):
            html_parts.append("<ol>")
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                item_text = re.sub(r"^\d+\.\s+", "", lines[i])
                html_parts.append(f"<li>{inline_markup(item_text)}</li>")
                i += 1
            html_parts.append("</ol>")
            continue

        # Blank line
        if not line.strip():
            i += 1
            continue

        # Paragraph: collect consecutive non-blank, non-special lines
        para_lines: list[str] = []
        while i < len(lines) and lines[i].strip() and not is_block_start(lines[i]):
            para_lines.append(lines[i])
            i += 1
        if para_lines:
            html_parts.append(f"<p>{inline_markup(' '.join(para_lines))}</p>")
        continue

    return "\n".join(html_parts)


def is_block_start(line: str) -> bool:
    """Check if a line starts a block element."""
    if line.strip().startswith("```"):
        return True
    if re.match(r"^#{1,6}\s+", line):
        return True
    if re.match(r"^\|.+\|$", line):
        return True
    if re.match(r"^[\-\*]\s+", line):
        return True
    if line.startswith("> "):
        return True
    if re.match(r"^---+\s*$", line):
        return True
    return bool(re.match(r"^\d+\.\s+", line))


def parse_table(lines: list[str]) -> str:
    """Parse markdown table lines into an HTML table."""
    parts: list[str] = ["<table>"]

    def split_row(line: str) -> list[str]:
        return [cell.strip() for cell in line.strip("|").split("|")]

    headers = split_row(lines[0])
    parts.append("<thead><tr>")
    for h in headers:
        parts.append(f"<th>{inline_markup(h)}</th>")
    parts.append("</tr></thead>")

    parts.append("<tbody>")
    for line in lines[2:]:
        cells = split_row(line)
        parts.append("<tr>")
        for cell in cells:
            parts.append(f"<td>{inline_markup(cell)}</td>")
        parts.append("</tr>")
    parts.append("</tbody>")

    parts.append("</table>")
    return "".join(parts)


def inline_markup(text: str) -> str:
    """Convert inline markdown (code, bold, italic) in a single line of text."""
    text = escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__([^_]+)__", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"<em>\1</em>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    return text


def strip_markup(text: str) -> str:
    """Remove markdown markers for use in plain-text contexts like <title>."""
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return text


def heading_slug(text: str) -> str:
    """Generate a URL-safe anchor id from heading text.

    Strips markdown markers, lowercases, drops non-alphanumeric (except spaces
    and hyphens), then collapses whitespace to single hyphens. Returns 'section'
    as fallback if the result would be empty.
    """
    text = strip_markup(text).lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    return text or "section"
