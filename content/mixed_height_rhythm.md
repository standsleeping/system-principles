---
id: MIXED_HEIGHT_RHYTHM
title: "Mixed-height content needs more vertical rhythm."
essence: "When inline elements are taller than the text baseline (math, code, badges), increase line-height and gap by one tier."
---

Prose with inline math notation, code spans, chemical formulas, or other elements taller than the text baseline compresses the visual rhythm. The mismatch between text height and expression height makes lines feel cramped even when the line-height is generous for plain text.

When content mixes text with taller inline elements:

1. Increase `line-height` by one tier (e.g., 1.5 → 1.6)
2. Increase vertical `gap` between items by one tier (e.g., 8px → 12px)
3. The adjustment applies to any container where mixed-height content appears: prose paragraphs, proof steps, list items, table cells

The tier increase is relative to what works for plain text in the same context. If plain text reads well at 1.5 line-height, mixed content needs 1.6. If list items need 8px gap for text-only steps, math-heavy steps need 12px.

This compounds with density: the more inline expressions per line, the more the rhythm compresses. A line with three MathML expressions needs more vertical breathing room than a line with one.
