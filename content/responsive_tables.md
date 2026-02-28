---
id: RESPONSIVE_TABLES
title: "Responsive Table Strategies."
essence: "Tables degrade by restructuring, not by hiding. Choose between horizontal scroll and stacked cards based on whether cross-row comparison matters."
---

Tables don't fit the standard component degradation model (wrap → hide → abbreviate → truncate). Their row-column structure requires restructuring on narrow viewports.

**Two Patterns**:

| Pattern | Use When | Trade-off |
|---------|----------|-----------|
| **Horizontal scroll** | Cross-row comparison is essential (spreadsheets, matrices) | Preserves column alignment; hides content off-screen |
| **Stacked cards** | Each row is a self-contained item (feature lists, config tables) | Shows all data at once; loses column alignment |

**Stacked Cards Implementation**: Hide the thead, set rows and cells to `display: block`, and use `data-label` attributes with `::before` pseudo-elements to re-label each value.

```css
@media (max-width: 768px) {
  table thead { display: none; }
  table, tbody, tr, td { display: block; }
  td[data-label]::before {
    content: attr(data-label);
  }
}
```

Use `display: flex; justify-content: space-between` on labeled cells to align labels left and values right.

**Uniform Cell Styling**: When table values share a visual type (paths, code, config), style the cells uniformly via CSS rather than marking individual tokens inline. Scattered inline styling creates visual dissonance; uniform styling reads as a cohesive column.
