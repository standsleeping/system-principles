---
id: FOCUS_STATES
title: "Focus States."
essence: "Every interactive element needs a visible, consistent focus indicator; keyboard users depend on it."
---

All interactive elements must have visible focus indicators for accessibility:

1. Use a consistent accent color for all focus states (e.g., `--color-primary`)
2. Two patterns based on element type:

**Bordered elements** (inputs, textareas): border-color change only. No box-shadow glow; the border itself is the indicator.
```css
element:focus {
  border-color: var(--color-primary);
}
```

**Borderless elements** (buttons, links, icon buttons): tight outline with no offset. The outline hugs the element's edge.
```css
element:focus {
  outline: 2px solid var(--color-primary);
}
```

Consistency in focus states aids keyboard navigation and accessibility.