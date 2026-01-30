---
id: SPACING_STRATEGY
title: "Spacing Strategy."
summary: "Use modern CSS layout for spacing:"
---

Use modern CSS layout for spacing:

1. **Flex gap** for spacing between elements (not margins)
2. **Padding** for internal spacing within containers
3. Avoid the margin-bottom anti-pattern
4. Let flex containers manage distribution

```css
/* Prefer this */
.container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

/* Over this */
.container > * {
  margin-bottom: var(--spacing-2);
}
.container > *:last-child {
  margin-bottom: 0;
}
```

Gap-based spacing is more predictable and requires less override logic.