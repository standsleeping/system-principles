---
id: SQUARE_PADDING_DEFAULT
title: "Square Padding Default."
essence: "Padding is one token on all four sides on every element. The role classification picks which token; it does not pick the shape. Asymmetric concerns — text-shape compensation, flow rhythm, top-vs-bottom emphasis — live in min-width, gap, or a structural sibling spacer, not in padding (see PADDING_IS_INSET_ONLY and NEVER_MARGIN)."
related: [PADDING_IS_INSET_ONLY, PEER_EDGE_RESERVATION, ZERO_SIDE_PADDING_SMELL, CONTAINER_OWNS_INSET, RESET_FIRST, SPACING_STRATEGY]
---

Most CSS habits encourage asymmetric padding — `padding: 8px 16px` on a button, `padding: 0 24px` on a row, `padding: 12px 16px 8px` on a header. The pattern is so reflexive that hands type the two- or three-value form without ever considering whether it's needed. This default is wrong for every element it touches.

The rule reverses the reflex: every `padding` declaration has one token applied to all four sides. The role classification determines *which* token; it does not determine the shape. Two- and three-value `padding` shorthands are not used.

Concerns that look like they need asymmetric padding — horizontal breathing for inline text, vertical rhythm between flow children, extra space above a section header — are not padding concerns. They live in the property that owns the asymmetric concern: `min-width` for text-shape compensation, parent `gap` for inter-element rhythm, a structural sibling spacer for explicit gaps between unrelated regions. See `PADDING_IS_INSET_ONLY` for the responsibility separation, and `NEVER_MARGIN` for why margin is excluded.

## Why asymmetric is the wrong default

Asymmetric padding makes elements look over-indented and visually unbalanced. The horizontal "wings" pull the eye outward, the text floats too high in its box, and adjacent elements that share a column inherit the asymmetry to stay aligned — so the cost compounds. But the deeper problem is that asymmetric padding conflates two or three different concerns into one property: a button's `padding: sm md` is mixing *inset* with *text-shape compensation*; a row's `padding: md 0` is mixing *inset* with *flow rhythm*. Each concern wants its own property.

The reflex to reach for asymmetric padding usually traces to one of three roots:

1. **Inline button reflex.** Form buttons historically wear `padding: 8px 16px` because they sit in flowing text and need horizontal generosity for short labels to feel clickable. The horizontal generosity is real; the property is wrong. The fix is square padding plus `min-width` — the floor that makes "OK" still look like a button. See `PADDING_IS_INSET_ONLY` for the worked example.
2. **State-edge compensation.** A selected row reveals a 2px accent stripe on its left edge, so every peer gets `padding-left: calc(X + accent)` to compensate. Now the row's padding is asymmetric forever. The right fix is `PEER_EDGE_RESERVATION`: every peer carries a transparent equivalent of the accent at all times; square padding stays reachable.
3. **No role check.** The author reaches for whatever values look right in the moment, without asking which kind of element this is. The token defaults compound across the file.

## Identify the role first

Before writing `padding:`, classify the element by role. The role determines which scale of token applies — and whether an accompanying `min-width` or parent `gap` is needed. The role does *not* determine the shape of `padding`; padding is always square.

| Role | What it is | Token range | Companion property |
|---|---|---|---|
| **Container** | A primary content surface | Larger (`xl`–`3xl`) | — |
| **Chrome** | A utility strip attached to a container | Mid (`lg`–`xl`) | — |
| **Inline** | A small control within chrome or text flow | Smaller (`sm`–`md`) | `min-width` for horizontal floor |
| **Flow child** | An element inside a flow container | Smallest (`xs`–`sm`) | Parent's `gap` for rhythm |

All four roles get a single token on every side. The horizontal "breathing" that inline controls need, and the vertical rhythm that flow children need, live in their companion properties — not in an asymmetric padding shape.

The most common failure is misclassification: treating a list-row flow child as an inline button. A clickable element in a stacked list (nav row, table row, outline link, vertical tab) is a flow child *even when it's focusable*. The cue: if it has sibling rows above or below sharing a vertical rhythm, it's a flow child. The rhythm lives in the parent's `gap`, not the row's padding.

## Scale by role, not by feel

After role, pick a token from the scale appropriate to it: containers take larger tokens, chrome takes mid, inline and flow-child take smaller. The specific token names depend on the project's spacing scale, but the *direction* is universal — the more structural the role, the larger the token. Picking from the wrong end of the scale is a separate, secondary mistake; getting the shape (always square) right comes first.

## What replaces the old "asymmetric is warranted" cases

Two cases used to be considered legitimate asymmetric padding: inline-scale controls with horizontal breathing, and flow-child rows with vertical-only padding. Both are real concerns; neither is a padding concern. They migrate to dedicated properties:

```css
/* Inline pill — square padding, min-width floor */
.tag {
  padding: var(--spacing-xs);
  min-width: var(--control-min-width-sm);
}

/* List row inside a flow container — square padding, parent gap */
.list-container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  padding: var(--spacing-md);
}
.list-row {
  padding: 0;  /* or square, if the row needs its own inset */
}
```

The visual result matches the asymmetric originals at typical content sizes; the failure modes get better (short labels stop looking cramped, the rhythm stays consistent when row contents grow). See `PADDING_IS_INSET_ONLY` for the full responsibility separation and additional worked examples.

## Gap handles what padding can't

If symmetric padding doesn't give the visual rhythm an element needs — e.g. a section header that wants tight bottom and generous top — the asymmetry belongs in the parent's `gap` (and, when the gap above the header differs from the regular section rhythm, in a structural sibling spacer), not in padding. Gap is a between-siblings concern (the rhythm of the flow); padding is a box concern (this element's content-to-edge spacing). Conflating them is what produces three-value padding declarations like `padding: lg lg xs`. See `NEVER_MARGIN` for why margin is no longer the destination.

```css
/* ❌ Asymmetric padding to push items below away */
.section-header {
  padding: var(--spacing-lg) var(--spacing-md) var(--spacing-xs);
}

/* ✅ Square padding on the header; rhythm on the parent */
.section-stack {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}
.section-header {
  padding: var(--spacing-md);
}
```

## Relationship to PEER_EDGE_RESERVATION

Edge-revealing state changes (a selection accent, a focus inset, a status marker on one edge) are the single most common reason rows go asymmetric: the author "pays for" the active state's geometry by widening the rest state's padding. `PEER_EDGE_RESERVATION` removes that pressure — every peer reserves the channel via a transparent equivalent, so the active state mutates colour, not layout. With reservation in place, square padding is reachable; without it, the column-wide drift makes it nearly impossible.

## Relationship to ZERO_SIDE_PADDING_SMELL

`ZERO_SIDE_PADDING_SMELL` flags a different shape of the same problem: `padding: Y 0` or `padding: 0 X` is asymmetric in the extreme, with one axis entirely deleted. The two principles together rule out both partial and total asymmetry as defaults. The smell warns; the default forbids.
