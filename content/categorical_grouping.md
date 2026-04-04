---
id: CATEGORICAL_GROUPING
title: "Categorical Grouping."
essence: "When a column contains few distinct values that partition rows, replace it with section headers to reclaim horizontal space and strengthen visual landmarks."
tags: [tables, columns, information-architecture]
related: [DATA_INK_RATIO, ONE_SIGNAL_PER_MEANING]
---

When a table column contains few distinct values that naturally partition rows into groups, replace the column with section headers. This reclaims horizontal space and provides stronger visual landmarks than a repeated text label.

**Signals that a column should become a group header**:

- Fewer than ~5 distinct values
- Values naturally order the rows (priority levels, status stages, categories)
- The same value repeats for many consecutive rows
- The column adds no new information when a filter is active (e.g., a "Priority" column when the user has already filtered to "NOW")

**The group header pattern**: a lightweight row spanning all columns that labels the section. It uses smaller, muted text with a count indicator. Combined with a filter toggle, the column is eliminated entirely while strengthening visual orientation in the unfiltered view.

```html
<tr class="group-header">
  <td colspan="3">NOW (16)</td>
</tr>
```

```css
.group-header td {
  font-family: var(--typography-mono);
  font-size: var(--font-size-xs);
  text-transform: uppercase;
  letter-spacing: var(--font-letter-spacing-wide);
  color: var(--color-text-muted);
  border-bottom-color: var(--color-gray-400);
}
```

**Consecutive deduplication**: within a group, if consecutive rows share a value in another column (e.g., the same project name), show it only on the first row. This reduces visual repetition and makes group boundaries visible within sections.

This is a specific instance of DATA_INK_RATIO's "deduplicate labels" guideline, applied structurally rather than typographically. It also follows ONE_SIGNAL_PER_MEANING: the toggle and the group header communicate priority; a column repeating the same word on every row is a redundant signal.
