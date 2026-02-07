---
id: EMPTY_STATE_COLLAPSE
title: "Empty State Collapse."
essence: "Empty structural elements hide automatically, so optional slots can be omitted without leaving gaps."
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