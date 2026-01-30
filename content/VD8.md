---
id: VD8
title: "Token-Driven Design."
summary: "Define design decisions as CSS variables (tokens):"
---

Define design decisions as CSS variables (tokens):

```css
:root {
  /* Typography */
  --font-size-sm: 12px;
  --font-size-base: 13px;
  --font-size-lg: 15px;

  /* Spacing */
  --spacing-sm: 4px;
  --spacing-md: 6px;
  --spacing-lg: 8px;

  /* Colors */
  --color-primary: var(--purple-500);
  --color-text: var(--gray-700);
  --color-text-light: var(--gray-400);
}
```

Benefits:

1. Single source of truth for design decisions
2. Easy global adjustments
3. Semantic naming (--color-primary vs #8300CA)
4. Consistent references across components