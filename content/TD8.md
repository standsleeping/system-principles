---
id: TD8
title: "Domain type safety."
summary: ""
---

- Never allow untyped dictionaries or maps in domain layers.
- Instead of raising exceptions in domain logic, use Result types.
- Result types make success and failure explicit.
- Handle errors explicitly, so all possible outcomes are visible in the type signature.
- Domain functions should never throw, making them predictable.
- Test both success and failure paths without exception handling.