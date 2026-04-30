---
id: ADJACENT_BAR_BASELINE
title: "Adjacent Bars Share a Baseline."
essence: "When two chrome bars in adjacent panes form a continuous horizontal rule, pin them to a shared height contract — content-driven sizing alone fractures the line."
tags: [layout, chrome, alignment]
related: [CONTENT_DRIVES_SIZE, ROW_HEIGHT_UNIFORMITY, CONTAINER_OWNS_INSET, BOUNDARY_OWNERSHIP]
---

A single horizontal rule that crosses a pane boundary is a structural promise: "everything above this is chrome, everything below is content." When the bars on each side of the boundary are sized independently by their own content, that promise breaks. The line fractures at the seam, and the page suddenly reads as two unrelated regions stacked next to each other rather than one orientable surface.

This is a different problem from `CONTENT_DRIVES_SIZE`. CDS governs *one* container: don't let a decorative child override what content needs. This principle governs *two* sibling containers on a shared horizontal axis: their content heights will diverge, so they need an explicit shared height — usually a CSS variable consumed by both — to keep the rule continuous.

**The Problem: Independent Content Sizing**

A typical workspace shell has two chrome bars at the top: a sidebar header (containing a workspace label) and a main-pane title bar (containing a panel-toggle icon and a title). Each bar's height comes from its own content plus padding.

```css
.sidebar-header {
  padding: var(--spacing-md);
  /* renders ~34px tall: 18px text line-box + 16px padding */
}

.pane-bar {
  padding: var(--spacing-md);
  /* renders ~40px tall: 24px icon-button + 16px padding */
}
```

Both bars draw a `border-bottom`. The text-driven bar lands at y=34, the icon-driven bar lands at y=40, and the horizontal rule has a 6px step at the pane boundary. The eye reads it as misalignment, not as a feature.

Pinning the bars to a `min-height` of the larger content's height *almost* works, but sub-pixel content (an inline glyph's line-box, a child with a fractional rem height) can push past the floor and reintroduce the gap. Use `height` rather than `min-height` when the goal is exact equality.

**The Fix: A Shared Height Contract**

Define one height variable. Have every chrome bar that participates in the same horizontal rule consume it.

```css
:root {
  --chrome-bar-h: 2.5rem;
}

.sidebar-header,
.pane-bar {
  height: var(--chrome-bar-h);
  box-sizing: border-box;
  padding: var(--spacing-md);
}
```

Now the two bars are identically sized regardless of what they contain. A consumer that needs a taller chrome (touch app, denser dashboard) overrides `--chrome-bar-h` once at the shell level and every participating bar follows. The rule stays continuous as content evolves.

**Generalizations**

The principle applies to any two containers whose visible borders form a continuous structural line:

| Boundary | Bars on each side |
|---|---|
| Top of a workspace shell | Sidebar header + main-pane title bar |
| Bottom of a split-pane editor | Status bar pieces in each pane |
| Header row of side-by-side tables | Column-header rows |
| Footer of a card grid | Per-card metadata strips |

The rule is the same: the shared border is *evidence* of a shared height contract, and you have to make that contract explicit.

**Anti-patterns**

| Don't | Do |
|---|---|
| `min-height` with sub-pixel inline content | `height` with `box-sizing: border-box` |
| Hardcode the bar height in each component's CSS | Read a shared CSS variable so a host can override |
| Asymmetric padding on chrome bars (`padding: md lg`) | Square padding from the chrome scale (see CDS / DK visual-language) |
| Hide the bottom border on one side to "fix" the visual fracture | Match heights; the border belongs on every bar |

**Relationship to CONTENT_DRIVES_SIZE**

CDS says: a container's height comes from its content children, not from decoration. That's right for one container. When two containers must visually agree, content alone can't decide — they need a shared external floor. The two principles compose: each bar is content-sized internally (CDS), but a shared `height` token sets the cross-container baseline (this principle).
