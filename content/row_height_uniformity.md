---
id: ROW_HEIGHT_UNIFORMITY
title: "Row Height Uniformity."
essence: "Uniform row heights preserve the scanning grid that makes tables superior to other layouts; constrain content rather than letting rows expand freely."
tags: [tables, scanning, alignment]
related: [TABLE_CELL_DISCIPLINE, MIXED_HEIGHT_RHYTHM, DATA_INK_RATIO]
---

Uniform row heights preserve the scanning grid that makes tables superior to other layouts. When row heights vary dramatically (one row is 1 line, another is 7), the grid breaks down and cross-row comparison becomes impossible.

Tables derive their scanning advantage from grid alignment. When a reader's eye moves horizontally across a row, uniform heights let them track the row reliably. Variable heights force the eye to hunt for the correct cell, especially in wide tables where the first column is far from the last.

**Techniques**:

1. Constrain cell content with CSS `line-clamp` (2-3 lines max)
2. Provide an expand affordance for content that exceeds the clamp
3. Move variable-length content to progressive disclosure (TABLE_CELL_DISCIPLINE)
4. Use `line-height` and `padding` from the spacing scale to establish a predictable row rhythm

```css
.cell-summary {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

**Relationship to MIXED_HEIGHT_RHYTHM**: that principle adjusts spacing to accommodate height variation (increasing `line-height` by one tier when inline elements are taller than text). This principle prevents the variation in the first place. Prefer prevention over accommodation when the table's scanning function is primary.

**When to relax**: content tables embedded in prose (2-3 columns of reading material) may tolerate height variation because the reader is not scanning across rows. Data tables with many rows where cross-row comparison matters should enforce uniformity.
