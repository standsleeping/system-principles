"""HTML template functions for the static site."""

import re
from html import escape

from principles.types import Principle, PrincipleId, Taxonomy, TaxonomyGroup


def slug(principle_id: PrincipleId) -> str:
    """Convert a principle ID to a URL slug: NEVER_MOCK_APP_CODE → never-mock-app-code."""
    return str(principle_id).lower().replace("_", "-")


# Words that should stay uppercase when displaying group names.
UPPERCASE_WORDS = {"ui", "css", "html", "js", "api", "sql", "http"}


def display_name(name: str) -> str:
    """Convert a group name to display text: 'ui-debugging' → 'UI Debugging'."""
    words = name.replace("-", " ").split()
    return " ".join(
        w.upper() if w in UPPERCASE_WORDS else w.capitalize() for w in words
    )


def base_page(
    title: str,
    content: str,
    sidebar_html: str,
    css_path: str,
) -> str:
    """Full HTML document with sidebar and main content."""
    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<link rel="stylesheet" href="{escape(css_path)}">
</head>
<body>
<aside class="sidebar">
<div class="sidebar-title"><a href="{root_from_css(css_path)}">Principles</a></div>
{sidebar_html}
</aside>
<main class="main">
{content}
</main>
</body>
</html>
"""


def root_from_css(css_path: str) -> str:
    """Derive the root path from a css path like '../../css/style.css'."""
    # css_path is relative: "css/style.css", "../css/style.css", etc.
    # The root is css_path minus "css/style.css" at the end
    if css_path.endswith("css/style.css"):
        root = css_path[: -len("css/style.css")]
        return root if root else "."
    return "."


def sidebar_nav(
    groups: tuple[TaxonomyGroup, ...],
    current_group: str,
    root_path: str,
) -> str:
    """Navigation sidebar listing taxonomy groups."""
    items: list[str] = []
    for group in groups:
        display = display_name(group.name)
        active = ' class="active"' if group.name == current_group else ""
        href = f"{root_path}{group.name}/"
        items.append(f'<li><a href="{href}"{active}>{escape(display)}</a></li>')
    return f"<nav><ul>{''.join(items)}</ul></nav>"


def index_page(
    taxonomy: Taxonomy,
    principle_map: dict[PrincipleId, Principle],
) -> str:
    """Landing page: hero section, group card grid, and searchable principle index."""
    total_principles = len(taxonomy.get_all_principle_ids())
    total_groups = len(taxonomy.groups)

    parts: list[str] = []

    # Hero section
    parts.append('<div class="hero">')
    parts.append("<h1>Design Principles</h1>")
    if taxonomy.description:
        parts.append(f'<p class="description">{escape(taxonomy.description)}</p>')
    parts.append('<div class="stats">')
    parts.append(f"<span>{total_principles} principles</span>")
    parts.append(f"<span>{total_groups} groups</span>")
    parts.append("</div>")
    parts.append("</div>")

    # Group card grid
    parts.append('<section class="groups">')
    parts.append("<h2>Groups</h2>")
    parts.append('<div class="card-grid">')
    for group in taxonomy.groups:
        count = len(group.get_all_principle_ids())
        dname = display_name(group.name)
        parts.append(f'<a class="card" href="{group.name}/">')
        parts.append(
            f'<div class="card-header">'
            f'<span class="card-name">{escape(dname)}</span>'
            f' <span class="card-count">{count}</span>'
            f"</div>"
        )
        if group.description:
            parts.append(f'<p class="card-desc">{escape(group.description)}</p>')
        parts.append("</a>")
    parts.append("</div>")
    parts.append("</section>")

    # Principle index
    sorted_principles = sorted(
        (
            (pid, principle_map[pid])
            for pid in taxonomy.get_all_principle_ids()
            if pid in principle_map
        ),
        key=lambda pair: pair[1].title.lower(),
    )

    parts.append('<section class="index">')
    parts.append("<h2>All Principles</h2>")
    parts.append(
        '<input type="text" class="search-input" '
        'placeholder="Filter principles..." autocomplete="off">'
    )
    parts.append('<ul class="index-list">')
    for pid, p in sorted_principles:
        title_text = p.title.rstrip(".")
        lower_title = title_text.lower()
        parts.append(f'<li data-title="{escape(lower_title)}">')
        parts.append(
            f'<a class="index-title" href="principles/{slug(pid)}/">'
            f"{inline_markup(title_text)}</a>"
        )
        if p.essence:
            parts.append(f'<div class="index-essence">{inline_markup(p.essence)}</div>')
        parts.append("</li>")
    parts.append("</ul>")
    parts.append("</section>")

    # Inline search script
    parts.append(
        "<script>"
        "document.querySelector('.search-input')"
        ".addEventListener('input',function(e){"
        "var q=e.target.value.toLowerCase();"
        "document.querySelectorAll('.index-list li')"
        ".forEach(function(li){"
        "li.style.display=li.dataset.title.indexOf(q)!==-1?'':'none';"
        "});"
        "});"
        "</script>"
    )

    sidebar_html = sidebar_nav(taxonomy.groups, current_group="", root_path="")
    return base_page(
        title="Design Principles",
        content="\n".join(parts),
        sidebar_html=sidebar_html,
        css_path="css/style.css",
    )


def group_page(
    group: TaxonomyGroup,
    principle_map: dict[PrincipleId, Principle],
    taxonomy: Taxonomy,
) -> str:
    """Group page: description + list of principles."""
    display = display_name(group.name)
    parts: list[str] = []
    parts.append(f"<h1>{escape(display)}</h1>")
    if group.description:
        parts.append(f'<p class="description">{escape(group.description)}</p>')

    parts.append('<ul class="principle-list">')
    for pid in group.principle_ids:
        if pid in principle_map:
            p = principle_map[pid]
            title_text = p.title.rstrip(".")
            parts.append("<li>")
            parts.append(
                f'<div class="principle-title">'
                f'<a href="../principles/{slug(pid)}/">{inline_markup(title_text)}</a>'
                f"</div>"
            )
            if p.essence:
                parts.append(
                    f'<div class="principle-essence">{inline_markup(p.essence)}</div>'
                )
            parts.append("</li>")
    parts.append("</ul>")

    # Subgroups
    for subgroup in group.subgroups:
        sub_display = display_name(subgroup.name)
        parts.append(f"<h2>{escape(sub_display)}</h2>")
        if subgroup.description:
            parts.append(f'<p class="description">{escape(subgroup.description)}</p>')
        parts.append('<ul class="principle-list">')
        for pid in subgroup.principle_ids:
            if pid in principle_map:
                p = principle_map[pid]
                title_text = p.title.rstrip(".")
                parts.append("<li>")
                parts.append(
                    f'<div class="principle-title">'
                    f'<a href="../principles/{slug(pid)}/">{inline_markup(title_text)}</a>'
                    f"</div>"
                )
                if p.essence:
                    parts.append(
                        f'<div class="principle-essence">{inline_markup(p.essence)}</div>'
                    )
                parts.append("</li>")
        parts.append("</ul>")

    sidebar_html = sidebar_nav(
        taxonomy.groups, current_group=group.name, root_path="../"
    )
    return base_page(
        title=f"{display} — Design Principles",
        content="\n".join(parts),
        sidebar_html=sidebar_html,
        css_path="../css/style.css",
    )


def principle_page(
    principle: Principle,
    taxonomy: Taxonomy,
    principle_map: dict[PrincipleId, Principle],
) -> str:
    """Individual principle page with full content."""
    parts: list[str] = []

    # Breadcrumb
    paths = taxonomy.get_paths_for_principle(principle.id)
    if paths:
        group_name = paths[0].split("/")[0]
        group_display = display_name(group_name)
        parts.append(
            f'<div class="breadcrumb">'
            f'<a href="../../">Home</a> / '
            f'<a href="../../{group_name}/">{group_display}</a>'
            f"</div>"
        )

    title_text = principle.title.rstrip(".")
    parts.append(f"<h1>{inline_markup(title_text)}</h1>")

    if principle.essence:
        parts.append(f'<p class="essence">{inline_markup(principle.essence)}</p>')

    parts.append(f'<div class="principle-id">{escape(str(principle.id))}</div>')

    # Render content
    parts.append('<div class="content">')
    parts.append(markdown_to_html(principle.content))
    parts.append("</div>")

    # Tags
    if principle.tags:
        parts.append('<div class="tags">')
        for tag in principle.tags:
            parts.append(f'<span class="tag">{escape(tag)}</span>')
        parts.append("</div>")

    # Related principles
    if principle.related:
        parts.append('<div class="related">')
        parts.append("<h3>Related</h3>")
        parts.append("<ul>")
        for rid in principle.related:
            if rid in principle_map:
                rp = principle_map[rid]
                parts.append(
                    f'<li><a href="../{slug(rid)}/">{escape(str(rid))}: '
                    f"{escape(rp.title)}</a></li>"
                )
            else:
                parts.append(f"<li>{escape(str(rid))}</li>")
        parts.append("</ul>")
        parts.append("</div>")

    # Determine current group for sidebar highlighting
    current_group = ""
    if paths:
        current_group = paths[0].split("/")[0]

    sidebar_html = sidebar_nav(
        taxonomy.groups, current_group=current_group, root_path="../../"
    )
    return base_page(
        title=f"{strip_markup(principle.title)} — Design Principles",
        content="\n".join(parts),
        sidebar_html=sidebar_html,
        css_path="../../css/style.css",
    )


# === Minimal Markdown to HTML ===


def markdown_to_html(text: str) -> str:
    """Convert simple markdown to HTML.

    Handles: headings, code blocks, inline code, bold, italic,
    unordered/ordered lists, and paragraphs.
    """
    lines = text.split("\n")
    html_parts: list[str] = []
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
            heading_text = inline_markup(heading_match.group(2))
            html_parts.append(f"<h{level}>{heading_text}</h{level}>")
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
    return bool(re.match(r"^\d+\.\s+", line))


def strip_markup(text: str) -> str:
    """Remove markdown markers for use in plain-text contexts like <title>."""
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return text


def parse_table(lines: list[str]) -> str:
    """Parse markdown table lines into an HTML table."""
    parts: list[str] = ["<table>"]

    def split_row(line: str) -> list[str]:
        # Strip leading/trailing pipes, split on |
        return [cell.strip() for cell in line.strip("|").split("|")]

    # First line is the header
    headers = split_row(lines[0])
    parts.append("<thead><tr>")
    for h in headers:
        parts.append(f"<th>{inline_markup(h)}</th>")
    parts.append("</tr></thead>")

    # Skip separator line (|---|---|), render remaining as body
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
    """Convert inline markdown: code, bold, italic, links."""
    # Escape HTML first, then apply markdown
    text = escape(text)

    # Inline code (must come before bold/italic to avoid conflicts)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

    # Bold
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__([^_]+)__", r"<strong>\1</strong>", text)

    # Italic (using _ only, since * is used for bold)
    text = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"<em>\1</em>", text)
    # Also handle single * for italic when not part of **
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)

    return text
