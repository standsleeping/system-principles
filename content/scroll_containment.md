---
id: SCROLL_CONTAINMENT
title: "Scroll Containment."
essence: "Only leaf content areas scroll; every container above them clips with overflow hidden."
---

Scrolling is contained within specific content slots, never at the layout level:

1. Layout containers have `overflow: hidden`
2. Content regions have `overflow-y: auto`
3. Only leaf content areas (sidebars, main content) scroll

This creates a clear hierarchy:

```
layout (overflow: hidden)
├── header (fixed height, no scroll)
├── content (overflow: hidden)
│   ├── sidebar (overflow-y: auto) ← scrolls here
│   └── main (overflow-y: auto)    ← scrolls here
└── footer (fixed height, no scroll)
```