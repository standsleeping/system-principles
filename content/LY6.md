---
id: LY6
title: "Empty State Collapse."
summary: "Empty structural elements should automatically hide:"
---

Empty structural elements should automatically hide:

```css
.layout-header:empty,
.layout-footer:empty,
.layout-sidebar-header:empty {
  display: none;
}
```

This allows optional slots to be omitted without leaving empty space.