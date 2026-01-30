---
id: OVERFLOW_CAUSES
title: "Common Overflow Causes."
summary: "When the no-scroll constraint is violated, common causes include viewport width issues, mismatched calculations, flex sizing, box-sizing, and missing overflow properties."
---

When the no-scroll constraint is violated, common causes include:

1. Using `100vw` for width (includes scrollbar width on some browsers)
2. Mismatched height calculations (e.g., `calc(100vh - 50px)` when nav is not 50px)
3. Flex children with min-height exceeding available space
4. Missing `box-sizing: border-box`
5. Content regions without `overflow: hidden` or `overflow: auto`
