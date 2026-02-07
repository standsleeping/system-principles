---
id: RESPONSIVE_COMPONENTS
title: "Responsive Component Design."
essence: "Rank information by priority; lower-priority items hide before higher-priority items truncate."
---

Components should present information optimally at every width, never overflowing their container. This requires explicit information hierarchy and graceful degradation.

**Information Hierarchy**: Rank every piece of information by importance:

1. Identity (name, title) - Must always be visible
2. Status (metrics, counts) - Core utility, high priority
3. Detail (types, signatures) - Nice to have, can hide
4. Decoration (icons, badges) - Progressive enhancement

Lower-priority items hide before higher-priority items truncate.

**Width Tiers**: Define explicit layout tiers:

| Tier | Strategy |
|------|----------|
| **Wide** | All information visible, optimal layout |
| **Medium** | Hide lowest-priority items, maintain readability |
| **Narrow** | Abbreviate where possible, hide decorative elements |
| **Minimum** | Essential info only, truncate as last resort |

**Degradation Rules**: Apply in order as width decreases:

1. **Wrap** - Let flex containers wrap naturally
2. **Hide** - Remove low-priority information entirely
3. **Abbreviate** - "3 calls" → "3c", "decisions" → "dec"
4. **Truncate** - Ellipsis on text, only when nothing else works

Never:
- Overflow the container
- Truncate high-priority items while showing low-priority ones
- Create inconsistent line counts across similar items

**Implementation Pattern**:

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

**Consistent Visual Rhythm**: Components at the same tier should have the same line count. Inconsistent heights create visual noise in lists. Design tiers so all items at a given width have predictable dimensions.

**Testing**: Use width-controlled preview (see UT12) to verify no overflow at any width, information degrades in priority order, consistent heights across variants, and readable at minimum supported width.