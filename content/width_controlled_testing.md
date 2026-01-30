---
id: WIDTH_CONTROLLED_TESTING
title: "Width-Controlled Responsive Testing."
summary: "Test responsive behavior by controlling container width, not viewport width:"
---

Test responsive behavior by controlling container width, not viewport width:

```javascript
const preview = document.createElement('div');
preview.style.width = `${this.previewWidth}px`;
preview.appendChild(component.render(props));
```

Container width is preferred over viewport width because it enables faster iteration (no window resizing), precise control (exact pixel values), side-by-side comparison (same viewport, different widths), and component-level testing.

Provide slider + input + auto button for width control. Test components at key widths to understand wrapping behavior and document where natural breakpoints occur.