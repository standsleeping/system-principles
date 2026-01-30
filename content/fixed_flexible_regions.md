---
id: FIXED_FLEXIBLE_REGIONS
title: "Fixed and Flexible Regions."
summary: "Layouts combine fixed-size regions (headers, footers, sidebars) with flexible regions that fill remaining space:"
---

Layouts combine fixed-size regions (headers, footers, sidebars) with flexible regions that fill remaining space:

- **Fixed regions**: Use explicit heights/widths via CSS variables (tokens)
- **Flexible regions**: Use `flex: 1` to fill available space
- **Resizable regions**: Constrain with min/max bounds

Example token definitions:

```css
:root {
  --layout-header-height: 48px;
  --layout-sidebar-default-width: 280px;
  --layout-sidebar-min-width: 200px;
  --layout-sidebar-max-width: 500px;
}
```