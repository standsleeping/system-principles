---
id: CONTINUOUS_MONITORING
title: "Continuous Monitoring."
essence: "One-time scans miss overflow that appears at certain sizes or after dynamic loads; watch continuously."
---

For dynamic content or resize behavior, watch for changes:

```javascript
// Check every second, report when state changes
UIDebug.watch(1000);
```

This catches overflow that only appears at certain viewport sizes or after dynamic content loads.