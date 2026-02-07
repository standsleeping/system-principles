---
id: INTERCHANGE_AT_BOUNDARIES
title: "Use interchange types at boundaries."
essence: "Use TypedDict/interfaces for JSON, API requests, database rows. They describe shape without behavior and serialize directly."
---

**Use for**: JSON blobs, API requests/responses, database rows, configuration files.

Interchange types describe the structure of data without behavior. They say "this data has these fields with these types" and serialize directly to JSON.

- **Pros**: Serialize natively to JSON. Compatible with external systems.
- **Cons**: No methods, no properties, no invariants (a negative radius is a valid int), clumsy for deep nesting.
- **Feature**: Can be partial, useful for patch requests or sparse data.

**Python example** using `TypedDict`:

```python
class UserPayload(TypedDict):
    id: str
    email: str
    # No guarantees that email is valid, just that it's a string.
```

**When to skip interchange types**: If the external format maps 1:1 to your domain types, you can parse directly into domain types without an intermediate layer. Intermediate types that exist only for mapping add maintenance cost and create opportunities for bugs when fields drift out of sync. Use explicit interchange types when: (a) the external shape genuinely differs from your domain, (b) you need to isolate against external format changes, or (c) multiple formats feed the same domain type.