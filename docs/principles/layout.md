# Layout

Layout principles govern the structural arrangement of UI components: where content lives, what contains what, and how space is allocated.

## [LY1] No Page-Level Scrolling

**No page should ever scroll at the html/body level.**

Individual components may scroll internally, but the page itself must fit exactly within the viewport. When the document size exceeds the viewport, something is wrong with the CSS layout.

This constraint:

1. Forces intentional scroll containment decisions
2. Prevents accidental overflow from breaking layouts
3. Makes overflow bugs immediately visible
4. Enables predictable, viewport-locked application shells

## [LY2] Viewport-Locked Containers

The root layout container fills exactly the viewport and prevents page-level scrolling:

```css
.layout {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}
```

From this foundation, all scrolling must be explicitly delegated to content regions.

## [LY3] Fixed and Flexible Regions

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

## [LY4] Scroll Containment

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

## [LY5] Container Boundary Rule

**The container owns the border; the child provides the padding.**

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

## [LY6] Empty State Collapse

Empty structural elements should automatically hide:

```css
.layout-header:empty,
.layout-footer:empty,
.layout-sidebar-header:empty {
  display: none;
}
```

This allows optional slots to be omitted without leaving empty space.

## [LY7] Layout Variants

Support multiple layout configurations through modifier classes on a shared base:

| Variant | Description |
|---------|-------------|
| `single-column` | Centered content with max-width |
| `left-sidebar` | Sidebar on left, main content on right |
| `right-sidebar` | Main content on left, sidebar on right |
| `combined` | Both sidebars visible |

The base `.layout` class provides the viewport-locked shell. Variants adjust which regions are visible and how space is distributed.

## Common Overflow Causes

When the no-scroll constraint is violated, common causes include:

1. Using `100vw` for width (includes scrollbar width on some browsers)
2. Mismatched height calculations (e.g., `calc(100vh - 50px)` when nav is not 50px)
3. Flex children with min-height exceeding available space
4. Missing `box-sizing: border-box`
5. Content regions without `overflow: hidden` or `overflow: auto`

## [LY8] Never Calculate What Layout Can Handle

**Never hardcode a value that depends on another element's size.** This creates duplicated knowledge: one element's size is defined in one place, and a guess about that size is hardcoded elsewhere. When either changes, they drift apart silently.

### The Problem: Duplicated Knowledge

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

### The Solution: Let Flexbox Distribute Space

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

### When You Must Use Explicit Sizes

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
