---
id: LAYOUT_VARIANTS
title: "Layout Variants."
summary: "Support multiple layout configurations through modifier classes on a shared base:"
---

Support multiple layout configurations through modifier classes on a shared base:

| Variant | Description |
|---------|-------------|
| `single-column` | Centered content with max-width |
| `left-sidebar` | Sidebar on left, main content on right |
| `right-sidebar` | Main content on left, sidebar on right |
| `combined` | Both sidebars visible |

The base `.layout` class provides the viewport-locked shell. Variants adjust which regions are visible and how space is distributed.

### Common Overflow Causes

When the no-scroll constraint is violated, common causes include:

1. Using `100vw` for width (includes scrollbar width on some browsers)
2. Mismatched height calculations (e.g., `calc(100vh - 50px)` when nav is not 50px)
3. Flex children with min-height exceeding available space
4. Missing `box-sizing: border-box`
5. Content regions without `overflow: hidden` or `overflow: auto`