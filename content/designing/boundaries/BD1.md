---
id: BD1
title: Start simple, add useful complexity
summary: A complex system that works evolved from a simple system that worked.
tags: [galls-law, complexity, incremental]
related: [BD2, AB1]
---

Begin with the simplest possible implementation that solves the problem.
Add complexity only when it provides clear value.

## Rationale

Gall's Law states that complex systems that work evolved from simpler
systems that worked. Starting complex usually fails because there are
too many interacting parts to debug.

## Application

1. Implement the minimal solution first
2. Verify it works correctly
3. Add features incrementally, testing each addition
4. Resist the urge to "design for the future"
