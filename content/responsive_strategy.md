---
id: RESPONSIVE_STRATEGY
title: "Responsive Design Strategy."
essence: "Start with natural flow, measure where it breaks, then decide whether to let it wrap or control it explicitly."
---

When building responsive components:

1. **Start with natural flow**: Use `flex-wrap: wrap` and let content flow naturally
2. **Measure natural breakpoints**: Use width control to find where content wraps
3. **Decide: natural vs controlled**: Natural wrapping (flex-wrap) is simpler and adapts to any content length but has less predictable visual rhythm. Controlled breakpoints (container queries) give explicit layout changes and predictable visual states but require more CSS complexity.
4. **Test with variants**: Create variants that stress-test wrapping with long content
5. **Document decisions**: Record breakpoint decisions in component or docs

```javascript
// Responsive behavior:
// < 200px: metrics stack vertically
// 200-280px: metrics wrap to 2 lines
// > 280px: single line
```