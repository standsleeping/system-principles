---
id: PEER_RAIL
title: "Peer Rail."
essence: "When parallel columns each carry a strip at the same y-position, those strips form one rail and must share a single height token."
related: [FIXED_FLEXIBLE_REGIONS, SCROLL_CONTAINMENT, BOUNDARY_OWNERSHIP, TOKEN_DRIVEN_DESIGN]
---

A multi-column shell (sidebar | main | aside, or any pair of vertically-aligned columns) often gives each column a fixed strip aligned across the layout: a topbar of labels at the y-origin, or a status footer at the bottom edge. Read horizontally across the layout, those strips form a single visual rail. The rail is real to the user even though the markup treats each strip as a per-column concern.

The constraint: every strip on the rail derives its height from the same token. One source of truth, three (or N) bindings.

A rail can sit at the top (a header rail), the bottom (a footer rail), or any other shared y-position. The principle is the same in every case; only the token name changes (`--layout-header-height`, `--layout-footer-height`, ...).

## The cause

The bug is silent because each strip compiles in isolation. Four common ways the rail breaks:

1. **One strip uses `height`, another uses `padding + content`.** A `.topbar { height: var(--layout-header-height) }` resolves to a fixed value; a sibling `.aside-label { padding: var(--spacing-md) }` resolves to `padding * 2 + line-height * font-size`, which depends on three unrelated tokens. Whether the two coincide is accidental.

2. **Each strip picks its own token.** `.topbar` uses `--layout-topbar-height`, `.aside-label` uses `--layout-label-height`. Both are tokens, both are deliberate, but no contract ties them together — someone tunes one and the rail steps. The same trap applies to footer rails: `.main-footer { height: var(--layout-status-height) }` and `.aside-footer { height: var(--layout-toolbar-height) }` will drift independently.

3. **A strip is nested inside its column's scroll container.** The strip itself is fine, but the parent's scrollbar gutter cuts into the strip's right edge, visually breaking the rail at that column. (See SCROLL_CONTAINMENT: rail strips go *outside* the scroll, not as `position: sticky` children inside it.)

4. **The strip belongs to a surface that enters the layout later — an overlay, flyout, drawer, or modal header bar.** It compiles in isolation from the page chrome, so no one notices the height drift until both surfaces are visible at once. The same fix applies: bind to the rail's token. The rail is defined by what the eye sees when the overlay is open, not by DOM ancestry or stacking context.

## The fix

Define one token per rail and bind every peer strip to it as `height`, with `display: flex; align-items: center` for vertical centering of inline content:

```css
:root {
  --layout-header-height: 2.5rem;
  --layout-footer-height: 2.5rem;
}

/* Header rail */
.topbar,
.sidebar-section-label,
.aside-label {
  height: var(--layout-header-height);
  display: flex;
  align-items: center;
  padding: var(--spacing-md);  /* square, per PADDING_IS_INSET_ONLY */
  flex-shrink: 0;
}

/* Footer rail */
.sidebar-footer,
.main-footer,
.aside-footer {
  height: var(--layout-footer-height);
  flex-shrink: 0;
}
```

`flex-shrink: 0` keeps the strip from collapsing when the column flexes. Horizontal padding stays per-strip; only the height (the rail's defining axis) is shared. Header and footer rails are independent — they may share a value coincidentally, but they're distinct contracts and get distinct tokens.

## When peer status applies

Two strips are on the same rail when:

1. They sit at the same y-position in the layout — the top of their column or surface (header rail), the bottom (footer rail), or any other shared horizontal line — with no other peer-level chrome between them and that line.
2. They are visually continuous to the eye when read across the page — the user sees one horizontal band, not several independent labels.

Peer status is **not** limited to columns within the same shell. A flyout, drawer, modal header bar, or any overlay whose top (or bottom) edge lands at the y-position of a page rail is on that rail when it is visible. The stacking context is irrelevant — the rail is defined by what the eye sees, not by DOM ancestry. Bind the overlay's strip to the same rail token as the page chrome it sits over.

Two strips are *not* on the same rail when:

- One sits below additional chrome in its column or surface (e.g. a sidebar with a header section above the section label). That label is mid-column, not a peer of the topbar.
- The strips serve different semantic purposes that don't share a baseline (e.g. a top status bar vs. a sub-tab in a different column).
- An overlay's edge sits below or above the page rail (e.g. a centered modal with a margin from the top). It's a different surface, not a rail peer.
- One column carries a header strip and another carries a footer strip. They look symmetric but they are two distinct rails at two distinct y-positions; do not bind them to the same token.

When in doubt, the test is visual: render the layout (with any overlay open) and ask whether a horizontal line drawn across one edge of one strip lands on the same edge of every other. If yes, they're peers; bind them.

## Relationship to FIXED_FLEXIBLE_REGIONS

`FIXED_FLEXIBLE_REGIONS` covers *that* a region claims explicit space via tokens. PEER_RAIL covers the *coordination* across parallel regions: which token, and that they share it. A layout can satisfy `FIXED_FLEXIBLE_REGIONS` per-column (every strip uses some token) and still violate the rail (each column uses a different token).
