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

## [VD10] Responsive Component Design

Components should present information optimally at every width, never overflowing their container. This requires explicit information hierarchy and graceful degradation.

### Information Hierarchy

Rank every piece of information in a component by importance:

```
1. Identity    (name, title)        - Must always be visible
2. Status      (metrics, counts)    - Core utility, high priority
3. Detail      (types, signatures)  - Nice to have, can hide
4. Decoration  (icons, badges)      - Progressive enhancement
```

Lower-priority items hide before higher-priority items truncate.

### Width Tiers

Define explicit layout tiers, not arbitrary breakpoints:

| Tier | Strategy |
|------|----------|
| **Wide** | All information visible, optimal layout |
| **Medium** | Hide lowest-priority items, maintain readability |
| **Narrow** | Abbreviate where possible, hide decorative elements |
| **Minimum** | Essential info only, truncate as last resort |

### Degradation Rules

Apply these rules in order as width decreases:

1. **Wrap** - Let flex containers wrap naturally
2. **Hide** - Remove low-priority information entirely
3. **Abbreviate** - "3 calls" → "3c", "decisions" → "dec"
4. **Truncate** - Ellipsis on text, only when nothing else works

Never:
- Overflow the container
- Truncate high-priority items while showing low-priority ones
- Create inconsistent line counts across similar items

### Implementation Pattern

```css
/* Base: wide layout */
.component__detail { display: block; }
.component__metric { /* full text */ }

/* Medium: hide detail */
@container (max-width: 350px) {
  .component__detail { display: none; }
}

/* Narrow: abbreviate metrics */
@container (max-width: 200px) {
  .component__metric--full { display: none; }
  .component__metric--abbrev { display: inline; }
}
```

Or use JavaScript to select content based on measured width:

```javascript
const width = container.offsetWidth;
const showDetail = width >= 350;
const abbreviate = width < 200;
```

### Consistent Visual Rhythm

Components at the same tier should have the same line count:

```
Wide (2 lines):
  process_payment (Order) → Result
  6 calls · 3 decisions

  validate_order (Order) → bool
  2 calls · 1 decision

Medium (2 lines):
  process_payment
  6 calls · 3 decisions

  validate_order
  2 calls · 1 decision
```

Inconsistent heights create visual noise in lists. Design tiers so all items at a given width have predictable dimensions.

### Testing Responsive Components

Use width-controlled preview (see [UT12]) to verify:

1. No overflow at any width
2. Information degrades in priority order
3. Consistent heights across variants
4. Readable at minimum supported width

Document the tier breakpoints in component source:

```javascript
// Responsive tiers:
// >= 350px: name + signature, metrics
// 200-349px: name, metrics (signature hidden)
// < 200px: name, abbreviated metrics
```

## [VD11] Data-Ink Ratio and Tabular Alignment

When presenting repeated metrics across items, optimize for scanability by reducing redundant labels and aligning values vertically.

### The Principle

Edward Tufte's data-ink ratio: maximize information, minimize redundant visual elements. When the same labels repeat on every row, move them to a single header:

```
Instead of:
  Customer       9 fields · 3 consumers · 2 producers
  DeliveryInfo   6 fields · 1 producer
  Ingredient     8 fields · 7 consumers · 3 producers

Prefer:
                        F   C   P
  Customer              9   3   2
  DeliveryInfo          6   —   1
  Ingredient            8   7   3
```

Benefits:
- **Scanability**: Eyes can quickly scan a column of aligned numbers
- **Comparison**: Easier to spot high/low values across items
- **Density**: More items visible in the same space
- **Reduced noise**: Labels stated once, not repeated 50 times

### Guidelines

1. **Deduplicate labels**: If a label appears on every row, move it to a header
2. **Align numbers vertically**: Use CSS grid or fixed-width columns
3. **Use tabular numerals**: `font-variant-numeric: tabular-nums` for consistent digit widths
4. **Use dashes for zeros**: `—` is clearer than `0` for "none" or "not applicable"
5. **Keep headers minimal**: Single letters or short abbreviations with tooltips for full names
6. **Right-align numbers**: Numbers align on the ones digit for easy comparison

### When to Apply

Appropriate when:
- Showing 5+ items with the same metric structure
- Numbers are primary information users need to compare
- The metric categories are stable (same columns for all items)

Not appropriate when:
- Items have different/variable fields
- Only 1-2 items displayed
- Descriptive text is more important than numeric values

### Implementation

```css
.metric-grid {
  display: grid;
  grid-template-columns: 1fr repeat(3, 3ch);  /* name + 3 metric columns */
  gap: var(--spacing-xs);
}

.metric-value {
  font-variant-numeric: tabular-nums;
  text-align: right;
}

.metric-empty {
  color: var(--gray-300);
}
```

```html
<!-- Section header with column labels -->
<div class="section-header metric-grid">
  <span>DATA</span>
  <span class="metric-label" title="Fields">F</span>
  <span class="metric-label" title="Consumers">C</span>
  <span class="metric-label" title="Producers">P</span>
</div>

<!-- Data rows -->
<div class="entity-row metric-grid">
  <span>Customer</span>
  <span class="metric-value">9</span>
  <span class="metric-value">3</span>
  <span class="metric-value">2</span>
</div>
```

### Responsive Considerations

At narrow widths, the tabular layout may need to degrade:

| Width | Strategy |
|-------|----------|
| **Wide** | Full grid with aligned columns |
| **Medium** | Inline format with separators: `9 · 3 · 2` |
| **Narrow** | Abbreviated: `9f 3c 2p` or hide secondary metrics |

The inline format loses alignment benefits but remains compact. Consider which metrics are essential vs. which can be hidden at narrow widths.

## [VD12] One Signal Per Meaning

Each piece of information should be communicated once, through one visual channel.

### The Problem

When the same meaning is conveyed through multiple signals, it creates redundancy:

```css
/* Redundant: both background AND text color indicate "resolved" */
.row.resolved {
  background: var(--gray-100);  /* Signal 1 */
}
.row.resolved .name {
  color: var(--blue-600);       /* Signal 2 - same meaning */
}
```

The user sees two visual changes but learns one fact. The extra signal is noise.

### The Principle

Choose one visual channel per meaning:

| Meaning | Preferred Signal | Avoid Adding |
|---------|------------------|--------------|
| Navigable/clickable | Text color (blue) | Background color |
| Selected | Background color | Border + background |
| Disabled | Opacity reduction | Gray text + gray background |
| Error state | Text color (red) | Red text + red border + red background |

### When Multiple Signals Are Justified

Multiple signals are appropriate when they serve different purposes:

1. **Accessibility**: Focus states may use both outline AND background for visibility
2. **Hover + selection**: Hover is transient feedback, selection is persistent state
3. **Different information**: Blue text (navigable) + badge (count) convey different facts

### Testing for Redundancy

Ask: "If I remove this visual treatment, does the user lose information?"

- If yes → keep it
- If no → remove it
