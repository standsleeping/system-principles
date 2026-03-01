---
id: SUBSTANCE_OVER_SURFACE
title: "Substance should outweigh surface."
essence: "A well-shaped component has more substance (logic, decisions, transformations) than surface (parameters, dependencies, exports); the ratio matters, not the absolute size."
---

Absolute size is a poor guide to design quality. A 200-line function may be well-designed; a 10-line function may be poorly designed. What matters is the relationship between what a component exposes (its interface) and what it encapsulates (its implementation).

A component with a large interface relative to its body is a pass-through: it takes many inputs, does little, and returns many outputs. This shape suggests the abstraction boundary is in the wrong place. A component with a small interface relative to its body is doing real work behind a clean facade. This is the goal.

Some architectural roles are intentionally thin. Translators and integrators have low substance-to-surface ratios by design, because they exist to concentrate substance in units. Evaluate the ratio in context of the component's role.

See matklad, [Size Matters](https://matklad.github.io/2025/11/28/size-matters.html).
