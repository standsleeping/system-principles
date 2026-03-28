---
id: SUBORDINATE_VISUALIZATION
title: "Subordinate Inline Visualization."
essence: "Inline visualizations annotate; they recede into the row, not headline it."
related: [VISUAL_ENCODING, COLOR_USAGE, SIMPLIFICATION_PATTERNS]
---

When a visualization appears inline (inside a table row, beside a label, within a list item), it is subordinate to the surrounding content. It annotates; it does not headline.

**Rules for inline visualizations:**

1. **Neutral palette.** Use grays for fill and stroke. Reserve semantic colors (green, red, purple) for status and interaction; the visualization should not compete with those signals
2. **Compact size.** Keep dimensions proportional to the text line height or row height. A sparkline in a table row should feel like a column value, not a hero element
3. **No interaction.** Inline visualizations are read-only glyphs. Hover effects, tooltips, and click targets belong to standalone charts, not inline annotations
4. **No chrome.** Omit axes, gridlines, legends, and labels. The surrounding content provides the context; the visualization provides only the shape

**Test:** if removing the visualization degrades the row's information but does not break it, the visualization is correctly subordinate. If the row becomes unintelligible without the visualization, it has taken on too much responsibility.

**Implementation note:** SVG with `viewBox` and CSS custom properties for colors keeps inline visualizations consistent with the surrounding design tokens without introducing a separate color system.
