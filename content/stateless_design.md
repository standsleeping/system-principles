---
id: STATELESS_DESIGN
title: "Stateless design."
summary: "All computations are pure. No in-memory state anywhere."
---

All computations are pure. No in-memory state anywhere.

Request comes in, data is fetched, computation runs, result is written, response goes out. Nothing lingers. No object lifetimes to manage, no cache invalidation, no "did that update propagate yet?" Each request is independent.