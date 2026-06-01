---
id: FLAT_CLASSED_FLEX_TREE
title: "Flat, Classed, Flex-Driven Element Tree."
essence: "Inspecting any element reveals a shallow DOM where every element has a class and styling is driven by flexbox (or grid). No deep wrapper chains, no unnamed elements, no positioning tricks substituting for flow distribution."
related: [NEVER_CALC_LAYOUT, TESTABLE_MARKUP, BOUNDARY_OWNERSHIP, ANCESTRY_TRACING, REDUCE_INTERLEAVING, LAYERED_UI_REVEAL]
---

A UI tree's quality is legible at inspection time. Open devtools, click any element, look at the ancestor chain: every element is named (has a class), the chain is short (≤ ~6 levels for most leaf content), and the layout is flex- or grid-driven (the Styles tab shows `display: flex` or `display: grid` near the top, not a thicket of positioning, margins, and floats).

This principle states the inspection contract:

1. **Every element has a class.** A bare `<div>` or `<section>` without a class is a smell. The class name is the element's structural role.
2. **The tree is flat.** Most leaf content is reachable within four to six levels from the root. Deep wrapper chains (ten or more levels) signal nested abstractions that should be flattened.
3. **Layout is flex- or grid-driven.** Children's positions come from the parent's flex/grid distribution, not from positioning offsets, margins, or floats. The only exception: `position: fixed` for overlays and `position: sticky` for chrome that survives scroll.

## Why the contract matters

When all three properties hold, debugging is fast. An element's appearance is a function of its class (visible in devtools' Elements panel) and its parent's flex/grid declaration (visible one level up). Drilling further is rarely needed.

When any property fails:

- **Unnamed elements.** A bare `<div>` provides no structural signal. Every reader of every PR re-derives its role from context.
- **Deep trees.** A twelve-level chain to reach a button means a dozen abstractions wrap it. Each is a place where a style could leak, an event could be intercepted, a className could be doubled.
- **Non-flex layout.** Absolute positioning, margins, and floats decouple an element's position from its DOM parent. The reader can't predict where the element will land by inspecting the markup.

## What this rules out

- **Mystery wrappers.** A `<div>` whose only role is to carry a className for a selector should be the named element itself, not a wrapper.
- **Positioning for flow.** Using `position: absolute` to lay out a row of items is a smell — flex does it without offsets.
- **Margin for distribution.** Enforced separately by `NEVER_MARGIN`: rhythm lives in the parent's `gap`, not in children's margins.
- **Nested abstraction layers.** Most layouts use one display mode per container. Two levels of nested grid is acceptable when the grid is non-trivial; three is a refactor signal.

## What this allows

- **Component composition.** A component renders a small tree of named elements with flex/grid distribution. Components compose by becoming children of each other's trees; depth grows linearly with composition, not exponentially.
- **Shallow utility wrappers.** A `<dk-icon>` wrapping an `<svg>` is fine — the wrapper carries one role (icon sizing and color flow). Multi-role wrappers are not.
- **Skipping levels via grid templates.** A grid container with `grid-template-areas` can place children at named positions without intermediate wrappers — the grid declaration carries the structural information.

## Diagnostic

For any shipped page, open devtools on a representative content element (a row, a card, a button). Walk the ancestor breadcrumb:

1. Count levels from `<body>` to the element. If greater than eight for a typical content child, flag for review.
2. Check each level has a class. Bare elements get flagged.
3. Click each level and check the Computed tab for `display`. Expect mostly `flex` or `grid`, with leaf elements `inline` or `block`. Frequent `position: absolute` or `display: table` is a smell.

A linter pass complements the diagnostic: any element with no `class` attribute in a shipped HTML page (excluding `<html>`, `<head>`, `<body>`, `<script>`, `<style>`, `<link>`, `<meta>`, `<title>`) is flagged.

## Relationship to other principles

- `NEVER_CALC_LAYOUT` is a corollary: flex/grid distributes space; explicit calculations are unnecessary.
- `TESTABLE_MARKUP` says every meaningful element should be addressable. Classes-everywhere is one expression of that.
- `BOUNDARY_OWNERSHIP` and `INSET_VS_FLUSH_LAYOUT` work because each layer of the tree owns one role; the flat-classed structure makes ownership inspectable.
- `LAYERED_UI_REVEAL` becomes mechanical: layer membership is one class match away because every element has a class.
- `ANCESTRY_TRACING` is the diagnostic principle for navigating the tree; flat-classed makes the trace short.
- `REDUCE_INTERLEAVING` is the broader principle this specializes: each element does one job, named at the class level.
