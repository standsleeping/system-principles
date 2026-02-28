---
id: LAYOUT_QUIRKS
title: "Beware Common Layout Quirks."
essence: "Mysterious layout gaps usually come from implicit CSS behaviors invisible in DevTools: baselines, 100vw, margin collapsing."
---

CSS has behaviors that cause unexpected spacing. These don't appear as margin or padding in DevTools, making them hard to diagnose. When debugging mysterious gaps, check for these quirks:

**Inline-Block Baseline Gaps**: Form elements (`textarea`, `input`, `select`) and replaced elements (`img`, `video`) default to `display: inline-block`. Inline-block elements sit on the text baseline, leaving space below for text descenders. Fix: Set `display: block` on form elements in layout contexts, or use `vertical-align: top`. Elements in flex/grid containers are blockified automatically.

**100vw Includes Scrollbar Width**: `width: 100vw` includes the scrollbar width on platforms with visible scrollbars, causing horizontal overflow. Prefer `width: 100%` or flex/grid layouts.

**Margin Collapsing**: Adjacent vertical margins collapse to the larger value. Parent and child margins also collapse if nothing separates them (no padding, border, or content). This causes unexpected spacing and elements "escaping" their containers. Fix: Use padding instead of margin, or use flex/grid (which disables margin collapsing).

**Sticky Elements Need Opaque Backgrounds**: `position: sticky` elements with `background-color: transparent` let content scroll visibly beneath them. This is easy to introduce when a component overrides a global style (e.g., a table header inherits `sticky` from a site-wide `th` rule, then a scoped style sets `background: transparent`). The result looks correct until the user scrolls. Fix: sticky and fixed elements always need an opaque background matching their context.