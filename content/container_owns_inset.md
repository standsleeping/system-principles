---
id: CONTAINER_OWNS_INSET
title: "Container Owns Inset, Children Own Flow."
essence: "Inset belongs on the container; rhythm belongs in the container's gap; children own neither. Both responsibilities collapse into one property each at the container level, leaving children with square (or zero) padding."
related: [PADDING_IS_INSET_ONLY, SQUARE_PADDING_DEFAULT, SPACING_STRATEGY, BOUNDARY_OWNERSHIP]
---

Inset is a container concern. Rhythm between siblings is also a container concern. Children should not know how far they are from the container's edge, and they should not know how far apart they are from each other — both belong to the parent that arranges them.

**The Problem: Compounding Padding**

When both a container and its children apply horizontal padding, the inset compounds. The child's left edge sits at container-padding + child-padding from the container's border, creating an over-indented appearance that's hard to diagnose because neither value is wrong in isolation.

```css
/* Wrong: horizontal padding on both levels */
.list {
  padding: var(--spacing-md);
}
.list-item {
  padding: var(--spacing-sm) var(--spacing-md);  /* horizontal doubles up */
}
```

Worse, when different children have different horizontal padding (because they have different roles), their left edges misalign. The container can't enforce a consistent inset because it doesn't own it.

**The Solution: Both Responsibilities at the Container**

The container owns both inset and rhythm. `padding` carries the inset (square, all four sides). `gap` carries the rhythm (between siblings, governed by flex or grid). Children carry neither — they have square or zero padding and contribute only their content.

```css
.list {
  display: flex;
  flex-direction: column;
  padding: var(--spacing-md);    /* container owns inset — square */
  gap: var(--spacing-sm);        /* container owns rhythm */
}
.list-item {
  padding: 0;                    /* or square if the row needs its own inset */
}
```

All children share the same inset because the container owns it once. Their left edges align automatically. The rhythm between rows is consistent because `gap` enforces it without per-child declarations. Adding a new child type requires no padding decisions and no rhythm decisions — the parent already provides both.

The older formulation of this principle gave the child vertical-only padding (`padding: var(--spacing-sm) 0`) to express its participation in the flow. That worked but left the child carrying an asymmetric `padding` shape — which under `PADDING_IS_INSET_ONLY` is a conflation of inset and rhythm. Lifting the rhythm to the parent's `gap` resolves the conflation: each property does one job at exactly one level of the DOM.

**Relationship to Other Principles**

This principle works with `SPACING_STRATEGY` (gap for inter-element spacing), `SQUARE_PADDING_DEFAULT` (padding is always square), and `PADDING_IS_INSET_ONLY` (the asymmetric flow-rhythm concern lives in `gap`, not in padding).

It also complements `BOUNDARY_OWNERSHIP`, which addresses the same separation for borders: the container owns structural borders, children own their internal boundaries.

**The Pattern Name**

This separation is articulated in Every Layout (Bell and Pickering) as the composition of the Box primitive (container handles inset on all sides) and the Stack primitive (children spaced via gap). Both primitives live at the container level; the children are composed by them rather than expressing the composition themselves.
