---
id: VIEWPORT_AS_FRAME
title: "Viewport as Frame."
essence: "The viewport edge already provides visual containment; padding inside scrollable content creates a frame inside the frame."
---

For content that scrolls horizontally (or fills the viewport), the browser window edge is the boundary. Adding internal padding creates a redundant inner frame that wastes space and fights the scroll experience.

**The test**: if the user will scroll to see more content, the viewport edge is doing the framing. Don't double-frame it.

```css
/* Wrong: padding creates a visible gap between content and viewport edge */
.scrollable-area {
  padding: 24px;
  overflow-x: auto;
}

/* Right: content runs to the viewport edge; the window is the frame */
.scrollable-area {
  overflow-x: auto;
}
```

Non-scrolling content below (settings panels, footers) can have its own padding because it occupies a different visual zone. The principle applies to the scrollable region specifically.

**Relationship to BOUNDARY_OWNERSHIP**: BOUNDARY_OWNERSHIP says each component should look complete in isolation. VIEWPORT_AS_FRAME says the viewport is a component too, and it already looks complete. Don't re-draw its edges.
