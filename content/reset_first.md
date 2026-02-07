---
id: RESET_FIRST
title: "Reset-First Approach."
essence: "Strip all browser defaults; every margin and padding should be a deliberate choice."
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