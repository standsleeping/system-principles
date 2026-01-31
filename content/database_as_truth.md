---
id: DATABASE_AS_TRUTH
title: "Database as truth."
summary: "All reads go through SQL queries. All writes append events."
---

All reads go through SQL queries. All writes append events.

Prefer flat, transactional, event-driven state in the database over rich object graphs in memory. Stateful objects with interlocking relationships create a second layer of truth that drifts from the database and complicates reasoning. More code to keep things stateless is worth the tradeoff.