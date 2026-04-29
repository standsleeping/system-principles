"""HTML template functions for the static site."""

from html import escape

from principles.types import Principle, PrincipleId, Taxonomy, TaxonomyGroup

from .markdown import inline_markup, render_markdown, strip_markup


# ================================================================
# NAMING / SLUGS
# ================================================================


def slug(principle_id: PrincipleId) -> str:
    """Convert a principle ID to a URL slug: NEVER_MOCK_APP_CODE → never-mock-app-code."""
    return str(principle_id).lower().replace("_", "-")


UPPERCASE_WORDS = {"ui", "css", "html", "js", "api", "sql", "http"}


def display_name(name: str) -> str:
    """Convert a group name to display text: 'ui-debugging' → 'UI Debugging'."""
    words = name.replace("-", " ").split()
    return " ".join(
        w.upper() if w in UPPERCASE_WORDS else w.capitalize() for w in words
    )


def root_from_css(css_path: str) -> str:
    """Derive the site-root URL from a css path like '../../css/style.css'."""
    if css_path.endswith("css/style.css"):
        root = css_path[: -len("css/style.css")]
        return root if root else "./"
    return "./"


# ================================================================
# PAGE SHELL
# ================================================================


def base_page(
    *,
    title: str,
    main_content: str,
    sidebar_html: str,
    css_path: str,
    root_path: str,
    context_label: str = "",
    toc_html: str = "",
    wide: bool = False,
) -> str:
    """Full HTML document: top header, left sidebar, main content, optional right TOC."""
    main_class = "main-content" + (" main-content-wide" if wide else "")
    toc_markup = ""
    if toc_html:
        toc_markup = (
            '<aside class="app-shell-right app-toc" aria-label="On this page">'
            f"{toc_html}"
            "</aside>"
        )
    context_markup = ""
    if context_label:
        context_markup = (
            f'<span class="app-header-context">{escape(context_label)}</span>'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{escape(css_path)}">
</head>
<body>
<a href="#main-content" class="sr-only">Skip to main content</a>
<div class="app-shell">
  <header class="app-shell-header app-header">
    <a class="app-header-brand" href="{escape(root_path) or "./"}">System Principles</a>
    <div class="app-header-meta">
      {context_markup}
    </div>
  </header>
  <div class="app-shell-body">
    <aside class="app-shell-left app-sidebar" aria-label="Taxonomy navigation">
      <div class="app-sidebar-main">
        {sidebar_html}
      </div>
    </aside>
    <main class="app-shell-main" id="main-content" tabindex="-1">
      <div class="{main_class}">
{main_content}
      </div>
    </main>
    {toc_markup}
  </div>
</div>
</body>
</html>
"""


# ================================================================
# SIDEBAR NAV
# ================================================================


def sidebar_nav(
    taxonomy: Taxonomy,
    principle_map: dict[PrincipleId, Principle],
    current_group: str,
    root_path: str,
) -> str:
    """Left-rail navigation: all taxonomy groups, with principle counts."""
    total = sum(1 for pid in taxonomy.get_all_principle_ids() if pid in principle_map)

    parts: list[str] = []

    # Overview section
    home_active = " nav-link-active" if current_group == "" else ""
    parts.append('<nav class="nav-section">')
    parts.append('<div class="nav-section-title">Overview</div>')
    parts.append(
        f'<a class="nav-link{home_active}" href="{escape(root_path)}">'
        "<span>Index</span>"
        f'<span class="nav-link-count">{total}</span>'
        "</a>"
    )
    parts.append("</nav>")

    # Groups section
    parts.append('<nav class="nav-section">')
    parts.append('<div class="nav-section-title">Groups</div>')
    for group in taxonomy.groups:
        count = sum(1 for pid in group.get_all_principle_ids() if pid in principle_map)
        display = display_name(group.name)
        active = " nav-link-active" if group.name == current_group else ""
        href = f"{root_path}{group.name}/"
        parts.append(
            f'<a class="nav-link{active}" href="{escape(href)}">'
            f"<span>{escape(display)}</span>"
            f'<span class="nav-link-count">{count}</span>'
            "</a>"
        )
    parts.append("</nav>")

    return "\n".join(parts)


# ================================================================
# BREADCRUMB
# ================================================================


def breadcrumb(crumbs: list[tuple[str, str | None]]) -> str:
    """Render a breadcrumb trail. Each crumb is (label, href_or_none)."""
    if not crumbs:
        return ""
    parts = ['<nav class="breadcrumb" aria-label="Breadcrumb">']
    for i, (label, href) in enumerate(crumbs):
        if i > 0:
            parts.append('<span class="breadcrumb-separator">/</span>')
        if href is None:
            parts.append(
                f'<span class="breadcrumb-crumb breadcrumb-current">{escape(label)}</span>'
            )
        else:
            parts.append(
                f'<a class="breadcrumb-crumb" href="{escape(href)}">{escape(label)}</a>'
            )
    parts.append("</nav>")
    return "".join(parts)


# ================================================================
# TOC (right rail)
# ================================================================


def toc_html_from_headings(headings: list[tuple[int, str, str]]) -> str:
    """Build right-sidebar TOC from a list of (level, text, anchor_id)."""
    if not headings:
        return ""
    parts = [
        '<div class="app-toc-main">',
        '<div class="app-toc-title">On this page</div>',
        '<div class="toc-list">',
    ]
    for level, text, anchor in headings:
        level_class = " toc-item-level-3" if level >= 3 else ""
        parts.append(
            f'<a class="toc-item{level_class}" href="#{escape(anchor)}">{escape(text)}</a>'
        )
    parts.append("</div>")
    parts.append("</div>")
    return "\n".join(parts)


# ================================================================
# PAGE NAV (prev/next)
# ================================================================


def find_container(
    principle_id: PrincipleId,
    taxonomy: Taxonomy,
) -> tuple[TaxonomyGroup | None, tuple[str, ...]]:
    """Find the innermost group whose principle_ids contains the principle.

    Returns (group_or_none, path_segments). Path segments are outer-to-inner.
    """

    def walk(
        groups: tuple[TaxonomyGroup, ...], prefix: tuple[str, ...]
    ) -> tuple[TaxonomyGroup | None, tuple[str, ...]]:
        for g in groups:
            path = prefix + (g.name,)
            if principle_id in g.principle_ids:
                return g, path
            sub, sub_path = walk(g.subgroups, path)
            if sub is not None:
                return sub, sub_path
        return None, ()

    return walk(taxonomy.groups, ())


def page_nav_html(
    current_id: PrincipleId,
    taxonomy: Taxonomy,
    principle_map: dict[PrincipleId, Principle],
) -> str:
    """Build previous/next navigation within the principle's containing group."""
    container, _ = find_container(current_id, taxonomy)
    if container is None:
        return ""

    ids = [pid for pid in container.principle_ids if pid in principle_map]
    if current_id not in ids:
        return ""

    idx = ids.index(current_id)
    prev_pid = ids[idx - 1] if idx > 0 else None
    next_pid = ids[idx + 1] if idx < len(ids) - 1 else None

    if prev_pid is None and next_pid is None:
        return ""

    def link(pid: PrincipleId, direction: str) -> str:
        label = "Previous" if direction == "prev" else "Next"
        p = principle_map[pid]
        title = strip_markup(p.title.rstrip("."))
        return (
            f'<a class="page-nav-link page-nav-link-{direction}" '
            f'href="../{slug(pid)}/">'
            f'<span class="page-nav-direction">{label}</span>'
            f'<span class="page-nav-title">{escape(title)}</span>'
            "</a>"
        )

    inner = ""
    if prev_pid is not None:
        inner += link(prev_pid, "prev")
    if next_pid is not None:
        inner += link(next_pid, "next")
    return f'<nav class="page-nav" aria-label="Pagination">{inner}</nav>'


# ================================================================
# INDEX PAGE
# ================================================================


def index_page(
    taxonomy: Taxonomy,
    principle_map: dict[PrincipleId, Principle],
) -> str:
    """Landing page: hero, stats, group table, filterable principle index."""
    all_ids = [pid for pid in taxonomy.get_all_principle_ids() if pid in principle_map]
    total_principles = len(all_ids)
    total_groups = len(taxonomy.groups)

    # Map each principle ID to its group's display name
    principle_to_group: dict[PrincipleId, tuple[str, str]] = {}
    for g in taxonomy.groups:
        for pid in g.get_all_principle_ids():
            principle_to_group[pid] = (g.name, display_name(g.name))

    parts: list[str] = []

    # Hero
    parts.append('<section class="hero">')
    parts.append('<div class="hero-eyebrow">Design principles · catalog</div>')
    parts.append('<h1 class="hero-title">System Principles</h1>')
    if taxonomy.description:
        parts.append(f'<p class="hero-description">{escape(taxonomy.description)}</p>')
    parts.append("</section>")

    # Stats
    parts.append('<div class="stats-bar">')
    parts.append(
        f'<div class="stat-item">'
        f'<span class="stat-value">{total_principles}</span>'
        f'<span class="stat-label">Principles</span>'
        f"</div>"
    )
    parts.append(
        f'<div class="stat-item">'
        f'<span class="stat-value">{total_groups}</span>'
        f'<span class="stat-label">Groups</span>'
        f"</div>"
    )
    parts.append(
        f'<div class="stat-item">'
        f'<span class="stat-value">{taxonomy.name.upper()}</span>'
        f'<span class="stat-label">Taxonomy</span>'
        f"</div>"
    )
    parts.append("</div>")

    # Groups table
    parts.append('<section class="section">')
    parts.append(
        '<div class="section-heading">'
        '<h2 class="section-heading-title">Groups</h2>'
        f'<span class="section-heading-meta">{total_groups} total</span>'
        "</div>"
    )
    parts.append('<div class="data-table-wrap">')
    parts.append('<table class="data-table">')
    parts.append(
        "<thead><tr>"
        '<th class="col-title">Group</th>'
        '<th class="col-essence">Description</th>'
        '<th class="col-count">Count</th>'
        "</tr></thead>"
    )
    parts.append("<tbody>")
    for g in taxonomy.groups:
        count = sum(1 for pid in g.get_all_principle_ids() if pid in principle_map)
        dname = display_name(g.name)
        desc = escape(g.description) if g.description else ""
        parts.append(
            f"<tr>"
            f'<td class="col-title" data-primary="true">'
            f'<a href="{escape(g.name)}/">{escape(dname)}</a>'
            f"</td>"
            f'<td class="col-essence" data-label="Description">{desc}</td>'
            f'<td class="col-count" data-label="Count">{count}</td>'
            f"</tr>"
        )
    parts.append("</tbody>")
    parts.append("</table>")
    parts.append("</div>")
    parts.append("</section>")

    # Principle index (filterable table)
    sorted_items = sorted(
        ((pid, principle_map[pid]) for pid in all_ids),
        key=lambda pair: pair[1].title.lower(),
    )
    parts.append('<section class="section">')
    parts.append(
        '<div class="section-heading">'
        '<h2 class="section-heading-title">All Principles</h2>'
        f'<span class="section-heading-meta" id="principle-count">{total_principles} total</span>'
        "</div>"
    )
    parts.append(
        '<div class="filter-bar">'
        '<span class="filter-label">Filter</span>'
        '<input type="text" id="principle-filter" class="filter-input" '
        'placeholder="Type to filter by title, ID, essence, or tag…" autocomplete="off">'
        '<span class="filter-count" id="filter-count"></span>'
        "</div>"
    )
    parts.append('<div class="data-table-wrap">')
    parts.append('<table class="data-table" id="principle-index">')
    parts.append(
        "<thead><tr>"
        '<th class="col-title">Title</th>'
        '<th class="col-essence">Essence</th>'
        '<th class="col-meta">Group</th>'
        "</tr></thead>"
    )
    parts.append("<tbody>")
    for pid, p in sorted_items:
        title_text = p.title.rstrip(".")
        essence_text = strip_markup(p.essence) if p.essence else ""
        tags_text = " ".join(p.tags)
        search_key = (
            f"{strip_markup(title_text).lower()} "
            f"{str(pid).lower()} "
            f"{essence_text.lower()} "
            f"{tags_text.lower()}"
        )
        group_info = principle_to_group.get(pid)
        group_line = ""
        if group_info:
            gname, gdisplay = group_info
            group_line = (
                f'<a href="{escape(gname)}/" class="meta-group">{escape(gdisplay)}</a>'
            )
        essence = inline_markup(p.essence) if p.essence else ""
        parts.append(
            f'<tr data-search="{escape(search_key)}">'
            f'<td class="col-title" data-primary="true">'
            f'<a href="principles/{slug(pid)}/">{inline_markup(title_text)}</a>'
            f"</td>"
            f'<td class="col-essence" data-label="Essence">{essence}</td>'
            f'<td class="col-meta" data-label="Group">'
            f"{group_line}"
            f'<span class="meta-id">{escape(str(pid))}</span>'
            f"</td>"
            f"</tr>"
        )
    parts.append("</tbody>")
    parts.append("</table>")
    parts.append("</div>")
    parts.append("</section>")

    # Filter script (served from public/js/filter.js)
    parts.append('<script src="js/filter.js" defer></script>')

    sidebar_html = sidebar_nav(taxonomy, principle_map, current_group="", root_path="")
    return base_page(
        title="System Principles",
        main_content="\n".join(parts),
        sidebar_html=sidebar_html,
        css_path="css/style.css",
        root_path="./",
        context_label="INDEX",
        wide=True,
    )


# ================================================================
# GROUP PAGE
# ================================================================


def render_principle_row(
    pid: PrincipleId,
    principle_map: dict[PrincipleId, Principle],
) -> str:
    """Render one row of the principle list table (for group pages)."""
    if pid not in principle_map:
        return (
            f'<tr><td class="col-title" colspan="2"><em class="text-muted">(missing)</em></td>'
            f'<td class="col-id">{escape(str(pid))}</td></tr>'
        )
    p = principle_map[pid]
    title_text = p.title.rstrip(".")
    essence = inline_markup(p.essence) if p.essence else ""
    return (
        f"<tr>"
        f'<td class="col-title" data-primary="true">'
        f'<a href="../principles/{slug(pid)}/">{inline_markup(title_text)}</a>'
        f"</td>"
        f'<td class="col-essence" data-label="Essence">{essence}</td>'
        f'<td class="col-id" data-label="ID">{escape(str(pid))}</td>'
        f"</tr>"
    )


def group_page(
    group: TaxonomyGroup,
    principle_map: dict[PrincipleId, Principle],
    taxonomy: Taxonomy,
) -> str:
    """Group page: breadcrumb, title, description, principle table, subgroups."""
    display = display_name(group.name)
    direct_count = sum(1 for pid in group.principle_ids if pid in principle_map)
    total_count = sum(
        1 for pid in group.get_all_principle_ids() if pid in principle_map
    )

    parts: list[str] = []

    # Breadcrumb
    parts.append(breadcrumb([("Home", "../"), (display, None)]))

    # Title + description
    parts.append(f'<h1 class="page-title">{escape(display)}</h1>')
    if group.description:
        parts.append(f'<p class="page-description">{escape(group.description)}</p>')

    # Meta strip
    parts.append('<div class="meta-strip">')
    parts.append(
        '<div class="meta-item">'
        '<span class="meta-label">Principles</span>'
        f'<span class="meta-value">{total_count}</span>'
        "</div>"
    )
    parts.append(
        '<div class="meta-item">'
        '<span class="meta-label">Direct</span>'
        f'<span class="meta-value">{direct_count}</span>'
        "</div>"
    )
    parts.append(
        '<div class="meta-item">'
        '<span class="meta-label">Subgroups</span>'
        f'<span class="meta-value">{len(group.subgroups)}</span>'
        "</div>"
    )
    parts.append("</div>")

    # Direct principles table
    if group.principle_ids:
        parts.append('<section class="section">')
        parts.append(
            '<div class="section-heading">'
            '<h2 class="section-heading-title">Principles</h2>'
            f'<span class="section-heading-meta">{direct_count} items</span>'
            "</div>"
        )
        parts.append('<div class="data-table-wrap">')
        parts.append('<table class="data-table">')
        parts.append(
            "<thead><tr>"
            '<th class="col-title">Title</th>'
            '<th class="col-essence">Essence</th>'
            '<th class="col-id">ID</th>'
            "</tr></thead>"
        )
        parts.append("<tbody>")
        for pid in group.principle_ids:
            parts.append(render_principle_row(pid, principle_map))
        parts.append("</tbody>")
        parts.append("</table>")
        parts.append("</div>")
        parts.append("</section>")

    # Subgroups
    for subgroup in group.subgroups:
        sub_display = display_name(subgroup.name)
        sub_count = sum(1 for pid in subgroup.principle_ids if pid in principle_map)
        parts.append('<section class="section">')
        parts.append(
            '<div class="section-heading">'
            f'<h2 class="section-heading-title">{escape(sub_display)}</h2>'
            f'<span class="section-heading-meta">{sub_count} items</span>'
            "</div>"
        )
        if subgroup.description:
            parts.append(
                f'<p class="page-description">{escape(subgroup.description)}</p>'
            )
        if subgroup.principle_ids:
            parts.append('<div class="data-table-wrap">')
            parts.append('<table class="data-table">')
            parts.append(
                "<thead><tr>"
                '<th class="col-id">ID</th>'
                '<th class="col-title">Title</th>'
                '<th class="col-essence">Essence</th>'
                "</tr></thead>"
            )
            parts.append("<tbody>")
            for pid in subgroup.principle_ids:
                parts.append(render_principle_row(pid, principle_map))
            parts.append("</tbody>")
            parts.append("</table>")
            parts.append("</div>")
        parts.append("</section>")

    sidebar_html = sidebar_nav(
        taxonomy, principle_map, current_group=group.name, root_path="../"
    )
    return base_page(
        title=f"{display} — System Principles",
        main_content="\n".join(parts),
        sidebar_html=sidebar_html,
        css_path="../css/style.css",
        root_path="../",
        context_label=f"GROUP · {display.upper()}",
        wide=True,
    )


# ================================================================
# PRINCIPLE PAGE
# ================================================================


def principle_page(
    principle: Principle,
    taxonomy: Taxonomy,
    principle_map: dict[PrincipleId, Principle],
) -> str:
    """Principle detail: breadcrumb, title, essence, meta, body, related, prev/next."""
    paths = taxonomy.get_paths_for_principle(principle.id)
    group_name = paths[0].split("/")[0] if paths else ""
    group_display = display_name(group_name) if group_name else ""

    parts: list[str] = []

    # Breadcrumb
    crumbs: list[tuple[str, str | None]] = [("Home", "../../")]
    if group_name:
        crumbs.append((group_display, f"../../{group_name}/"))
    crumbs.append((str(principle.id), None))
    parts.append(breadcrumb(crumbs))

    # Title
    title_text = principle.title.rstrip(".")
    parts.append(f'<h1 class="page-title-prose">{inline_markup(title_text)}</h1>')

    # Essence
    if principle.essence:
        parts.append(f'<p class="page-essence">{inline_markup(principle.essence)}</p>')

    # Meta strip
    parts.append('<div class="meta-strip">')
    parts.append(
        '<div class="meta-item">'
        '<span class="meta-label">ID</span>'
        f'<span class="meta-value">{escape(str(principle.id))}</span>'
        "</div>"
    )
    if group_name:
        parts.append(
            '<div class="meta-item">'
            '<span class="meta-label">Group</span>'
            f'<span class="meta-value">'
            f'<a href="../../{escape(group_name)}/">{escape(group_display)}</a>'
            f"</span>"
            "</div>"
        )
    if principle.tags:
        parts.append(
            '<div class="meta-item">'
            '<span class="meta-label">Tags</span>'
            f'<span class="meta-value">{len(principle.tags)}</span>'
            "</div>"
        )
    if principle.related:
        parts.append(
            '<div class="meta-item">'
            '<span class="meta-label">Related</span>'
            f'<span class="meta-value">{len(principle.related)}</span>'
            "</div>"
        )
    parts.append("</div>")

    # Main body
    body_html, headings = render_markdown(principle.content)
    parts.append('<div class="content">')
    parts.append(body_html)
    parts.append("</div>")

    # Tags
    if principle.tags:
        parts.append('<div class="tags">')
        for tag in principle.tags:
            parts.append(f'<span class="tag">{escape(tag)}</span>')
        parts.append("</div>")

    # Related
    if principle.related:
        parts.append('<section class="related-section">')
        parts.append(
            '<div class="section-heading">'
            '<h2 class="section-heading-title">Related</h2>'
            f'<span class="section-heading-meta">{len(principle.related)} principles</span>'
            "</div>"
        )
        parts.append('<div class="related-list">')
        for rid in principle.related:
            if rid in principle_map:
                rp = principle_map[rid]
                rp_title = strip_markup(rp.title.rstrip("."))
                parts.append(
                    f'<div class="related-item">'
                    f'<span class="related-id">{escape(str(rid))}</span>'
                    f'<a class="related-title" href="../{slug(rid)}/">{escape(rp_title)}</a>'
                    f"</div>"
                )
            else:
                parts.append(
                    f'<div class="related-item">'
                    f'<span class="related-id">{escape(str(rid))}</span>'
                    f'<span class="related-title text-muted">(missing)</span>'
                    f"</div>"
                )
        parts.append("</div>")
        parts.append("</section>")

    # Prev/next nav
    parts.append(page_nav_html(principle.id, taxonomy, principle_map))

    sidebar_html = sidebar_nav(
        taxonomy, principle_map, current_group=group_name, root_path="../../"
    )
    toc_html = toc_html_from_headings(headings)
    plain_title = strip_markup(title_text)
    return base_page(
        title=f"{plain_title} — System Principles",
        main_content="\n".join(parts),
        sidebar_html=sidebar_html,
        css_path="../../css/style.css",
        root_path="../../",
        context_label=f"PRINCIPLE · {str(principle.id)}",
        toc_html=toc_html,
    )
