---
id: PEER_EDGE_RESERVATION
title: "Peer Edge Reservation."
essence: "When one state of an interactive item reveals a visual element at one edge (an accent stripe on selection, a status marker, a focus inset), every peer reserves that same edge via a transparent equivalent; never compensate for it with asymmetric padding on the row or its neighbours."
related: [NO_LAYOUT_SHIFT, SQUARE_PADDING_DEFAULT, CONTAINER_OWNS_INSET, ZERO_SIDE_PADDING_SMELL, STATE_BELONGS_TO_INTERACTIVE, PEER_RAIL]
---

An interactive list — nav items, segmented options, tabs, table rows — typically has an active state that reveals a thin visual element at one edge of the active row: a 2px accent stripe on the left for selection, a focus inset on all four sides, a status dot on the right. The active row's content cannot occupy that edge; some space has to be reserved for the indicator.

The question is *where* the reservation lives. There are two answers, and only one of them survives contact with the rest of the layout.

## The trap: compensate with padding

The local-feeling answer is to ask every inactive peer to leave a hole in its padding where the active state's indicator would otherwise live:

```css
/* ❌ Asymmetric padding compensates for an accent that only exists when selected */
.row              { padding: var(--spacing-sm) var(--spacing-lg); }
.row:not(.is-selected) {
  /* match the visual offset that .is-selected's border-left will introduce */
  padding-left: calc(var(--spacing-lg) + var(--border-width-accent));
}
.row.is-selected  { border-left: 2px solid var(--accent); }
```

That arithmetic appears benign in isolation, but it leaks:

1. **Every sibling adopts the offset.** Section headers, group labels, chrome strips, and the column's own header all need to align with the row content — so each gets its own `calc(X + accent)` left-pad. The compensation becomes a column-wide tax.
2. **The padding is now asymmetric.** Row padding is `sm lg`, header padding is `0 lg 0 calc(lg + accent)`. Symmetric square padding is no longer reachable without rethinking the indicator.
3. **State changes shift content.** Even with the calc, hover/focus indicators added later (a faint left tint, a focus ring) re-open the same question, and the answer keeps drifting.
4. **The CSS encodes geometry the user can't see.** A reader asks "why `calc(lg + accent)` and not `lg`?" — and the answer is a state that may not even be visible on the page in front of them.

## The fix: reserve via a transparent peer

Move the reservation onto the indicator itself, in its inactive form. Every peer carries the indicator at all times; the *state* only changes its colour:

```css
/* ✅ Every peer reserves the accent channel via a transparent equivalent */
.row {
  padding: var(--spacing-md);
  border-left: var(--border-width-accent) solid transparent;
}
.row.is-selected { border-left-color: var(--accent); }

/* Other elements in the same column do the same — square padding throughout */
.section-header {
  padding: var(--spacing-md);
  border-left: var(--border-width-accent) solid transparent;
}
.column-header {
  padding: var(--spacing-md);
  border-left: var(--border-width-accent) solid transparent;
}
```

The accent channel is now a *fixed structural feature* of the row, not a state-dependent geometry adjustment. Row padding stays square. The active state mutates a colour, not a layout. Every sibling can adopt the same `border-left` reservation and the column's left edge becomes one continuous channel — content aligns naturally with zero `calc`.

The reservation can be a border, an outline placeholder, a pseudo-element, or a fixed-width column in a grid — whatever paints zero pixels in the inactive state while occupying the geometry. Pick the one that matches how the active state will paint.

## When this applies

The principle is about *peer alignment under state changes*. It applies whenever:

1. An interactive item has multiple states (default / hover / focus / selected / disabled).
2. At least one state reveals a visual element on an edge of the item — accent stripe, focus ring inset, status icon, leading checkbox column, sort arrow column.
3. The item has visible peers above, below, or beside it that share content alignment with it.

It does **not** apply when:

- The "indicator" is the item's content itself (e.g. text that bolds on hover). No geometry change, no reservation needed.
- The indicator overlays the item from a different stacking context (e.g. an absolutely-positioned focus ring outside the row's flow). The row's geometry is unaffected.
- The item has no peers (a one-off button, a free-floating control). There's nothing to align with.

## Relationship to NO_LAYOUT_SHIFT

`NO_LAYOUT_SHIFT` is the general principle: toggling visibility must not reflow surrounding content; reserve space for conditional elements. `PEER_EDGE_RESERVATION` is its specific corollary for edge indicators on interactive items — the most common case where layout shift sneaks in through *appearance changes* rather than visibility toggles. The state change isn't "show / hide an element," it's "recolour an edge that was always there."

## Relationship to SQUARE_PADDING_DEFAULT

`SQUARE_PADDING_DEFAULT` says padding should be a single token on all four sides for everything that isn't an inline-scale control. The edge-accent compensation pattern is the single most common reason rows go asymmetric and violate that default. `PEER_EDGE_RESERVATION` is what makes the default reachable: with reservation in place, the active state mutates colour, not layout, and the row's padding can stay square. Without it, the column-wide drift makes square padding nearly impossible to keep.
