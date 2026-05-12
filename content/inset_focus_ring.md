---
id: INSET_FOCUS_RING
title: "Inset the focus ring."
essence: "Draw the focus ring inside the element with a negative outline-offset whenever an outwardly offset ring would be clipped by an ancestor or collide with a sibling — list items, tabs, breadcrumbs, and any element inside a scroll or overflow-hidden container."
related: [FOCUS_STATES, SCROLL_CONTAINMENT, STABLE_SCROLLBAR_GUTTER]
---

The default focus ring (`outline: 2px solid ...; outline-offset: 2px`) draws 2px outside the element's border box. That works for elements that float in normal flow with margin around them. It breaks in two situations: when the element sits inside a clipped ancestor (the ring is cut off), and when the element is a sibling in a tight list or chrome strip (the ring overlaps neighbors).

## Cause: clipped ancestor

Setting `overflow` on either axis to anything other than `visible` (`auto`, `scroll`, `hidden`, `clip`) makes the *other* axis clip as well: the spec defines `overflow: visible` only when both axes are visible. So a typical sidebar declaration:

```css
.sidebar-main {
  overflow-y: scroll;
}
```

silently clips horizontally. Any focusable child whose box reaches the container's left/right edge will lose the left/right segments of an outwardly offset focus ring. Only the top and bottom segments survive, and the indicator looks fragmented (often two horizontal purple lines with no sides).

The same trap applies inside `overflow: hidden` cards, fixed-aspect tiles, segmented toggles with rounded clip masks, and any container with `contain: paint`.

## Cause: sibling collision

Even without a clipping ancestor, an outwardly offset ring overlaps adjacent siblings whenever items are tightly packed: rows in a list, tabs in a tab bar, crumbs in a breadcrumb, cells in a table. The 2px offset extends past the element's border into the neighbor's space, so the ring either renders on top of the neighbor's content or gets visually fragmented by the neighbor's border. The element does not need a clipping ancestor for this to look wrong; the collision is purely geometric.

## The fix

In both cases the fix is the same: draw the ring on the inside of the element.

```css
.sidebar a:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: -2px;
}
```

The negative offset pulls the ring 2px inside the element's border box, so the entire ring renders within the ancestor's content box and nothing gets clipped. The element's padding must be large enough that the ring does not collide with the text; with the standard `--spacing-md` padding this is usually fine.

## When to apply

Use a negative `outline-offset` whenever the focusable element falls into either category:

**Inside a clipping context** — full-bleed child of:

- A scroll container (`overflow-y: auto | scroll`, `overflow-x: ...`)
- A clipping container (`overflow: hidden | clip`)
- A paint-contained container (`contain: paint | strict`)
- A masked or rounded-clip container (border-radius + `overflow: hidden`)

**Adjacent to siblings** — an item in:

- A list of rows (sidebar nav, TOC, table rows, menu items)
- A tab bar or segmented control (siblings sharing a baseline)
- A breadcrumb trail or any inline chrome strip
- A table cell (siblings separated by 1px borders)

Use the standard positive offset for standalone controls that float in normal flow with margin around them: form inputs, standalone buttons, prose links, headings.

## Why not box-shadow

`box-shadow: 0 0 0 2px var(--color-focus-ring)` also draws inward when paired with `inset`, but it does not respect `forced-colors` mode the way `outline` does. Outlines are the accessibility-correct primitive for focus indication; the offset sign is the only thing that needs to change.
