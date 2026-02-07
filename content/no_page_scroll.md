---
id: NO_PAGE_SCROLL
title: "No Page-Level Scrolling."
essence: "If the page itself scrolls, something is wrong; scrolling is an intentional per-component decision."
---

No page should ever scroll at the html/body level. Individual components may scroll internally, but the page itself must fit exactly within the viewport. When the document size exceeds the viewport, something is wrong with the CSS layout.

This constraint:

1. Forces intentional scroll containment decisions
2. Prevents accidental overflow from breaking layouts
3. Makes overflow bugs immediately visible
4. Enables predictable, viewport-locked application shells