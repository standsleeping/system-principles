---
id: BD2
title: Structure reflects sources of change
summary: Module boundaries should align with what changes together.
tags: [parnas, modularity, coupling]
related: [BD1, BD4]
---

Structure your system so that things that change together are grouped
together, and things that change independently are separated.

## Rationale

David Parnas identified that the key to modular design is identifying
"sources of change" - the decisions that might need to change over time.
Each module should hide one such decision.

## Application

1. Identify what might change (data formats, algorithms, external services)
2. Create boundaries that isolate each source of change
3. Design interfaces that don't leak implementation details
