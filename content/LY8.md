---
id: LY8
title: "Never Calculate What Layout Can Handle."
summary: ""
---

**Never hardcode a value that depends on another element's size.** This creates duplicated knowledge: one element's size is defined in one place, and a guess about that size is hardcoded elsewhere. When either changes, they drift apart silently.

**The Problem: Duplicated Knowledge**

Consider this common pattern:

```html
<!-- nav.html -->
<nav style="padding: 0.75rem;">...</nav>  <!-- Creates ~53px height -->
```

```css
/* styles.css */
.main-content {
  min-height: calc(100vh - 50px);  /* Assumes nav is 50px */
}
```

The nav's height is implicitly defined by its content and padding (~53px). The main content calculation assumes 50px. This 3px discrepancy causes page scroll, and the bug is invisible until someone notices the layout drifts by a few pixels.

This pattern is fragile because:

- The two values have no connection in code
- Changing nav padding silently breaks the layout
- The "50px" is a magic number with no clear origin
- Debugging requires measuring actual rendered sizes

**The Solution: Let Flexbox Distribute Space**

Instead of calculating remaining space, use flex layout to let the browser handle distribution automatically:

```css
body {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

nav {
  /* No explicit height; sizes to content */
}

main {
  flex: 1;  /* "Take whatever space remains" */
}
```

Now the nav can be 50px, 53px, or 100px. The main content automatically adjusts. No magic numbers, no synchronization required, no brittleness.

**When You Must Use Explicit Sizes**

If explicit dimensions are truly required (rare), use a single CSS variable that both elements reference:

```css
:root {
  --nav-height: 50px;
}

nav {
  height: var(--nav-height);
}

.main-content {
  min-height: calc(100vh - var(--nav-height));
}
```

This creates a single source of truth. But prefer the flexbox approach: it eliminates the variable entirely.