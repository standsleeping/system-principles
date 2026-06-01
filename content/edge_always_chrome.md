---
id: EDGE_ALWAYS_CHROME
title: "The Edge is Always Chrome."
essence: "Every edge of the viewport is occupied by non-main-content: a header, a footer, a left sidebar, or a right sidebar. Main content never touches the viewport; chrome carries the boundary."
related: [VIEWPORT_LOCKED, BOUNDARY_OWNERSHIP, FIXED_FLEXIBLE_REGIONS, INSET_VS_FLUSH_LAYOUT, LAYOUT_VARIANTS]
---

The viewport edge is a load-bearing surface: it's where the user's eye lands first, where focus rings cling, where the OS chrome adjoins the application's. That surface must be owned, not borrowed from whatever happens to be at the edge of main content.

This principle elevates a structural constraint: every edge of the viewport is occupied by chrome (header, footer, left sidebar, right sidebar). Main content lives inside chrome, never against the viewport.

## The four edges

A viewport-locked shell composes four edge slots: top, bottom, left, right. Every slot is filled by chrome or by a collapsed-state stand-in for chrome.

| Edge | Possible chrome |
|---|---|
| Top | Header, app bar, breadcrumb rail, topbar |
| Bottom | Footer, status bar, action bar, bottom-tab bar |
| Left | Sidebar (expanded or icon-collapsed), nav rail, drawer handle |
| Right | Inspector, TOC rail, secondary sidebar, comment thread |

A collapsed sidebar (icon strip, e.g. 48px wide) is still chrome — the slot is filled. A hidden sidebar (overlay mode, off-screen) does *not* fill the slot; in that case, the edge must be filled by another piece of chrome (often a header or footer that extends all the way to that edge, or a thin nav rail).

The rule is not "you must have all four edges populated" — it's "every edge that's there must be chrome, never main content."

## Why this matters

The viewport is the unsalvageable boundary: nothing wraps around it, nothing rescales it, the user's cursor exits when crossing it. Main content abutting the viewport is content asked to do chrome's job — owning the boundary, providing the focal anchor, surviving overlap with browser UI.

Three failure modes appear when this rule slips:

1. **Content runs to the edge.** Body text whose first character sits at `x=0` because there's no left sidebar and no padding. The page reads as if the application is missing chrome rather than choosing not to have it.
2. **Chrome appears to float.** A toolbar with horizontal padding has its first interactive element inside the viewport, not at the viewport's edge. The visual edge is the viewport; the functional edge is offset. Users overshoot.
3. **Mode confusion.** When some edges are chrome and others are main content, the shell looks half-framed. The user's mental model of "where the app starts" becomes fuzzy.

## Diagnostic

For any shipped layout, walk the four viewport edges and identify which DOM element sits against each. If any element is main content (an article body, a code block, a chart canvas, a `<main>` descendant whose role is content), the rule is violated. The fix is to introduce or expand chrome on that side. Even minimal chrome — a 1px rule plus zero padding — is enough; the question is *what kind of element* the edge belongs to, not its visual weight.

A runtime audit pairs naturally with `LAYERED_UI_REVEAL`: stripping the UI to the base + chrome layer and inspecting each viewport edge for a chrome-class descendant.

## The collapsed-sidebar case

A sidebar in icon-collapsed state still occupies its edge slot. A sidebar in hidden state (`display: none` or `transform: translateX(-100%)` overlay) does not; the edge must be filled by something else — typically a header or footer extending all the way to that edge.

The tri-state encoding (`expanded` / `icon` / `hidden`) makes the slot-ownership explicit: the first two states fill the slot directly; the third state forces the slot to be filled by adjacent chrome.

## Relationship to other principles

- `VIEWPORT_LOCKED` provides the foundation: the root container is exactly the viewport. This principle adds: the edges of that container are chrome.
- `BOUNDARY_OWNERSHIP` says components own their boundaries. Chrome owns the viewport-edge boundary; main content does not need to draw one because it never reaches the viewport.
- `FIXED_FLEXIBLE_REGIONS` describes how chrome claims its space. This principle answers what fills the fixed regions: chrome, not main content.
- `INSET_VS_FLUSH_LAYOUT` is downstream: once chrome owns the edges, the content region inside chrome chooses inset or flush.
