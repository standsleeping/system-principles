---
id: PEER_RAIL
title: "Peer Rail."
essence: "When parallel columns each carry a strip at the same y-position, those strips form one rail and must share a single height token."
related: [FIXED_FLEXIBLE_REGIONS, SCROLL_CONTAINMENT, BOUNDARY_OWNERSHIP, TOKEN_DRIVEN_DESIGN]
---

A multi-column shell (sidebar | main | aside, or any pair of vertically-aligned columns) often gives each column a fixed strip aligned across the layout: a topbar of labels at the y-origin, or a status footer at the bottom edge. Read horizontally across the layout, those strips form a single visual rail. The rail is real to the user even though the markup treats each strip as a per-column concern.

The constraint: every strip on the rail derives its height from the same token. One source of truth, three (or N) bindings.

A rail can sit at the top (a header rail), the bottom (a footer rail), or any other shared y-position. The principle is the same in every case; only the token name changes (`--layout-header-height`, `--layout-footer-height`, ...).

## What the height token names

The shared height names a *total visible height* — `box-sizing: border-box` is the canonical interpretation, so a strip's declared height includes its own borders. Strips that respect this convention align by default; strips that violate it stutter by exactly the border width.

The most common violation: the visible bottom rule is drawn by a wrapper element (a container's `border-bottom`) sitting *outside* the strip's `border-box`. The wrapper's height becomes `strip + border`, one border-width past the token's value, so the rule lands one pixel below sibling strips that drew their rule inside `border-box`. Same token, same value, different interpretation. Move the rule onto the element that owns the bound height — borders sit *inside* `border-box`, never on a wrapper that sizes itself by content.

## The cause

The bug is silent because each strip compiles in isolation. Four common ways the rail breaks:

1. **One strip uses `height`, another uses `padding + content`.** A `.topbar { height: var(--layout-header-height) }` resolves to a fixed value; a sibling `.aside-label { padding: var(--spacing-md) }` resolves to `padding * 2 + line-height * font-size`, which depends on three unrelated tokens. Whether the two coincide is accidental.

2. **Each strip picks its own token.** `.topbar` uses `--layout-topbar-height`, `.aside-label` uses `--layout-label-height`. Both are tokens, both are deliberate, but no contract ties them together — someone tunes one and the rail steps. The same trap applies to footer rails: `.main-footer { height: var(--layout-status-height) }` and `.aside-footer { height: var(--layout-toolbar-height) }` will drift independently.

3. **A strip is nested inside its column's scroll container.** Even under `NATIVE_SCROLLBAR`, nesting a rail strip inside a scroll container couples its visibility to the scroll position — a `position: sticky` strip can lag, jitter, or fall out of view at certain scroll positions. Rail strips go *outside* the scroll context, as siblings of the scroll container, not as children of it.

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

## Sharpening: quantization via cascading multiplier

The single-token form above assumes every page wants the same one-row strip. Real pages sometimes need two rows of controls in the rail (a filter strip above a results strip, a width-and-height row above an axes row, a title above a breadcrumb). Each new height is a new token name and a new coordination problem — the rail breaks every time content grows.

The fix is to make the rail height **an integer multiple of a base** rather than a single value. One token names the row; one cascading CSS variable names how many rows this page's rail occupies; every peer strip computes its height from the product.

```css
/* The base unit, "one chrome row" */
:root {
  --layout-chrome-bar-h: 2.5rem;
}

/* The page-level multiplier, defaults to 1 row, propagates via cascade */
.app-shell-body { --chrome-bar-rows: 1; }
.app-shell-body[data-chrome-rows="2"] { --chrome-bar-rows: 2; }
.app-shell-body[data-chrome-rows="3"] { --chrome-bar-rows: 3; }

/* Every peer-rail strip reads both */
.topbar,
.sidebar-section-label,
.aside-label,
.sticky-toc-summary {
  height: calc(var(--layout-chrome-bar-h) * var(--chrome-bar-rows, 1));
  display: flex;
  align-items: center;
  flex-shrink: 0;
}
```

A page whose rail is two rows tall declares it once on the shell:

```html
<div class="app-shell-body" data-chrome-rows="2">
```

Every strip inside that shell grows together by inheritance. Coordination is automatic — a new chrome strip doesn't need to know about its peers, only the formula.

### Why integer multiples

The fractional case (one strip at `1.5×`, another at `1×`) is the bug PEER_RAIL exists to prevent. Quantizing the multiplier to integers makes half-row offsets structurally impossible: the only legal heights are `1n × bar-h` for integer `n`, and the cascade ensures every strip on the rail picks the same `n`.

### The escape hatch

A single strip that genuinely should not participate in the rail (a slim status bar inside a 2-row page, a specialised inspector header) overrides the multiplier locally:

```html
<header class="topbar" style="--chrome-bar-rows: 1">…</header>
```

The override is in markup, not buried in component CSS — greppable, reviewable, and visible to whoever next reads the page.

### Enforcement

The cascade is the *expression* arm: it makes coordination free for components that opt into the formula. A component can still bypass the formula and hardcode `height: 3.5rem`. The complementary *enforcement* arm is a layout-rendering audit that walks the rendered page and flags two horizontal rules that sit *near-but-not-aligned* across sibling columns: close enough to look like an intended rail (within ~12px y), far enough to read as a stutter (more than ~1.5px y), with overlapping x ranges.

A stronger, declarative arm sits between cascade and shape detection: each rail member opts into the rail by setting a registered custom property (`--peer-rail: chrome`) in the same CSS rule that binds its height. An audit walks the DOM, finds every element computing the token, and verifies each member's rendered height matches `--layout-chrome-bar-h × --chrome-bar-rows` (resolved at the member's cascaded position via an inline probe). This catches drift that the near-miss border check cannot see: a rail member whose height *and* its neighbors' heights are all wrong by the same amount, a member in an unmeasured state (a drilled nav level, a collapsed sidebar), a member whose mismatch happens to align with no neighbor's border. The opt-in nature is the point: the contract belongs to the component, not to the framework's registry of class names.

- **Cascade**: coordination by default; no per-component opt-in
- **Declarative contract**: members tag themselves with `--peer-rail`; audit verifies each member's height against the formula
- **Near-miss border audit**: backstop for strips that escaped both the cascade and the contract

### When the multiplier doesn't apply

The multiplier is for **chrome strips on a peer rail**. It does not extend to body content (which has its own typographic rhythm via `MIXED_HEIGHT_RHYTHM`), to footer rails (which are an independent contract — different `data-chrome-rows` attribute if both rails grow, or a separate `--footer-rows` variable), or to one-off mid-column strips that are not on a rail. Apply quantization where strips already qualify as peers under the original principle.
