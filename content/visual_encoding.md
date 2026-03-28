---
id: VISUAL_ENCODING
title: "Visual Encoding vs. Text."
essence: "Text for precision, visual for shape; supplement, don't duplicate."
related: [DATA_INK_RATIO, ONE_SIGNAL_PER_MEANING, SIMPLIFICATION_PATTERNS]
---

Text and visual encoding serve different cognitive purposes. Text delivers precise values; visual encoding (sparklines, bars, area fills, color scales) communicates shape, trend, and relative magnitude at a glance.

**When to use each:**

| Channel | Strength | Example |
|---------|----------|---------|
| Text    | Precision, exact comparison | "14,203" or "2026-03-01" |
| Visual  | Trend, distribution, relative scale | Sparkline showing 50 recent values |

**Guidelines:**

1. Don't replace text with a chart when the reader needs exact values
2. Don't add a chart that restates what the adjacent number already says; show a different dimension (trend, distribution, trajectory)
3. Pair channels when both are useful: exact value in a column, trend shape in an adjacent sparkline
4. A visualization earns its space by communicating something text cannot: the shape of change over time, the skew of a distribution, relative position within a range

**Anti-patterns:**

- A bar chart next to a number that encodes the same single value (redundant signal)
- Replacing a readable number with a gauge or dial (lost precision, no gain)
- Adding a chart "because the data exists" rather than because the shape tells the reader something they need
