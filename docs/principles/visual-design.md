# Visual Design

Visual design principles govern aesthetics: how interfaces look, how hierarchy is communicated, and how users perceive structure through typography, color, and spacing.

## [VD1] Typography-Based Hierarchy

Establish visual importance through typography, not color or decoration:

1. Use font-weight (400, 500, 600, 700) for emphasis levels
2. Use font-size variations (xs, sm, md, lg, xl) for hierarchy
3. Prefer gray-700 for primary content, gray-400 for secondary
4. Avoid colored backgrounds on text elements (badges, labels, inline code)

Typography carries meaning. When weight and size do the work, color becomes available for other purposes (status, interaction, accent).

## [VD2] Transparent by Default

Small UI elements should not compete for attention:

1. Badges, labels, and inline elements have transparent backgrounds
2. Remove padding and border-radius from small text elements
3. Reserve background colors for major container elements
4. Use white backgrounds for subtle section separation

This reduces visual noise and lets content breathe.

## [VD3] Minimal Borders

Borders should define structure, not decorate:

1. Use subtle left borders (2px) for visual grouping and hierarchy
2. Use top borders for separating sequential items
3. Avoid rounded corners on small elements (badges, inline code)
4. Use border colors that complement content, not create noise
5. Prefer single-side borders over full boxes

Borders are structural cues. When everything has a border, nothing stands out.

## [VD4] Spacing Strategy

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

## [VD5] Color Usage

Reserve color for meaning:

1. Bright accent colors (purple, green) for borders and interactive elements
2. Muted text colors (gray-400) for secondary information
3. Dark text (gray-700) for primary content
4. Avoid using background colors to convey category or meaning

A restrained palette makes intentional color usage more impactful.

## [VD6] Simplification Patterns

When in doubt, simplify:

| Instead of | Prefer |
|------------|--------|
| Icons | Text (e.g., "true/false" over checkmarks) |
| Uppercase | Lowercase (softer appearance) |
| Background color | Font-weight for emphasis |
| Visual containers | Whitespace for breathing room |
| Decorative borders | Structural borders only |

Each visual element costs attention. Earn that cost.

## [VD7] Focus States

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

## [VD8] Token-Driven Design

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

## [VD9] Reset-First Approach

Start from a clean slate:

```css
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
```

Then build up intentionally. Every margin, every padding should be a deliberate choice, not a browser default.
