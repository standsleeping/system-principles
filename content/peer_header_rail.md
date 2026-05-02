---
id: PEER_HEADER_RAIL
title: "Peer Header Rail."
essence: "When parallel columns each carry a header strip at the same y-position, those strips form one rail and must share a single height token."
related: [FIXED_FLEXIBLE_REGIONS, SCROLL_CONTAINMENT, BOUNDARY_OWNERSHIP, TOKEN_DRIVEN_DESIGN]
---

A multi-column shell (sidebar | main | aside, or any pair of vertically-aligned columns) often gives each column a header strip at the top: a label, a topbar, a toolbar. Read horizontally across the layout, those strips form a single visual rail. The rail is real to the user even though the markup treats each strip as a per-column concern.

The constraint: every strip on the rail derives its height from the same token. One source of truth, three (or N) bindings.

## The cause

The bug is silent because each column compiles in isolation. Three common ways the rail breaks:

1. **One strip uses `height`, another uses `padding + content`.** A `.topbar { height: var(--layout-header-height) }` resolves to a fixed value; a sibling `.aside-label { padding: var(--spacing-md) }` resolves to `padding * 2 + line-height * font-size`, which depends on three unrelated tokens. Whether the two coincide is accidental.

2. **Each column picks its own token.** `.topbar` uses `--layout-topbar-height`, `.aside-label` uses `--layout-label-height`. Both are tokens, both are deliberate, but no contract ties them together — someone tunes one and the rail steps.

3. **One column nests the strip inside its scroll container.** The strip itself is fine, but the parent's scrollbar gutter cuts into the strip's right edge, visually breaking the rail at that column. (See SCROLL_CONTAINMENT: headers go *outside* the scroll, not as `position: sticky` children inside it.)

## The fix

Define one token and bind every peer strip to it as `height`, with `display: flex; align-items: center` for vertical centering of inline content:

```css
:root {
  --layout-header-height: 2.5rem;
}

.topbar,
.sidebar-section-label,
.aside-label {
  height: var(--layout-header-height);
  display: flex;
  align-items: center;
  padding: 0 var(--spacing-md);
  flex-shrink: 0;
}
```

`flex-shrink: 0` keeps the strip from collapsing when the column flexes. Horizontal padding stays per-strip; only the height (the rail's defining axis) is shared.

## When peer status applies

Two strips are on the same rail when:

1. They sit at the same y-position in the layout (top of their column, with no other peer-level chrome above them).
2. They are visually continuous to the eye when read across columns — the user sees one horizontal band, not three independent labels.

Two strips are *not* on the same rail when:

- One sits below additional chrome in its column (e.g. a sidebar with a header section above the section label). That label is mid-column, not a peer of the topbar.
- The strips serve different semantic purposes that don't share a baseline (e.g. a top status bar vs. a sub-tab in a different column).

When in doubt, the test is visual: render the layout and ask whether a horizontal line drawn across the top of one strip lands on the top of every other. If yes, they're peers; bind them.

## Relationship to FIXED_FLEXIBLE_REGIONS

`FIXED_FLEXIBLE_REGIONS` covers *that* a region claims explicit space via tokens. PEER_HEADER_RAIL covers the *coordination* across parallel regions: which token, and that they share it. A layout can satisfy `FIXED_FLEXIBLE_REGIONS` per-column (every strip uses some token) and still violate the rail (each column uses a different token).
