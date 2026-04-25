---
id: AUTO_VERIFICATION
title: "Automatic Verification."
essence: "Treat layout bugs as first-class defects. Any layout constraint worth writing down is worth having tooling enforce automatically. Manual inspection doesn't scale."
---

Layout constraints should be automatically verified, not manually inspected. When a constraint like "no page-level scrolling" exists, tooling should:

1. Detect violations immediately
2. Identify the specific cause
3. Integrate with automated tests
4. Be available during development

Treat layout bugs as first-class defects with proper tooling support.