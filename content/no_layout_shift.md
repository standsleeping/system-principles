---
id: NO_LAYOUT_SHIFT
title: "No Layout Shift."
essence: "Toggling an element's visibility must never cause surrounding content to reflow. Reserve space for conditional elements so the layout remains stable."
---

When an element appears or disappears, surrounding content should not jump. This is **layout shift**, and it breaks the user's spatial memory of where things are on the page.

## The cause

`display: none` (Tailwind's `hidden`) removes an element from document flow entirely. When the element is toggled back in, every sibling and ancestor recalculates its position. The same applies to conditional rendering that adds or removes DOM nodes.

## The fix: reserve space

Use `visibility: hidden` (Tailwind's `invisible`) instead. The element remains in the flow and occupies its full box, but is simply not painted:

```html
<!-- Bad: causes layout shift -->
<button class="hidden" data-target="deselectButton">Deselect all</button>

<!-- Good: reserves space, no shift -->
<button class="invisible" data-target="deselectButton">Deselect all</button>
```

The JS toggle follows the same rule:

```js
// Bad
element.classList.toggle("hidden", !visible);

// Good
element.classList.toggle("invisible", !visible);
```

## When `hidden` is appropriate

`display: none` is still correct when the element's absence is the expected layout. Examples:

- **Structural slots** that are empty and should collapse (see EMPTY_STATE_COLLAPSE)
- **Expandable sections** like accordion content or format details, where the content below is expected to move
- **Removed content** that the user will not need to see again in the same interaction

The test: if the surrounding content's position is part of what the user is actively looking at, use `invisible`. If the user expects the layout to change (opening an accordion, navigating to a new section), `hidden` is fine.

## Cumulative Layout Shift (CLS)

This principle aligns with the web vitals metric **Cumulative Layout Shift**. CLS penalizes unexpected visual instability. The most common offenders:

1. **Toggled UI controls** (buttons, badges, banners) that push content around
2. **Images and embeds** loading without reserved dimensions
3. **Dynamic content** injected above the viewport

For toggled controls, `invisible` is the simplest and most reliable fix.
