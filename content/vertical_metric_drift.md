---
id: VERTICAL_METRIC_DRIFT
title: "Vertical metric drift."
essence: "Sibling inline elements drift along the block axis when each computes its inline-box height from a different reference (UA defaults vs cascade vs explicit override); anchor every peer's visible glyph rectangle to font metrics, not to line-height, to keep them aligned."
related: [PEER_RAIL, MIXED_HEIGHT_RHYTHM, FLAT_CLASSED_FLEX_TREE, RESET_FIRST]
---

A flex row mixes a `<span>`, a `<button>`, and a custom component. All three carry the same font-size, the same padding, the same border. Visually, the glyphs do not line up — one rides high, another sits low, a third looks centered. The boxes appear matched in DevTools. The text inside does not.

The cause is silent and structural. CSS computes each inline element's box height from `line-height × font-size`, but `line-height` arrives by three different paths depending on the element:

- A `<span>` inherits whatever `line-height` cascades from the page (often `1.5` or `1.6` for body-relaxed reading).
- A `<button>`, `<input>`, `<select>`, or `<textarea>` carries the UA default `line-height: normal`, which roughly resolves to the font's intrinsic ascender + descender ratio (typically `~1.0–1.2`). UA stylesheets explicitly break the cascade for form controls.
- A custom component or wrapper may set `line-height` explicitly, often to a third value.

Same font-size, same padding, three different line-box heights, three different outer-box heights — even when an "envelope match" makes the visible borders look equal. Worse, the visible glyphs sit at a position derived from each element's own line-box, so they land at different y-coordinates inside the row. `align-items: center` on the flex container centers the *boxes*, not the *glyphs*.

The classic symptom: a chrome rail with a count label next to a set of toggle buttons. The count is a span, the toggles are buttons. The author adds matching padding to the count to fix the obvious height mismatch. The boxes now visually align. The glyphs still don't. The drift is one to three pixels — small enough to look like an aliasing bug, large enough to read as wrong.

## The fix mechanisms, in order of robustness

**1. Anchor the visible glyph rectangle to font metrics.** `text-box: trim-both cap alphabetic` (or its longhand `text-box-trim: trim-both; text-box-edge: cap alphabetic`) crops the inline box on the block axis to the font's cap-height on top and alphabetic baseline on bottom. The trimmed rectangle is intrinsic to the font and indifferent to `line-height`. Apply it to every peer in the rail and `line-height` drops out of the alignment equation entirely:

```css
.rail-label,
.rail-button {
  text-box: trim-both cap alphabetic;
}
```

This is the only fix that survives a font change, a theme change, or a refactor that swaps a `<span>` for a `<button>`. It does change layout: the inline box becomes shorter (cap-height instead of line-box), so any padding or border around the element should be re-checked to ensure the visible row still has the intended outer height.

**2. Force a single `line-height` on the rail.** Set `line-height` explicitly on the flex container or on every child, overriding both UA defaults and cascade. Every peer's inline box now computes from the same multiplier:

```css
.chrome-rail,
.chrome-rail > * {
  line-height: 1;
}
```

This works but is brittle. UA defaults on form controls (`<button>`, `<input>`) may resist inheritance in older browsers; explicit `line-height: 1` on the controls themselves is sometimes required. And the value `1` collapses leading entirely, which can clip descenders if the rail's content is ever lowercase. A safer value is the font's natural line-height (`var(--font-line-height-tight)` in many systems, typically `1.1–1.2`).

**3. Avoid mixing element types.** If every peer in the rail is the same element (all `<button>`, or all `<span>`), they share the same UA-or-cascade source for `line-height` and the drift cannot arise. This is fragile — the first refactor that introduces a heterogeneous peer reopens the bug — but it is the cheapest fix when text-box-trim is unavailable.

## When the drift is invisible to box-level audits

A `PEER_RAIL` audit measures outer-box positions. It can verify that every strip on the rail has the same height. It cannot see vertical metric drift, because the drift is inside boxes that are correctly sized.

The detection probe is the visible-glyph rectangle, not the outer box. Two ways to measure it:

- **In DevTools**, select two peers and compare their `getBoundingClientRect()` *after* applying `text-box-trim` to a probe element with the same font. If the trimmed peers have different rects, line-height is still the variable.
- **In a layout audit**, render the page and walk every flex row whose children include inline text content. For each pair of inline-text children, measure the top of the first glyph and the bottom of the last. If those y-positions differ by more than `~1px` while the outer-box positions agree, vertical metric drift is present.

The audit cannot run on outer-box geometry alone, because identical outer boxes can contain misaligned glyphs.

## Where the drift commonly surfaces

- **Chrome rails** mixing inline text (counts, breadcrumbs, eyebrows) with form controls (`<button>`, `<input>`).
- **Tab strips** where the tab is a `<button>` or `<a>` sitting next to a `<span>` count or `<input>` filter.
- **Toolbar rows** with a mixture of icon buttons (UA `<button>`) and text labels (`<span>` or `<label>`).
- **Tables** where one column carries uppercase chrome (`<th>`) while another carries data with descenders; the line-box asymmetry between the two appears as row drift.
- **Mounted-component placeholders** — a placeholder `<span>` that the runtime fills with a component DIV inherits the surrounding line-height, sits as a much taller flex item than its mounted contents, and pushes the visible component off-center. The fix on the placeholder side is `display: contents`, which removes the placeholder's box from layout so the mounted component is the effective flex child. See the runtime-mount note below.

## Runtime-mount note

A component runtime that targets a caller-provided element via `mountEl.append(component)` should make the placeholder layout-transparent before appending:

```js
mountEl.innerHTML = '';
mountEl.style.display = 'contents';
mountEl.append(component);
```

`display: contents` deletes the placeholder's own box from the layout tree while preserving the element in the DOM (its attributes remain queryable). The mounted component becomes the effective flex/inline child of the placeholder's parent, inheriting the parent's line-height context directly rather than first passing through the placeholder's inflated line-box.

The alternative is `mountEl.replaceWith(component)`, which removes the placeholder entirely. That is cleaner conceptually but deletes the placeholder's `data-*` attributes from the DOM. Choose `display: contents` when the placeholder's identity matters (later queries, re-mounts, analytics hooks); choose `replaceWith` when it does not.

## Relationship to PEER_RAIL

`PEER_RAIL` says: parallel strips at the same y-position must share a single height token. It is a *box-level* contract.

`VERTICAL_METRIC_DRIFT` says: even when the boxes have matched heights, the *visible glyphs inside them* can drift if the inline-box heights inside the boxes come from different references. It is a *glyph-level* contract that sits beneath the box-level one.

A rail can satisfy `PEER_RAIL` (every strip is the same height) and still violate `VERTICAL_METRIC_DRIFT` (the visible text in each strip lands at a different y). The peer-rail audit cannot see this; a glyph-position audit must.

## Relationship to MIXED_HEIGHT_RHYTHM

`MIXED_HEIGHT_RHYTHM` covers prose flow where inline elements (math, code, badges) are taller than surrounding text; the cure is more `line-height` and `gap` to absorb the height variance.

`VERTICAL_METRIC_DRIFT` covers the inverse: inline elements with the *same intended height* drifting because their inline-box source differs. The cure is to remove the variance, not to absorb it.
