---
id: SEPARATE_DECISIONS_BEHAVIOR
title: "Separate decisions from behavior."
essence: "A match that both decides and executes complects two concerns. Lift the decision into a dispatch table so data picks the handler and the handler just runs."
---

Don't embed "what to do" inside "how to do it." Instead of a match statement that both decides and executes, use a dispatch table (dictionary) that maps cases to handlers.

Avoid storing knowledge as control flow. Prefer data-driven dispatch tables (decisions as data). Represent the domain as plain data with behavior in functions, and make time/identity explicit inputs rather than hidden globals.

```python
# In-place decision (complects decision + behavior)
match user.status:
    case UserStatus.ACTIVE:
        return handle_active_user(user)
    case UserStatus.SUSPENDED:
        return handle_suspended_user(user)

# Decision as data (separation)
handlers = {
    UserStatus.ACTIVE: handle_active_user,
    UserStatus.SUSPENDED: handle_suspended_user,
}
return handlers[user.status](user)
```