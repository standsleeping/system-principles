---
id: SPACING_STRATEGY
title: "Spacing Strategy."
essence: "Use flex gap for spacing between elements; it's more predictable and needs no last-child overrides."
---

Use modern CSS layout for spacing:

1. **Flex gap** for spacing between elements (not margins)
2. **Padding** for internal spacing within containers
3. Avoid the margin-bottom anti-pattern
4. Let flex containers manage distribution

```css
/* Prefer this */
.container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

/* Over this */
.container > * {
  margin-bottom: var(--spacing-2);
}
.container > *:last-child {
  margin-bottom: 0;
}
```

Gap-based spacing is more predictable and requires less override logic.

**Spacing creates groups.** Vary spacing to signal what belongs together. Tight spacing between a title and its subtitle says "these are a unit." More space before the next section says "new context." This is Gestalt proximity: elements near each other are perceived as related. Uniform spacing between all elements flattens the hierarchy and makes everything feel equally important.

**Consistent placement over optimal placement.** When a secondary element (a badge, link, or annotation) sometimes fits inline and sometimes wraps to a new line, the inconsistency is worse than either layout alone. Pick one position and use it always. If the element ever needs its own line, make it always a block. The small cost in compactness is repaid by a predictable visual rhythm that the eye can learn once and then stop noticing.

**Square padding on every element.** Padding represents a box's inset and is always one token on all four sides. Before writing a padding declaration, identify the element's role — but the role picks the *token*, not the shape:

- **Container** (primary content surface): square padding, larger-scale token.
- **Chrome** (utility strip attached to a container): square padding, mid-scale token.
- **Inline** (small control within chrome or a container): square padding, smaller-scale token. Horizontal floor for short labels comes from `min-width`, not from asymmetric padding.
- **Flow child** (element inside a flow container): square or zero padding. Vertical rhythm between rows lives in the parent's `gap`, not in the child's vertical padding.

Asymmetric padding makes elements look over-indented and visually unbalanced; it is the single most common spacing mistake. The asymmetric concerns it tries to express — horizontal breathing for inline text, vertical rhythm between flow children, top-heavy or bottom-heavy emphasis — live in `min-width`, `gap`, and `margin` respectively. See `PADDING_IS_INSET_ONLY` and `CONTAINER_OWNS_INSET`.