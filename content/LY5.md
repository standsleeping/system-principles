---
id: LY5
title: "Boundary Ownership."
summary: "Components own their own visual boundaries. This applies to both parent/child and sibling relationships."
---

Components own their own visual boundaries. This applies to both parent/child and sibling relationships.

**Parent/Child: Container Owns Border, Child Owns Padding**

When a container has structural borders (separating header from content, for example), the container defines those borders. Children provide their own internal padding.

This allows "flush" variants where children fill edge-to-edge:

```css
/* Normal: container provides padding */
.sidebar-header {
  padding: var(--spacing-lg) var(--spacing-2xl);
  border-bottom: 1px solid var(--gray-200);
}

/* Flush: child fills to edges, provides its own padding */
.sidebar-header-flush {
  padding: 0;
  border-bottom: 1px solid var(--gray-200);
}
```

**Siblings: Each Component Completes Itself**

When two components sit adjacent, each should be visually complete in isolation. A component shouldn't rely on its neighbor to provide its visual edge.

**Test**: If you render each component alone, which one looks incomplete?

```
nav (no bottom border)     →  looks unfinished
content (no top border)    →  looks fine
```

The nav owns the border because it's incomplete without it:

```css
nav {
  border-bottom: 1px solid var(--gray-200);
}
```

The content area shouldn't add a top border to compensate for the nav's missing boundary. That creates implicit coupling.