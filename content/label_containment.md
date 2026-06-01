---
id: LABEL_CONTAINMENT
title: "Label Containment."
essence: "If an element has a text label, its container must be wide enough to display the full label without clipping or overflow."
related: [ELASTIC_CONTENT_NEEDS_GIVE]
---

A container that shows a text label is responsible for sizing itself to contain that label fully. Truncated or clipped labels are a sizing bug, not a content problem.

Guidelines:

1. Set minimum widths from label content, not from abstract grid math
2. If a zoom level or column width cannot fit its labels, widen the column
3. Prefer slightly wider containers over ellipsis or overflow: hidden on short labels
4. For genuinely long content (descriptions, paragraphs), truncation is acceptable; for identifiers and short labels (dates, names, statuses), it is not

**Motivating example**: A gantt chart with day-level zoom at 24px column width clips date labels like "3/11" to "3/1". The fix is to widen the day column to fit the widest date label, not to truncate the date.
