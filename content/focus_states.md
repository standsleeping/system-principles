---
id: FOCUS_STATES
title: "Focus States."
essence: "Every interactive element needs a visible, consistent focus indicator; keyboard users depend on it."
---

All interactive elements must have visible focus indicators for accessibility:

1. Use a consistent accent color for all focus states (e.g., purple-500)
2. Two patterns based on element type:

**Bordered elements** (inputs, buttons with borders):
```css
element:focus {
  border-color: var(--purple-500);
  box-shadow: 0 0 0 2px var(--purple-100);
}
```

**Borderless elements** (links, icon buttons):
```css
element:focus {
  outline: 2px solid var(--purple-500);
  outline-offset: 2px;
}
```

Consistency in focus states aids keyboard navigation and accessibility.