---
id: ZERO_SIDE_PADDING_SMELL
title: "Zero-Side Padding is a Smell."
essence: "A padding declaration with a zero side almost always means a container is deleting spacing it's about to reintroduce somewhere else."
---

When you see `padding: X Y 0` (or any rule where one side of padding is explicitly zero while the others are non-zero on a non-inline element), pause. The author usually wasn't aiming for asymmetry — they were canceling a side to prevent spacing from doubling with a sibling or child. That cancellation is a coupling: this container's padding now depends on the next element's padding to look right.

**Why the anti-pattern appears**

```css
.metrics {
  padding: var(--spacing-xl);
  padding-bottom: 0;  /* avoid doubling with .list padding-top below */
}
.list {
  padding: var(--spacing-xl);
}
```

The author tried to square the metrics container but noticed a double gap between it and the list. Instead of fixing the spacing at the right level (the parent), they subtracted one side. The visible layout is now correct, but the rule is implicit and fragile: change the list's top padding and the metrics spacing breaks.

**Why it's a smell, not a rule**

Legitimate zero-side padding exists — flow children are designed with `padding: Y 0` because their container owns the horizontal inset (see `CONTAINER_OWNS_INSET`). The difference is ownership:

- **Flow child**: the zero side is intentional — the parent fills that axis via its own padding or gap. Consistent, declarative.
- **Smell**: the zero side is reactive — the author is *subtracting* to neutralize a sibling's space. Coupled, fragile.

The test: if removing the zero-side override would cause spacing to *double*, the rule is a smell. The fix lives upstream.

**The fix**

Three options, in order of preference:

1. **Lift to a parent gap.** Put the spacing on the common parent:
   ```css
   .page-section {
     display: flex;
     flex-direction: column;
     gap: var(--spacing-xl);
   }
   .metrics { padding: var(--spacing-xl); }
   .list    { padding: var(--spacing-xl); }
   ```
   No cancellation. Each container has square, symmetric padding. The parent orchestrates flow.

2. **Remove the redundant neighbor padding.** If the list's padding-top was also cosmetic, delete it; the metrics container already provides the space.

3. **If neither fits, own the asymmetry.** Move the element into a flow-child role explicitly: strip horizontal padding from the flow child and put it on the container. This is no longer the smell — it's the flow-child pattern.

**Relationship to other principles**

Complements `SPACING_STRATEGY`'s "square padding by default" with a specific diagnostic for the most common violation: the container-in-flow that cancels its own bottom padding. Refines `CONTAINER_OWNS_INSET` by distinguishing intentional flow-child asymmetry from reactive anti-padding.

**How to catch it**

A grep for three-value `padding:` declarations (or `padding-*: 0` overrides on selectors that also set a general `padding:`) surfaces candidates quickly. Most hits are smells; a small minority are legitimate flow-child declarations that should instead be written as `padding: Y 0` unambiguously.
