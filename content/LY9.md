---
id: LY9
title: "Beware Common Layout Quirks."
summary: "CSS has behaviors that cause unexpected spacing. These don't appear as margin or padding in DevTools, making them hard to diagnose. When debugging mysterious gaps, check for these quirks:"
---

CSS has behaviors that cause unexpected spacing. These don't appear as margin or padding in DevTools, making them hard to diagnose. When debugging mysterious gaps, check for these quirks:

**Inline-Block Baseline Gaps**: Form elements (`textarea`, `input`, `select`) and replaced elements (`img`, `video`) default to `display: inline-block`. Inline-block elements sit on the text baseline, leaving space below for text descenders. Fix: Set `display: block` on form elements in layout contexts, or use `vertical-align: top`. Elements in flex/grid containers are blockified automatically.

**100vw Includes Scrollbar Width**: `width: 100vw` includes the scrollbar width on platforms with visible scrollbars, causing horizontal overflow. Prefer `width: 100%` or flex/grid layouts.

**Margin Collapsing**: Adjacent vertical margins collapse to the larger value. Parent and child margins also collapse if nothing separates them (no padding, border, or content). This causes unexpected spacing and elements "escaping" their containers. Fix: Use padding instead of margin, or use flex/grid (which disables margin collapsing).