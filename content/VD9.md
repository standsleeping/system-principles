---
id: VD9
title: "Reset-First Approach."
summary: "Start from a clean slate:"
---

Start from a clean slate:

```css
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
```

Then build up intentionally. Every margin, every padding should be a deliberate choice, not a browser default.