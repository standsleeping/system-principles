---
id: BOUNDARY_OWNERSHIP
title: "Boundary Ownership."
essence: "Each component should look visually complete in isolation; relying on a neighbor for your edge is implicit coupling."
related: [ADJACENT_BAR_BASELINE, CONTAINER_OWNS_INSET, CONTENT_DRIVES_SIZE, PADDING_IS_INSET_ONLY]
---

Components own their own visual boundaries. This applies to both parent/child and sibling relationships.

**Parent/Child: Container Owns Border, Child Owns Padding**

When a container has structural borders (separating header from content, for example), the container defines those borders. Children provide their own internal padding.

**Separator Containers: Frame and Content Split**

When a container uses borders to separate repeated sections (e.g. a scrollable list of sections with horizontal rules between them), separate the *frame* (which owns the structural border and spans full width) from the *content* (which owns its own square inset). One element does one job:

```css
.section-frame                    { /* full-width frame owns the separator */ }
.section-frame + .section-frame   { border-top: 1px solid var(--color-border); }
.section-frame > .section-content { padding: var(--spacing-2xl); }
```

```html
<div class="section-frame">
  <div class="section-content">…</div>
</div>
<div class="section-frame">
  <div class="section-content">…</div>
</div>
```

The frame element owns the border, which spans pane-edge to pane-edge because the frame has no padding to interfere. The content element owns square inset on every side. No box-model coincidences, no position tricks, no pseudo-elements; each element has exactly one structural job.

This is the same pattern DK calls "bookend frame for flush dividers" (see `visual-language.md`) and what makes `PADDING_IS_INSET_ONLY` reachable in the separator-container case: instead of folding two concerns (border placement + content inset) into one element with an asymmetric padding shape, separate them into two elements with one concern each.

**Siblings: Each Component Completes Itself**

When two components sit adjacent, each should be visually complete in isolation. A component shouldn't rely on its neighbor to provide its visual edge.

**Test**: If you render each component alone, which one looks incomplete?

```
nav (no bottom border)     →  looks unfinished
content (no top border)    →  looks fine
```

The nav owns the border because it's incomplete without it:

```css
nav {
  border-bottom: 1px solid var(--gray-200);
}
```

The content area shouldn't add a top border to compensate for the nav's missing boundary. That creates implicit coupling.

**Detection: doubled parallel rules**

The most common violation is two elements drawing the same edge — a wrapper's `border-right` and the wrapped component's `border-right` rendered at the same x-coordinate, producing a sub-pixel "shadow" (often around 0.8px) that reads as a rendering bug. CSS lint can't see this because adjacency is layout-dependent.

Detect at runtime. For each visible element, project its four border edges onto axis-pos line segments (top/bottom = horizontal at y, left/right = vertical at x). Flag any pair of *parallel* segments (same axis) whose positions sit within ~1px of each other AND whose orthogonal ranges meaningfully overlap (≥ 4px). Tip-to-tip continuations are excluded by the overlap floor; corner intersections are excluded because they're orthogonal axes.

```js
// Sketch — minus details, this is the whole algorithm:
for (const el of doc.querySelectorAll('*')) {
  const cs = getComputedStyle(el);
  const r = el.getBoundingClientRect();
  for (const side of ['top', 'right', 'bottom', 'left']) {
    if (parseFloat(cs[`border${side[0].toUpperCase()}${side.slice(1)}Width`]) < 0.5) continue;
    if (cs[`border${side[0].toUpperCase()}${side.slice(1)}Color`] === 'rgba(0, 0, 0, 0)') continue;
    lines.push({ el, side, axis: /top|bottom/.test(side) ? 'h' : 'v',
                 pos: r[side === 'top' || side === 'left' ? side : (side === 'right' ? 'right' : 'bottom')],
                 start: /top|bottom/.test(side) ? r.left : r.top,
                 end:   /top|bottom/.test(side) ? r.right : r.bottom });
  }
}
// Pairs of (a, b) where a.axis === b.axis, |a.pos - b.pos| < 1.5,
// and overlap between their ranges ≥ 4 → doubled rule.
```

Wire this as a build-time check by loading each shipped page in a headless iframe and running the audit. Failures get a clear report (selector pair, axis, position, overlap length); fixing means deciding which element owns the edge and removing the duplicate.