---
id: UT3
title: "Ancestry Tracing."
summary: "When an element causes overflow, trace up the DOM to find where the problem originates:"
---

When an element causes overflow, trace up the DOM to find where the problem originates:

```
body: 1200x900 (r:1200, b:900)
  main: 1200x900 (r:1200, b:900)
    section: 1200x850 (r:1200, b:850)
      div: 1250x400 (r:1250, b:400) [!RIGHT]  ← overflow starts here
```

The trace shows dimensions and flags where overflow begins, making it clear which ancestor to fix.