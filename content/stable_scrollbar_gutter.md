---
id: STABLE_SCROLLBAR_GUTTER
title: "Stable Scrollbar Gutter."
essence: "Reserve scrollbar space on intermittent scroll containers so the inner content-box width never depends on whether the bar is rendered."
related: [NO_LAYOUT_SHIFT, SCROLL_CONTAINMENT, INDEPENDENT_VIEWPORT]
---

NO_LAYOUT_SHIFT covers the vertical reflow caused by toggling element visibility. A second class of layout shift is *horizontal*, and its source is the scrollbar itself.

## The cause

A container with `overflow-y: auto` paints the vertical scrollbar only when content exceeds the container height. When user interaction changes content height across that threshold (collapse/expand, filter, search, lazy load, tab switch), the bar appears or disappears. The content-box width changes by the bar's width on every crossing, and every element inside reflows horizontally.

This is not Cumulative Layout Shift in the web-vitals sense; the user initiated the change. It still breaks spatial memory and reads as jitter.

## The fix

Declare `scrollbar-gutter: stable` on the scroll container:

```css
.scroll-region {
  overflow-y: auto;
  scrollbar-gutter: stable;
}
```

The gutter is reserved at all times, so the content-box width is invariant whether the bar is rendered or not.

## When to apply

On any `overflow-y: auto` (or `overflow-y: scroll`) container whose content height can cross the overflow threshold during user interaction:

- Hosts collapsibles, accordions, or expandable sections
- Has filter or search controls that hide rows
- Lazy-loads or paginates in place
- Has tabs that swap content of different lengths

Skip it when the container's content is static and either always or never overflows, or when the container is declared `overflow-y: scroll` with content known to fill it (the bar is permanent, so the gutter is permanent already).

## Companion: transparent track

`scrollbar-gutter: stable` reserves space for a track that may or may not contain a thumb. To prevent the reserved gutter from reading as a visible empty stripe when the thumb is short, pair it with a transparent track:

```css
html {
  scrollbar-width: thin;
  scrollbar-color: var(--color-border) transparent;
}
```

Transparent also avoids the wrong-shade problem when scroll containers nest inside surfaces of different shade: an opaque token-bound track bleeds the page background into nested surfaces.
