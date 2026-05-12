---
id: STATE_BELONGS_TO_INTERACTIVE
title: "State belongs to the interactive element."
essence: "Visual state — hover, focus, active/selected, disabled — lives on the focusable element, not on a structural wrapper. The CSS target then matches the ARIA target and the focus model, so indicators stay aligned without :focus-within plumbing."
related: [FOCUS_STATES, INSET_FOCUS_RING, HONEST_AFFORDANCES]
---

When a list item or row contains an interactive child (`<a>`, `<button>`, an element with `tabindex`), it is tempting to put visual state on the structural wrapper because the wrapper is the larger box and the state visually applies to the whole row. Don't. The browser, the accessibility tree, and CSS itself all agree that the focusable element is the thing that owns its state.

## Why co-location is forced by the platform

Three independent systems target the same element when state changes:

1. **Focus model.** `:focus-visible`, `:focus`, `:active` only fire on the element that takes focus. The wrapper never receives focus directly, so its state pseudo-classes never fire — surfacing the wrapper's "focused" appearance requires `:focus-within`, which is a workaround, not a primary affordance.

2. **ARIA states.** `aria-current="page"` (active nav link), `aria-selected="true"` (listbox option), `aria-pressed` (toggle button), `aria-checked` (custom checkbox), `aria-expanded` (disclosure trigger) — all belong on the focusable element that represents the action, not on its container. Screen readers announce state from the element they're focused on.

3. **Pointer state.** `:hover`, `:active`, and the disabled state (`[disabled]`, `:disabled`) all key off the interactive element. Hover styling on the wrapper requires the cursor to enter the wrapper's box, which may be larger than the focusable child and produce a hover signal that doesn't match the actual click target.

If the visual indication and the ARIA state target the same element, all three systems stay in sync automatically. If they don't, every state change costs a `:focus-within` selector, an `aria-` attribute on the wrong node, or a disagreement between the visible affordance and the click target.

## The symptom: misaligned indicators

The most common failure mode is an active indicator on the wrapper plus a focus ring on the child:

```css
/* Drifted: active and focus on different boxes */
.list-item {
  border-left: 2px solid transparent;
}
.list-item-active {
  border-left-color: var(--color-link); /* on wrapper */
}
.list-item-link:focus-visible {
  outline: 2px solid var(--color-focus-ring); /* on child */
  outline-offset: -2px;
}
```

When an item is both active and focused, the active bar (on the wrapper's edge) and the focus ring (inside the child's box) sit at different x-coordinates. Any horizontal padding between the wrapper edge and the child box becomes a visible gap on the left of the ring — the ring's top and bottom segments don't reach the active bar.

## The fix: promote state down to the focusable element

```css
/* Aligned: active and focus on the same box */
.list-item-link {
  display: block;
  padding: var(--spacing-sm) var(--spacing-md);
  border-left: 2px solid transparent;
}
.list-item-active .list-item-link {
  border-left-color: var(--color-link);
}
.list-item-link:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: -2px;
}
```

The `<li>` becomes a pure semantic shell with no padding, no border, no fill. Anything that previously lived on the wrapper for visual reasons (level indents, hover fills, selected backgrounds, disabled opacity) moves into the focusable element. The wrapper still announces "list item N of M" to assistive tech; that is its only job.

If the wrapper carries decorations that genuinely sit outside the focusable element (a numeric prefix, a count badge in a separate column), bring them inside the focusable element so the click target and the visible affordance match. This often improves the design as a side effect: it forces the question of whether those decorations were ever really clickable, and removes the ambiguity if they weren't.

## When the rule does not apply

Composite widgets with multiple interactive children in a single row — a data-grid row with separate action buttons, a card with both a primary link and an inline menu — operate under the composite-widget pattern (roving `tabindex`, `aria-activedescendant`). In those cases neither child fully represents the row, and the row itself may legitimately carry the selection state because selection is a row-level concept distinct from any individual button's state. The principle still applies internally: each interactive child owns its own focus and hover; the row's selection styling is a separate, row-level concern.
