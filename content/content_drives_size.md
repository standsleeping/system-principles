---
id: CONTENT_DRIVES_SIZE
title: "Content Sizes the Container; Decoration Fills It."
essence: "A container's dimensions should be driven by its content children, not by decorative or structural children. Use min-width for floors, not width for overrides."
---

**Content sizes the container; decoration fills it.** When a component has both content elements (text, labels, data) and decorative elements (color tiles, icons, visual indicators), the content determines the container's natural size. Decorative elements stretch to fill that size. Inverting this relationship (letting a fixed-size decorative child dictate the container width) suppresses content and causes overflow.

**The Problem: Decoration Suppressing Content**

Consider a color swatch component with a tile and a label:

```css
.swatch {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.swatch-color {
  width: 48px;   /* Fixed decorative width */
  height: 32px;
}
```

The color tile is 48px wide. Short labels ("100", "red") fit fine. But "punctuation" is wider than 48px, so it overflows its column and collides with neighbors. The decorative element (the tile) dictated the container's size, and the content (the label) was forced to comply.

This pattern appears whenever a structural or decorative child uses `width` instead of `min-width`:

- Color swatches where labels are longer than tiles
- Icon + text combinations where the icon constrains the row
- Thumbnail grids where captions overflow the image width

**The Fix: Let Content Lead**

Flip the relationship. The container sizes to its content; the decorative element stretches to fill:

```css
.swatch {
  display: flex;
  flex-direction: column;
  align-items: stretch;  /* Decoration fills the content width */
  min-width: 48px;       /* Floor, not ceiling */
}

.swatch-color {
  height: 32px;          /* No explicit width */
}
```

Now the swatch column is as wide as `max(48px, label width)`. Short labels get the 48px minimum; long labels expand the column, and the tile stretches to match. Content is never suppressed.

**The Rule**

Use `width` only on elements with no content-driven siblings. When a container has both decorative and content children:

1. Set `min-width` on the container (a floor, not an override)
2. Let the content child determine natural width
3. Use `align-items: stretch` so decorative children fill the content-determined width
