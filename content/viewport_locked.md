---
id: VIEWPORT_LOCKED
title: "Viewport-Locked Containers."
essence: "Lock the root to the viewport; from there, all scrolling must be explicitly delegated to content regions."
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