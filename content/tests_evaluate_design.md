---
id: TESTS_EVALUATE_DESIGN
title: "Tests evaluate design quality."
essence: "If testing is painful, don't blame the tests: fix the design."
---

Well-designed components produce tests that are easy to read, write, and run. We use our tests as a way of evaluating the quality of our design.

**Design smell indicators in tests:**

| Test Symptom | Design Problem |
|--------------|----------------|
| Requires extensive mocking | Component has too many dependencies |
| Setup is longer than assertion | Boundaries are unclear |
| Name is hard to write | Function does too much |
| Needs to patch internals | Missing seam or abstraction |

If testing is painful, don't blame the tests: fix the design.