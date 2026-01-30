---
id: LY2
title: "Viewport-Locked Containers."
summary: "The root layout container fills exactly the viewport and prevents page-level scrolling:"
---

The root layout container fills exactly the viewport and prevents page-level scrolling:

```css
.layout {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}
```

From this foundation, all scrolling must be explicitly delegated to content regions.