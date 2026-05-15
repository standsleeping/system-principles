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

Earlier formulations carved out `padding: Y 0` as a legitimate flow-child pattern (the parent owned horizontal inset; the child owned vertical flow). Under `PADDING_IS_INSET_ONLY` and the updated `CONTAINER_OWNS_INSET`, that exception is gone: the flow rhythm lives in the parent's `gap`, not in the child's vertical padding. Both forms of zero-side padding — the smelly subtraction and the old "intentional" flow-child shape — migrate to a single fix.

The test is the same: if removing the zero-side override would cause spacing to *double* or *vanish*, the rule is a smell. The fix lives upstream — either at a shared parent's `gap`/`padding`, or by separating the concern that wanted asymmetry into the property that owns it.

**The fix**

Two options, in order of preference:

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
   No cancellation. Each container has square padding. The parent orchestrates flow.

2. **Remove the redundant neighbor padding.** If the list's padding-top was also cosmetic, delete it; the metrics container already provides the space.

The older "intentional flow-child" escape hatch (`padding: Y 0` on a row whose container owns horizontal inset) is no longer recommended — the same outcome is reachable with square padding on the container and `gap` on the container, leaving the row with square (or zero) padding. See `PADDING_IS_INSET_ONLY` and the updated `CONTAINER_OWNS_INSET`.

**Relationship to other principles**

Complements `SPACING_STRATEGY`'s square-padding rule with a specific diagnostic for the most common violation: the container-in-flow that cancels its own bottom padding. Under `PADDING_IS_INSET_ONLY` this smell becomes a hard signal — any non-1-value padding shorthand is a candidate for relocation, with no "legitimate flow-child asymmetry" exception left to carve out.

**How to catch it**

A scanner for non-1-value `padding:` shorthands (or `padding-*: 0` overrides on selectors that also set a general `padding:`) surfaces every site. With the exception list removed, the scanner becomes mechanical: each hit either lifts to the parent's `gap`, drops to square padding, or moves the asymmetric concern into `min-width` or `margin`.
