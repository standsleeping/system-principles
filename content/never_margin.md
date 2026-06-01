---
id: NEVER_MARGIN
title: "Never Margin."
essence: "`margin` does not appear in production CSS. Inter-element rhythm lives in the parent's `gap`; explicit gaps between unrelated regions live in a structural sibling spacer; centering lives in `place-items` or grid alignment."
related: [PADDING_IS_INSET_ONLY, SQUARE_PADDING_DEFAULT, CONTAINER_OWNS_INSET, SPACING_STRATEGY, ZERO_SIDE_PADDING_SMELL]
---

Every spacing concern in the UI has a single owner. `padding` owns the inset between a box and its content; `gap` owns the rhythm between siblings; a structural spacer owns explicit gaps between unrelated regions. `margin` is gone.

The earlier principles (`PADDING_IS_INSET_ONLY`, `SQUARE_PADDING_DEFAULT`) routed one residual concern — top-heavy or bottom-heavy emphasis — into `margin-top`. This principle removes that escape hatch.

## Why margin goes

Margin's defining feature is that it lives outside the element's box. That places it in an awkward middle: it isn't owned by the element (the box ends at the border), and it isn't owned by the parent (which already has `padding` and `gap`). The same vertical gap between two siblings can be expressed three ways — `margin-bottom` on the upper, `margin-top` on the lower, `gap` on the parent — with no canonical answer. Three call sites for one concern.

Margin's other defining feature, *collapsing margins*, makes the rendered gap a function of both siblings' margins (the larger wins, sometimes), not the sum. A spacing system whose rendered gaps don't match its source declarations isn't a system.

Banning margin collapses three failure modes:

1. **Ambiguous ownership.** A gap has one owner: the parent's `gap`. No re-litigation per call site.
2. **Collapsing surprises.** Flex/grid `gap` does not collapse. Declared value equals rendered value.
3. **Audit reachability.** A static check rejecting any `margin:` declaration is mechanical; no exception list.

## Where the old margin uses go

| Old use | New destination |
|---|---|
| `margin-top` on a section header for emphasis | Parent uses `display: flex; flex-direction: column; gap: var(--spacing-lg);`. The header is a flow child with only its inset. |
| `margin-bottom` between two stacked unrelated regions | Lift to a shared parent's `gap`. If no parent exists, introduce one. |
| `margin: auto` for centering | `display: grid; place-items: center;` on the parent. |
| `margin-block-start` / `margin-block-end` on prose | The prose container uses `gap`; paragraphs carry no spacing. |
| `margin: 0 auto` on a max-width content column | `display: grid; grid-template-columns: minmax(0, var(--content-max-width)); justify-content: center;` on the parent. |
| Negative margin for overflow tricks | CSS Grid with `grid-column: 1 / -1;`, or restructure so the full-bleed element isn't a descendant of the constrained one. |

When the natural answer is "the gap belongs to a parent that doesn't exist yet," introduce the parent. One wrapper for one named owner is a fair trade.

## Worked example: top-heavy section header

```css
/* ❌ Old: margin-top for emphasis */
.section-header {
  padding: var(--spacing-md);
  margin-top: var(--spacing-lg);
}

/* ✅ New: parent owns rhythm */
.section-stack {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}
.section-header {
  padding: var(--spacing-md);
}
```

When the gap above a particular header needs to differ from the default rhythm, insert a structural spacer:

```html
<div class="section-stack">
  <section class="content">…</section>
  <div class="spacer" aria-hidden="true"></div>
  <section class="section-header">Next section</section>
</div>
```

```css
.spacer { height: var(--spacing-2xl); }
```

The spacer is a DOM-visible artifact. Its size, role, and presence are inspectable. Margin was invisible.

## The audit

The `padding` CLI audit (`prinz/padding_audit.py`) gains a `--ban-margin` strict mode that flags every `margin` / `margin-*` declaration regardless of asymmetry. Migration is mechanical: each finding lifts to a parent `gap` or a structural spacer.

## Costs

- **One new DOM element occasionally.** Lifting rhythm to a parent's `gap` sometimes requires a wrapper. The wrapper carries one class and one role.
- **`place-items: center` instead of `margin: auto`.** Centered modals and content columns gain one container declaration; the container's role becomes explicit.
- **Migration breadth.** Existing codebases have margin spread thinly. The `--ban-margin` audit produces a long initial list.

## Relationship to other principles

- `PADDING_IS_INSET_ONLY`: the third concern (top-heavy/bottom-heavy emphasis) now routes to parent `gap` or a structural spacer, not `margin-top`.
- `SQUARE_PADDING_DEFAULT`'s "Margin handles what padding can't" section is replaced with the gap+spacer pattern.
- `CONTAINER_OWNS_INSET` is unchanged in spirit: padding owns inset, gap owns rhythm. This principle removes the residual margin role.
- `SPACING_STRATEGY` decomposes into `padding` and `gap`. Margin is no longer in the decomposition.
