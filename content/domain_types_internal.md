---
id: DOMAIN_TYPES_INTERNAL
title: "Use domain types internally."
essence: "Use domain types (classes, dataclasses) for business entities. They enforce invariants, have identity, and are immutable."
---

**Use for**: Business entities, value objects, internal logic.

Domain types (classes, records with behavior) represent domain concepts with identity. They say "this is a User," not just "this has user-like fields."

- **Pros**: Can enforce invariants at construction, have computed properties, methods, and identity.
- **Cons**: Need serialization steps to leave the system.
- **Feature**: Immutability makes them safe to pass around.

**Python example** using `dataclass`:

```python
@dataclass(frozen=True)
class User:
    id: UUID
    email: EmailAddress  # Refined type!

    @property
    def domain(self) -> str:
        return self.email.split("@")[1]
```