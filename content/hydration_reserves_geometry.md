---
id: HYDRATION_RESERVES_GEOMETRY
title: "Hydration Reserves Geometry."
essence: "When JavaScript fills a shell after load, the shell's regions already carry their final size from CSS at first paint. JS injects content into correct boxes; it never resizes the boxes. This extends NO_LAYOUT_SHIFT from the steady state to the load sequence."
related: [NO_LAYOUT_SHIFT, NO_FIRST_PAINT_FLASH, CONTENT_DRIVES_SIZE, FIXED_FLEXIBLE_REGIONS, EMPTY_STATE_COLLAPSE]
---

A common pattern ships empty structural slots and builds the chrome and content client-side after load — call it **hydration**. There is nothing wrong with it, except that the empty-to-filled transition is a layout shift unless the empty shell already occupies its final geometry. NO_LAYOUT_SHIFT governs toggles in the steady state; this principle is the same rule applied to the one moment every page passes through exactly once: the load.

## Render the invariant, hydrate the variable

The most predictable part of any page is its shell: the header, the footer, the rails, the scroll regions. The least predictable part is the content that fills them. So it is backwards to make the *shell* the dynamic thing and the content static. Render the shell statically — in the HTML, or at build time — with its regions sized by tokens (FIXED_FLEXIBLE_REGIONS), and let JavaScript pour *content* into boxes that are already the right size.

If the dynamic part of your load is the chrome and the static part is the content, you have inverted it.

## Reserve, don't compute-after

The regions' sizes are known before any data loads: fixed rails get their width from a token; the flexible center takes the rest. Persisted geometry — a resized panel, a collapsed rail — is restored in the same synchronous head bootstrap that establishes render state (NO_FIRST_PAINT_FLASH), so columns are correct in frame 0 rather than corrected in a `ResizeObserver` callback after paint.

```css
/* Reserved at first paint, before JS mounts anything into them */
.app-shell { display: grid; grid-template-columns: var(--rail-w) 1fr var(--inspector-w); }
.app-shell-left, .app-shell-right { overflow: hidden; }   /* clip, don't grow */
```

## Don't widen the empty window

Gating chrome construction behind asynchronous work — a config fetch, then a dynamic import, then a measure-and-collapse — stretches the empty-shell window to the duration of that work. Build the shell from static markup and synchronous state; defer only the work that genuinely needs the network.

## Test

Cumulative Layout Shift over the load should be ~0. Record the load as a filmstrip (or run a headless trajectory audit) and confirm that no region changes size between first paint and settled — only content appears inside regions that were already the right shape.
