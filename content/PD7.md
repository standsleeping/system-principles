---
id: PD7
title: "Manage exhaustiveness explicitly."
summary: "Since Python lacks total pattern exhaustiveness, use enums for variants, default handlers where appropriate, and validation tests that assert all enum members are mapped."
---

Since Python lacks total pattern exhaustiveness, use enums for variants, default handlers where appropriate, and validation tests that assert all enum members are mapped.

```python
def test_handlers_cover_all_statuses() -> None:
    assert set(handlers.keys()) == set(UserStatus)
```

Guidance:

1. Use property-based tests to generate variant coverage and assert dispatch invariants.
2. Prefer running core logic in a REPL/simulator without external I/O.