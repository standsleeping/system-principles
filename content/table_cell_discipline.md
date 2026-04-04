---
id: TABLE_CELL_DISCIPLINE
title: "Table Cell Discipline."
essence: "A table cell should serve one informational purpose; heterogeneous content in a single cell gets progressive disclosure."
tags: [tables, progressive-disclosure, information-architecture]
related: [DATA_INK_RATIO, ROW_HEIGHT_UNIFORMITY, MIXED_HEIGHT_RHYTHM]
---

A table cell should serve one informational purpose. When a cell carries heterogeneous content types (a description plus file references, a value plus a trend chart, a name plus metadata), the secondary content should be hidden behind progressive disclosure rather than displayed inline.

When a cell contains both primary and secondary content, the secondary content inflates row height unevenly, breaks scanning rhythm, and competes with primary content for attention. A summary column that shows both a description and four reference links is doing two jobs: the references serve a different moment in the user's workflow (drilling in) than the description (scanning).

**Techniques**:

1. Collapse secondary content behind a count indicator ("3 refs") that expands on click
2. Use CSS `line-clamp` to constrain primary content to a fixed number of lines with an expand affordance
3. Move secondary content to an adjacent detail panel rather than embedding it in the cell

```css
/* Clamp to 2 lines with expand affordance */
.cell-summary {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.cell-summary.expanded {
  display: block;
  -webkit-line-clamp: unset;
  overflow: visible;
}
```

**The test**: if you could remove a piece of content from a cell and the cell still serves its primary purpose, that content is a candidate for progressive disclosure.

This principle interacts with ROW_HEIGHT_UNIFORMITY: cell discipline is one of the primary tools for achieving uniform row heights. It also refines DATA_INK_RATIO: deduplication reduces redundant ink, while cell discipline separates ink that serves different purposes.
