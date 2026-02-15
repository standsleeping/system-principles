---
id: STATE_DRIVEN_STYLING
title: "State as Data, Style as CSS."
essence: "JavaScript sets semantic state via data attributes. CSS maps state to visuals. The two never cross responsibilities."
---

Interactive elements often have multiple visual states: default, hover, active/selected, selected+hover, disabled, focused. When JavaScript directly toggles CSS classes to reflect these states, two problems emerge:

1. **Class conflicts.** Dynamically added classes compete with statically declared classes for specificity. In Tailwind, `bg-sky-50` added via JS may lose to `bg-white` already in the class list, depending on stylesheet order. This leads to defensive patterns like toggling both the "on" and "off" class, which is fragile and hard to read.

2. **Combinatorial explosion.** Each visual property (background, border, ring, text color) multiplied by each pseudo-state (hover, focus) means JS must juggle an ever-growing bag of class additions and removals. A single state change becomes a multi-line classList operation that's easy to get wrong.

## The principle

Separate concerns strictly:

- **JS owns semantic state.** Set a data attribute: `el.dataset.active = ""` or `delete el.dataset.active`. That's it. JS never references colors, sizes, or visual properties.
- **CSS owns visual mapping.** The template declares every visual consequence of every state, including pseudo-state combinations.

## In Tailwind

Use the `data-[attr]` variant for JS-driven states:

```html
<div class="border border-stone-300 bg-white hover:bg-stone-50
            data-[active]:border-sky-600 data-[active]:bg-sky-50
            data-[active]:hover:bg-sky-50">
```

The corresponding JS:

```js
// Activate
element.dataset.active = "";

// Deactivate
delete element.dataset.active;
```

For CSS-only states (no JS involved), use Tailwind's `peer` and `group` modifiers:

```html
<input type="checkbox" class="sr-only peer" />
<span class="bg-white peer-checked:bg-sky-600 peer-checked:text-white">
```

## When each mechanism applies

| State trigger | Mechanism | Example |
|---|---|---|
| Pure CSS pseudo-state | Native pseudo-class | `hover:`, `focus:` |
| Sibling input state | `peer` / `group` | `peer-checked:`, `group-hover:` |
| JS-driven state | `data-[attr]` | `data-[active]:`, `data-[loading]:` |

## Why this ordering matters

CSS specificity in Tailwind makes `data-[active]:bg-sky-50` beat `bg-white` because the data attribute selector adds specificity. This means the active state naturally overrides the default without needing to remove conflicting classes. The same applies to compound states: `data-[active]:hover:bg-sky-100` cleanly overrides both `hover:bg-stone-50` and `data-[active]:bg-sky-50`.

## Corollary: keep state attributes semantic

Name data attributes for what they mean, not what they look like:

- `data-active` (what the element is)
- `data-loading`
- `data-expanded`
- `data-error`

Not:

- `data-blue-border` (what it looks like)
- `data-highlighted`

This keeps the JS/CSS contract stable even if the visual design changes.
