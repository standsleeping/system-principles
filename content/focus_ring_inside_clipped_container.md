---
id: FOCUS_RING_INSIDE_CLIPPED_CONTAINER
title: "Focus Ring Inside Clipped Container."
essence: "When a focusable element lives inside an overflow-clipped ancestor, draw its focus ring inside the element with a negative outline-offset so the indicator is not clipped."
related: [FOCUS_STATES, SCROLL_CONTAINMENT, STABLE_SCROLLBAR_GUTTER]
---

The default focus ring (`outline: 2px solid ...; outline-offset: 2px`) draws 2px outside the element's border box. That works for elements that float in normal flow, where the surrounding margin is `visible`. It breaks for elements that sit inside an ancestor with overflow clipping, because part of the ring lands outside the ancestor's content box and gets cut off.

## The cause

Setting `overflow` on either axis to anything other than `visible` (`auto`, `scroll`, `hidden`, `clip`) makes the *other* axis clip as well: the spec defines `overflow: visible` only when both axes are visible. So a typical sidebar declaration:

```css
.sidebar-main {
  overflow-y: scroll;
}
```

silently clips horizontally. Any focusable child whose box reaches the container's left/right edge will lose the left/right segments of an outwardly offset focus ring. Only the top and bottom segments survive, and the indicator looks fragmented (often two horizontal purple lines with no sides).

The same trap applies inside `overflow: hidden` cards, fixed-aspect tiles, segmented toggles with rounded clip masks, and any container with `contain: paint`.

## The fix

For elements inside a clipped ancestor, draw the ring on the inside of the element:

```css
.sidebar a:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: -2px;
}
```

The negative offset pulls the ring 2px inside the element's border box, so the entire ring renders within the ancestor's content box and nothing gets clipped. The element's padding must be large enough that the ring does not collide with the text; with the standard `--spacing-md` padding this is usually fine.

## When to apply

Use a negative `outline-offset` whenever the focusable element is a full-bleed child of:

- A scroll container (`overflow-y: auto | scroll`, `overflow-x: ...`)
- A clipping container (`overflow: hidden | clip`)
- A paint-contained container (`contain: paint | strict`)
- A masked or rounded-clip container (border-radius + `overflow: hidden`)

Use the standard positive offset for elements that float in normal flow, where the ring has room to breathe outside the element.

## Why not box-shadow

`box-shadow: 0 0 0 2px var(--color-focus-ring)` also draws inward when paired with `inset`, but it does not respect `forced-colors` mode the way `outline` does. Outlines are the accessibility-correct primitive for focus indication; the offset sign is the only thing that needs to change.
