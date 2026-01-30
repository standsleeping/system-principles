---
id: UT6
title: "Development Workflow."
summary: "Load debugging tools on every page during development:"
---

Load debugging tools on every page during development:

```javascript
UIDebug.scan()           // Find and highlight overflow
UIDebug.traceOverflow(el) // Walk up DOM to find source
UIDebug.measure(el)      // Inspect specific element
UIDebug.watch()          // Monitor during resize
UIDebug.clear()          // Remove highlights
```

Run layout constraint tests as part of CI/CD. Fail the build if layout constraints are violated.