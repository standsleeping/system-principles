---
id: PD8
title: "Data-driven dispatch for domain logic."
summary: "Complecting structure (what states exist) with behavior (what to do) makes both harder to change independently."
---

Complecting structure (what states exist) with behavior (what to do) makes both harder to change independently.

```python
# Pattern matching complects structure and behavior
match user.status:
    case UserStatus.ACTIVE:
        handle_active(user)
    case UserStatus.SUSPENDED:
        handle_suspended(user)

# Decisions as data
handlers = {
    UserStatus.ACTIVE: handle_active,
    UserStatus.SUSPENDED: handle_suspended,
}
result = handlers[user.status](user)
```

The second approach separates decisions (the dispatch table) from handlers (what to do), making operations easier to add and test independently.