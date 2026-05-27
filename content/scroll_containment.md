---
id: SCROLL_CONTAINMENT
title: "Scroll Containment."
essence: "Vertical scroll is allowed in exactly two layout slots: sidebars and the center content area. Horizontal scroll is allowed only inside individual content elements (a wide table, a code block) within the center — never at any layout container, including the center itself. Every container above a scrolling leaf clips with `overflow: hidden`."
related: [VIEWPORT_LOCKED, NO_PAGE_SCROLL, EDGE_ALWAYS_CHROME, INSET_VS_FLUSH_LAYOUT, SCROLLBAR_HIDDEN_BY_DEFAULT, ELASTIC_CONTENT_NEEDS_GIVE]
---

Scrolling is contained within an explicit allowlist of slots, never at the layout level. The shell clips; only specific leaves scroll, and the leaves are different for the two axes.

## Vertical scroll: two layout slots only

The only elements permitted to scroll vertically are:

1. **Sidebars** (left or right, in expanded state). The sidebar's content overflows the sidebar's height; the bar appears inside the sidebar's column.
2. **The center content area** (main content). The center's content overflows the center's height; the bar appears against the center's interior edge.

No other vertical scroll situations are allowed. Headers, footers, chrome rails, status bars, toolbars, and overlays all size to their content (or to a token-defined height) and do not scroll. If a header's content can grow taller than its row, it's misclassified — that content belongs in the center, with an in-content title.

## Horizontal scroll: inside content elements only, never at any layout container

**No layout container scrolls horizontally — not sidebars, not chrome, not even the center.** The center is a vertical-only scroll context; its width is whatever the layout shell gives it, and its content reflows or wraps to fit. A horizontal scrollbar attached to the center itself is a violation.

Horizontal scroll is allowed only inside individual content elements *within* the center, when the element's content explicitly demands it:

- A wide data table whose columns exceed its container width — the table scrolls horizontally inside its own bounds.
- A code block with long lines that should not wrap.
- A horizontal pannable image, sparkline strip, or carousel.

Each such element owns its own horizontal scroll context (`overflow-x: auto` on the element itself, not on any ancestor layout container). The center's width remains the center's width; the inner element's overflow is its own concern, and the scrollbar appears at the inner element's edge, not at the column edge.

If a sidebar's or chrome's content overflows its width, the region is misconfigured: either its width is wrong, or its content needs the responsive-component degradation pattern (see `RESPONSIVE_COMPONENTS`). The fix is *not* to add `overflow-x: auto` to the layout region; the fix is to reshape the content.

## The shell clips

Every container above a scrolling leaf carries `overflow: hidden`. The viewport-locked root, the chrome strip wrappers, the section panes, even the center — all clip on the axis they don't scroll. The hierarchy looks like:

```
:root        (height: 100vh, overflow: hidden)
└── layout   (display: flex, overflow: hidden)
    ├── header     (fixed height, no scroll)
    ├── content    (display: flex, overflow: hidden)
    │   ├── sidebar   (overflow-y: auto, overflow-x: hidden)   ← vertical scroll
    │   └── center    (overflow-y: auto, overflow-x: hidden)   ← vertical scroll
    │       ├── table-scroll  (overflow-x: auto)               ← horizontal scroll lives here
    │       ├── code-block    (overflow-x: auto)               ← or here
    │       └── ...other content that reflows or wraps
    └── footer     (fixed height, no scroll)
```

An `overflow-x: auto` declaration on any layout container (the layout, the content row, the sidebar, the center) breaks the allowlist. Horizontal scroll is a leaf-element affordance, not a region affordance. The reader should be able to predict from the structure where a scrollbar can appear; the rule is the contract.

## Why an allowlist, not a guideline

The earlier framing ("only leaf content areas scroll") was correct but soft — every project drifts into adding "just this one" extra scroll context: a toolbar that overflows, a footer with hidden actions, an inspector that scrolls separately from the sidebar, a center pane that scrolls horizontally to fit a wide chart. Each addition makes the page's scroll behavior less predictable. The split allowlist (two slots vertical at the layout level, content-element-only horizontal) collapses the ambiguity:

1. Adding a third vertical layout-scroll context, or a horizontal scroll at any layout container, requires the principle to change — not just one CSS file.
2. Audits mechanically check: any element with `overflow-y: scroll` / `overflow-y: auto` outside the sidebar and center selectors, or any element with `overflow-x: scroll` / `overflow-x: auto` whose role is "layout container," is a violation.
3. Designers can pre-commit to the constraint when shaping a new screen, rather than discovering it during implementation.

## Enforcement

The allowlist is mechanically checked by two complementary arms, so a regression fails a build or a test rather than waiting to be noticed in a browser.

**Authoring rule.** Declare the scrolling axis explicitly: `overflow-y: auto` for a vertical scroller, `overflow-x: auto` for a horizontal leaf. Never use the single-value shorthand `overflow: auto` (or `overflow: scroll`) on a layout container — it arms *both* axes, so one too-wide child silently turns the container into a horizontal scroller. The two-value form (`overflow: hidden auto`) is acceptable because the axes are stated explicitly.

**Static arm.** A CSS lint flags the single-value `overflow: auto` / `overflow: scroll` shorthand in shared component CSS. It runs at build time and catches the *capability* before it ships — the cheapest place to stop the regression. A genuinely two-axis-scrollable surface opts out with an inline marker.

**Runtime arm.** A headless audit loads each page at several widths and fails if (a) the page scrolls horizontally, (b) the center container's content overflows it — caught even when the cross axis is clipped, because `scrollWidth` still reports the overflow, or (c) any element is an *actual* horizontal scroller. A genuine leaf scroller (wide table, code block) opts out with a data attribute on itself or an ancestor.

The static arm prevents the common authoring mistake; the runtime arm catches overflow that only appears at certain widths or after dynamic content loads (`CONTINUOUS_MONITORING`). Together they make the clip-vs-scroll contract a checked invariant, not a convention. The narrow widths matter: this class of bug typically appears only when a fixed sidebar and inspector squeeze the center, so the audit must probe below the comfortable desktop width.

## Relationship to other principles

- `VIEWPORT_LOCKED` is the foundation: the root never scrolls.
- `EDGE_ALWAYS_CHROME` works downstream: chrome doesn't scroll, so it can own its edge slot stably.
- `INSET_VS_FLUSH_LAYOUT` chooses how chrome and content relate; the scrollbar treatment is uniform across both modes.
- `SCROLLBAR_HIDDEN_BY_DEFAULT` defines how every scroll container in this allowlist expresses scrolling: the bar is never painted, so the contract is structural (where scroll lives) without any visible-bar consequences.
