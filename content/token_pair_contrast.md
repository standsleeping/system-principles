---
id: TOKEN_PAIR_CONTRAST
title: "Tokens carry pairwise contracts."
essence: "A semantic token's real contract is the adjacency it must survive, not the value it resolves to; two tokens that appear next to each other must stay distinguishable in every theme."
tags: [color, tokens, themes]
related: [TOKEN_DRIVEN_DESIGN, ADJACENT_SHADE_SEPARATION, COLOR_USAGE]
---

A semantic token is not defined by its resolved color; it is defined by what it must remain visible against. `--color-border` whose job is "separator on page background" has one contract: be distinguishable from `--color-bg` in every theme. If the same token is reused for a different adjacency (a hover outline stacked on `--color-hover-bg`), it is being asked to honor a contract it was never designed for, and in some themes the values will collide.

## The failure mode

A polymorphic token works silently in most contexts because the palette tends to space values evenly. The collision surfaces only when two tokens happen to resolve to the same primitive in one theme: `--color-border` and `--color-hover-bg` both collapse to gray-600 in a dark theme, and a row outline drawn in `--color-border` on a hover-filled row becomes invisible. Light mode is fine because the pair is two stops apart there; dark mode hides the bug.

## The fix

Give each distinct adjacency its own semantic token. A border that separates a hover state from its surroundings is not the same role as a border that separates rows; naming them together is a shortcut that silently assumes their contrast requirements match. They do not.

```css
/* Polymorphic: honors one contract (vs page-bg), silently fails others */
--color-border: light-dark(gray-200, gray-600);

/* Purpose-specific: contract is "visible against hover-bg in every theme" */
--color-hover-outline: light-dark(gray-400, gray-500);
```

## Verifying the contract

The rule "tokens that appear adjacent must stay distinguishable in every theme" is a build-time check, not a runtime hope. Enumerate the pairs the design system composes (background × border, hover-bg × outline, code-bg × text, selected-bg × foreground) and assert a minimum contrast ratio for each pair across every defined theme. A small script catches the whole class of regressions that `ADJACENT_SHADE_SEPARATION` describes one instance of.

## Relation to other principles

1. `TOKEN_DRIVEN_DESIGN` says use tokens as the single source of truth. This principle says tokens are *contracts*, not just shared values, and their contracts must be honored across themes.
2. `ADJACENT_SHADE_SEPARATION` is the component-level statement of the rule: draw a border where two shades meet. This principle lifts the same rule to the palette: any token pair that will meet must stay distinguishable.
3. `COLOR_USAGE` reserves color for meaning; the meaning is expressed through contrast, and contrast is only meaningful if it survives theme switches.
