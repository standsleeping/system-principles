---
id: PADDING_IS_INSET_ONLY
title: "Padding is Inset Only."
essence: "Padding represents a box's uniform inset and is square on every element. Asymmetric concerns — horizontal breathing around inline text, vertical rhythm between flow children, edge-heavy emphasis — live in the property that owns the asymmetric concern: min-width/min-height for control sizing, gap for inter-element rhythm, margin for layout."
related: [SQUARE_PADDING_DEFAULT, CONTAINER_OWNS_INSET, ZERO_SIDE_PADDING_SMELL, SPACING_STRATEGY, CONTENT_DRIVES_SIZE]
---

Padding is the space between an element's border and its content — its *inset*. A box has one inset; the inset is uniform; padding is square. Every legitimate-looking use of asymmetric padding is a different concern wearing padding's costume:

- **Horizontal breathing room around inline text** is a content-sizing concern. A button "needs" wider than tall because Latin (and most proportional) text in a button has horizontal extent: letters cluster wider than they are tall, so a square-padded button with a 2-character label reads as cramped. That concern belongs in `min-width`: the button is square-padded around its content, and `min-width` sets the floor that makes short labels still feel clickable. The breathing comes from a sizing token, not from padding.
- **Vertical rhythm between flow children** is a between-element concern. List rows, stack children, derivation steps need consistent vertical spacing without horizontal padding doubling up against the container's inset. That concern belongs in the parent's `gap`: children carry zero (or square) padding; the parent's flex/grid `gap` orchestrates the flow.
- **Top-heavy or bottom-heavy emphasis** is a layout concern. A section header that wants tight bottom and generous top is asking for vertical breathing *above* it, not asymmetric padding *inside* it. That concern belongs in `margin-top`.

Conflate these into `padding` and every asymmetric-padding line becomes a re-litigation: which role is this, does it qualify for the exception, did the author classify it right? Separate them and the role table collapses to one column.

## The collapsed role table

| Role | Padding | Asymmetric concern lives in |
|---|---|---|
| Container | Square (`xl`–`3xl`) | — |
| Chrome | Square (`lg`–`xl`) | — |
| Inline (button, badge, pill, table cell) | Square (`sm`–`md`) | `min-width` / `min-height` for shape compensation |
| Flow child (list row, stack child) | Square or zero | Parent's `gap` for rhythm |

The role still matters — it determines which spacing token to use and whether `min-width` or `gap` is needed. What changes is that the *shape* of padding is invariant. A static check that rejects any non-1-value `padding` declaration becomes correct by construction.

## Worked example: button

```css
/* ❌ Padding doing two jobs: inset + horizontal shape */
.btn {
  padding: var(--spacing-sm) var(--spacing-md);
}

/* ✅ Padding for inset; min-width for shape */
.btn {
  padding: var(--spacing-sm);
  min-width: var(--control-min-width-md);
}
```

Short labels ("OK") still feel clickable because `min-width` enforces horizontal extent. Long labels expand the button naturally — the floor releases as soon as content exceeds it. The button looks identical to the asymmetric version in the common case and better-behaved at the extremes.

## Worked example: list row

```css
/* ❌ Padding doing two jobs: inset + flow rhythm */
.list                { padding: 0 var(--spacing-md); }
.list > .list-item   { padding: var(--spacing-sm) 0; }

/* ✅ Padding for inset; gap for rhythm */
.list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  padding: var(--spacing-md);
}
.list > .list-item {
  padding: 0;            /* or square, if the row needs its own inset */
}
```

Both container and child have square (or zero) padding. The vertical rhythm has moved from the child's `padding-top/bottom` to the container's `gap`, which *means* "space between sibling elements." Adding a new sibling type requires no rhythm decision at the child level — the parent already owns it.

## Worked example: top-heavy section header

```css
/* ❌ Three-value padding to push neighbors away */
.section-header {
  padding: var(--spacing-lg) var(--spacing-md) var(--spacing-xs);
}

/* ✅ Square inset; margin for layout rhythm */
.section-header {
  padding: var(--spacing-md);
  margin-top: var(--spacing-lg);
}
```

`margin-top` *means* "space above this element"; `padding-top` does not.

## Why this matters

When asymmetric padding is permitted "only at inline scale" or "only on flow children," every static check is gated on a judgment call. With padding restricted to inset only, the lint is mechanical: any non-1-value `padding` shorthand fails. The role classification still happens — but only to pick the *token*, not the *shape*. Three failure modes collapse:

1. **Misclassification.** "Is this clickable element a flow-child row or an inline button?" stops being load-bearing. Both get square padding; what differs is whether `min-width` or parent `gap` is involved.
2. **Compounding edits.** If a row gains horizontal padding later, the container's `gap` doesn't break; if the parent's gap changes, the row needs no counter-edit. Each property's value is independent of the others.
3. **Scanner exceptions.** A static check for asymmetric padding becomes correct by construction — no allowlist of "legitimate" asymmetric patterns to maintain.

## Costs

- **A `--control-min-width-*` token scale becomes load-bearing.** Picking sizes badly produces buttons that are always-too-wide or always-too-narrow. The scale belongs alongside the spacing tokens (DK ships `sm` / `md` / `lg` variants).
- **Flow-child rhythm requires a flex/grid parent.** Plain block flow has no `gap`; the rhythm there has to live in `margin-top` instead. Most modern layouts already use flex/grid, but legacy block stacks need conversion.
- **Existing codebases need migration.** A scanner for non-1-value `padding` shorthands (e.g. `scan-asymmetric-spacing.py`) surfaces every site to revisit. The migration is mechanical but broad.

## Relationship to `SQUARE_PADDING_DEFAULT`

`SQUARE_PADDING_DEFAULT` framed the rule as "square by default, with narrow exceptions for inline-scale controls and flow children." This principle promotes those exceptions to "padding has no asymmetric exceptions; the asymmetric concern lives elsewhere." The role classification still picks the spacing token; it no longer picks the shape of `padding`.

## Relationship to `CONTAINER_OWNS_INSET`

`CONTAINER_OWNS_INSET` separates horizontal-inset ownership (container) from vertical-flow ownership (child). With `PADDING_IS_INSET_ONLY`, both responsibilities collapse into one property each at the container level: `padding` owns the inset; `gap` owns the rhythm. The child no longer needs to express either responsibility in its own `padding`.

## Relationship to `CONTENT_DRIVES_SIZE`

`CONTENT_DRIVES_SIZE` already prescribes `min-width` as a floor (not a ceiling) so content can size its container without overflow. `PADDING_IS_INSET_ONLY` is the same move applied to inline controls: instead of `padding: sm md`, use `padding: sm` plus a `min-width` floor. Short labels get the floor; long labels expand past it; the container is never suppressed.

## Relationship to `ZERO_SIDE_PADDING_SMELL`

`ZERO_SIDE_PADDING_SMELL` flagged `padding: X 0` and `padding: 0 X` as a smell except when intentional flow-child / container-inset patterns. Under this principle both forms become smells unconditionally — the intentional flow-child case migrates to parent `gap`, and the container-inset case becomes square padding plus child-side adjustment. The smell becomes the rule.
