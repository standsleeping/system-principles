---
id: CONTAINER_OWNS_INSET
title: "Container Owns Inset, Children Own Flow."
essence: "Horizontal padding belongs on the container; children handle only vertical spacing via gap or vertical padding."
---

Horizontal inset is a container concern. Children should not know how far they are from the container's edge; they only know how far apart they are from each other.

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

**The Solution: Split Responsibility**

The container sets horizontal padding (inset from its edges). Children set only vertical padding (spacing between each other in the flow), or rely on the container's gap.

```css
.list {
  display: flex;
  flex-direction: column;
  padding: 0 var(--spacing-md);  /* container owns horizontal inset */
}
.list-item {
  padding: var(--spacing-sm) 0;  /* children own vertical flow spacing */
}
```

All children now share the same horizontal inset without declaring it themselves. Their left edges align automatically. Adding a new child type requires no horizontal padding decisions.

**Relationship to Other Principles**

This principle works with `SPACING_STRATEGY` (gap for inter-element spacing) and `SQUARE_PADDING_DEFAULT` (identify role before choosing padding). It refines the role identification: once you know an element is a child within a flow container, its horizontal padding is zero because the container already provides the inset.

It also complements `BOUNDARY_OWNERSHIP`, which addresses the same separation for borders: the container owns structural borders, children own their internal boundaries.

**The Pattern Name**

This separation is articulated in Every Layout (Bell and Pickering) as the composition of the Box primitive (container handles inset on all sides) and the Stack primitive (children spaced via gap). The container is the Box; the children participate in the Stack. Padding and flow are orthogonal concerns assigned to different levels of the DOM.
