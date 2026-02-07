---
id: OVERFLOW_DETECTION
title: "Overflow Detection."
essence: "Good overflow tooling identifies both the symptom (page scrolls) and the cause (which element)."
---

The core constraint (no page-level scrolling) requires tooling to detect when the document size exceeds the viewport.

**What to Measure**:

```javascript
// Viewport: what the user sees
const viewport = { width: window.innerWidth, height: window.innerHeight };

// Document: how big the page actually is
const document = {
  width: Math.max(body.scrollWidth, html.scrollWidth),
  height: Math.max(body.scrollHeight, html.scrollHeight)
};

// Violation: document larger than viewport
const hasScroll = {
  horizontal: document.width > viewport.width,
  vertical: document.height > viewport.height
};
```

For each element, check: Does its bounding rect extend beyond the viewport? Does it have internal scroll? What are its computed overflow properties? This identifies both the symptom (page scrolls) and the cause (specific element).