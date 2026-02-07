---
id: DEPEND_ON_VALUES
title: "Depend on values, not behaviors."
essence: "Components that exchange data instead of calling each other can be tested, moved, and run in parallel."
---

Our code should always depend on values (i.e. data), not behaviors (i.e. code):

1. "Values" are just data, or anything that has no behavior.
2. Replace method calls with data passing between components.
3. Components should transform values instead of calling each other.
4. Building blocks should agree on data shape, not on implementation.
5. Decisions should live in one place, and dependencies in another.
6. Data is flexible: it can travel across functions, threads, or networks.
7. Every value is a potential message, and messages allow concurrency.
8. When components only transform values, they can run in parallel.