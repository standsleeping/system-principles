---
id: DATA_INK_RATIO
title: "Data-Ink Ratio and Tabular Alignment."
summary: "When presenting repeated metrics across items, optimize for scanability by reducing redundant labels and aligning values vertically."
---

When presenting repeated metrics across items, optimize for scanability by reducing redundant labels and aligning values vertically.

Edward Tufte's data-ink ratio: maximize information, minimize redundant visual elements. When the same labels repeat on every row, move them to a single header:

```
Instead of:
  Customer       9 fields · 3 consumers · 2 producers
  DeliveryInfo   6 fields · 1 producer

Prefer:
                      F   C   P
  Customer            9   3   2
  DeliveryInfo        6   —   1
```

Guidelines:

1. Deduplicate labels: If a label appears on every row, move it to a header
2. Align numbers vertically: Use CSS grid or fixed-width columns
3. Use tabular numerals: `font-variant-numeric: tabular-nums` for consistent digit widths
4. Use dashes for zeros: `—` is clearer than `0` for "none" or "not applicable"
5. Keep headers minimal: Single letters or short abbreviations with tooltips for full names
6. Right-align numbers: Numbers align on the ones digit for easy comparison

Appropriate when showing 5+ items with the same metric structure where numbers are primary information users need to compare.

**Implementation**:

```css
.metric-grid {
  display: grid;
  grid-template-columns: 1fr repeat(3, 3ch);  /* name + 3 metric columns */
  gap: var(--spacing-xs);
}

.metric-value {
  font-variant-numeric: tabular-nums;
  text-align: right;
}

.metric-empty {
  color: var(--gray-300);
}
```

```html
<!-- Section header with column labels -->
<div class="section-header metric-grid">
  <span>DATA</span>
  <span class="metric-label" title="Fields">F</span>
  <span class="metric-label" title="Consumers">C</span>
  <span class="metric-label" title="Producers">P</span>
</div>

<!-- Data rows -->
<div class="entity-row metric-grid">
  <span>Customer</span>
  <span class="metric-value">9</span>
  <span class="metric-value">3</span>
  <span class="metric-value">2</span>
</div>
```

**Responsive Considerations**: At narrow widths, the tabular layout may need to degrade:

| Width | Strategy |
|-------|----------|
| **Wide** | Full grid with aligned columns |
| **Medium** | Inline format with separators: `9 · 3 · 2` |
| **Narrow** | Abbreviated: `9f 3c 2p` or hide secondary metrics |

The inline format loses alignment benefits but remains compact.