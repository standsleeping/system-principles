---
id: BOUNDARY_OWNERSHIP
title: "Boundary Ownership."
essence: "Each component should look visually complete in isolation; relying on a neighbor for your edge is implicit coupling."
---

Components own their own visual boundaries. This applies to both parent/child and sibling relationships.

**Parent/Child: Container Owns Border, Child Owns Padding**

When a container has structural borders (separating header from content, for example), the container defines those borders. Children provide their own internal padding.

**Separator Containers**

When a container uses borders to separate repeated sections (e.g. a scrollable list of sections with horizontal rules between them), the container must not also carry content padding. Putting horizontal padding and a horizontal separator on the same element couples two concerns: the separator's visual extent depends on box-model details (border renders outside padding). It works by coincidence, not by structure.

The separator container gets zero horizontal padding. Its children inherit content inset:

```css
.section                { padding: var(--spacing-2xl) 0 var(--spacing-xl); }
.section + .section     { border-top: 1px solid var(--color-border); }
.section > *            { padding-left: var(--spacing-2xl); padding-right: var(--spacing-2xl); }
```

The section owns the separator (zero horizontal padding means the border spans full width). The children own their content inset. No position tricks, no pseudo-elements; the box model does what it says.

**CSS shorthand trap:** Children that set their own vertical padding must use longhand properties (`padding-top`/`padding-bottom`), not the `padding` shorthand. The shorthand resets all four sides, silently clobbering the horizontal values inherited from `.section > *`.

```css
/* Wrong: shorthand resets padding-left/right to 0 */
.demo-block { padding: var(--spacing-lg) 0; }

/* Right: longhands leave horizontal padding alone */
.demo-block { padding-top: var(--spacing-lg); padding-bottom: var(--spacing-lg); }
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