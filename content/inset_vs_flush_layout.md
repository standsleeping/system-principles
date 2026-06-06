---
id: INSET_VS_FLUSH_LAYOUT
title: "Inset vs Flush Layout."
essence: "Chrome is always flush against the viewport. The layout mode is the choice of what happens inside: an inset layout floats content surfaces in a gutter; a flush layout runs them edge-to-edge against the chrome's interior."
related: [VIEWPORT_LOCKED, BOUNDARY_OWNERSHIP, FIXED_FLEXIBLE_REGIONS, LAYOUT_VARIANTS, SCROLL_CONTAINMENT, PADDING_IS_INSET_ONLY]
---

A viewport-locked shell forces chrome (header, footer, sidebars) to occupy every edge of the window. Chrome is flush by structural necessity — it owns the boundary against the viewport. What varies between layouts is the mode of the *content region* the chrome surrounds.

## The two modes

| Mode | Content region | Sibling surfaces | Boundary between |
|---|---|---|---|
| **Inset layout** | Recessed field with a gutter on all sides | Float; each owns four borders | Negative space (the gutter) |
| **Flush layout** | Edge-to-edge with chrome | Stack flush | A full-bleed rule |

In an inset layout, content surfaces are *cards*: each owns its four borders, sits on a recessed field background that makes the gutter visible against the chrome, and is separated from neighbours by negative space. The chrome's interior edge is the boundary between two different surface kinds — chrome (flush) and field (inset) — and the gutter starts immediately inside.

In a flush layout, content surfaces are *items* in a list: they touch the chrome's interior edge with no gutter, and they touch each other separated by a single full-bleed rule. The chrome's interior edge is continuous with the content's exterior edge; the only boundary inside is the rule between items.

## Why the dichotomy is structural

Inset/flush first appeared as a card-level pattern (Apple's `insetGrouped` vs `plain`). But the same asymmetry-of-ownership operates at every nested level — the layout shell, the regions inside the chrome, the surfaces inside those regions, the items inside those surfaces. Each level independently picks inset or flush, and the choice cascades:

- **Background tokens.** An inset content region needs a recessed background that makes the gutter visible against the chrome. A flush content region shares the chrome's background and relies on the rule to mark transitions.
- **Scrollbar treatment.** Both modes use the native bar (see `NATIVE_SCROLLBAR`); neither hides, tints, nor reserves a gutter for it. On overlay-scrollbar platforms the bar floats and neither mode pays a cost; on classic platforms the bar takes its width at the container's inline-end edge, the accepted platform cost in both modes.
- **Selected-item indicators.** Inset cards indicate active state with a border-color shift on all four sides plus a fill. Flush items indicate active state with a single-side border (left for vertical lists, bottom for horizontal) plus a full-bleed fill.
- **Padding role.** Inset cards are *containers* (square padding, larger token range). Flush items are *flow children* (square or zero padding; rhythm via the parent's `gap`).

Mixing modes within a level is the most common drift: a flush-mode list that draws four borders around each row leaks card vocabulary into an item context; an inset-mode card whose edge touches the field's interior breaks the gutter that defines the mode.

## Picking a mode

The mode is a property of the application shell, set at the layout level. Compatible signals:

- **Inset suits** settings panels, dashboards with discrete metric surfaces, group-listed content (Apple's `Settings.app`).
- **Flush suits** navigation-heavy shells, scrollable content lists where rules-of-separation carry hierarchy (mail apps, IDE file trees, terminal-style tools).

A single application can compose both — an inset layout in one pane, a flush layout in another — but the boundary between them must be the chrome itself, not an arbitrary inner element. Two modes meeting inside the same content region is the drift signal.

## Relationship to other principles

- `VIEWPORT_LOCKED` provides the foundation: chrome is flush because the viewport is the boundary.
- `BOUNDARY_OWNERSHIP` extends downward: in an inset layout, each card owns four boundaries; in a flush layout, the chrome and the rules own the boundaries.
- `FIXED_FLEXIBLE_REGIONS` describes how chrome claims its space; this principle describes what happens *inside* the flexible region.
- `SCROLL_CONTAINMENT` defines where scroll is allowed; `NATIVE_SCROLLBAR` defines how those containers express it. This principle is independent of both — it governs the chrome/content boundary.
- `PADDING_IS_INSET_ONLY` becomes mode-dependent: in inset layouts, each card carries square container padding plus the field's gutter; in flush layouts, items carry square (or zero) padding while the chrome (and the container row above the item) carries the inset.
