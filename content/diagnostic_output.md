---
id: DIAGNOSTIC_OUTPUT
title: "Diagnostic Output."
summary: "When constraints are violated, provide actionable diagnostics:"
---

When constraints are violated, provide actionable diagnostics:

```
[FAIL] Page scrolls (vertical: +47px)
Viewport: 1920x1080
Document: 1920x1127

Overflowing elements (3):
  main.content:
    - Extends 47px past bottom edge
  div#sidebar:
    - Content 23px taller than container
  section.hero:
    - Extends 12px past right edge
```

Include the violation type and amount, viewport vs document comparison, list of contributing elements, and specific issue for each element.