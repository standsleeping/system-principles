---
id: FLAT_VISUAL_HIERARCHY
title: "Flat Visual Hierarchy."
essence: "A visible container inside another visible container is a box-in-box; flatten to one surface with border separators."
related: [BOUNDARY_OWNERSHIP, SIMPLIFICATION_PATTERNS, SPACING_STRATEGY]
---

When a container (background, border, or both) appears inside another container, the user sees nested boxes. Each nesting level adds visual weight without adding information. The inner box says "I am contained"; the outer box already said that.

## The fix: flatten

Replace the inner container with border separators or whitespace within the outer container. One surface owns the background; children differentiate through borders and spacing, not through their own backgrounds.

## When nesting is appropriate

Nesting is acceptable when the inner surface has a *different semantic role* from the outer one: a code block inside a page, a tooltip over content, a modal over the page. The test: could you remove the outer container and the inner one would still make sense on its own? If yes, the nesting is structural, not decorative.

## Common violations

- A textarea with its own border inside a code block that already has a border
- A card with a background inside a panel with a background
- An input group with a border inside a form section with a border

In each case, the inner element should adopt the outer container's surface and use only a border (or nothing) to delineate itself.
