---
id: FOCUS_STATES
title: "Focus States."
essence: "Every interactive element needs a visible, consistent focus indicator; keyboard users depend on it."
---

All interactive elements must have visible focus indicators for accessibility:

1. Use a consistent accent color for all focus states (e.g., `--color-primary`)
2. Use `:focus-visible` rather than `:focus` so focus rings appear on keyboard navigation but not on mouse clicks
3. Two patterns based on element type:

**Bordered elements** (inputs, textareas, selects): border-color change plus a light outer ring. The border provides the primary signal; the ring ensures visibility on low-contrast backgrounds.
```css
element:focus-visible {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px var(--color-focus-ring-light);
}
```

**Borderless elements** (buttons, links, icon buttons): tight outline with no offset. The outline hugs the element's edge.
```css
element:focus-visible {
  outline: 2px solid var(--color-primary);
}
```

Consistency in focus states aids keyboard navigation and accessibility.