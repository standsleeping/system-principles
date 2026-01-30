---
id: NO_DEPS_IN_DISPATCH
title: "Keep dependencies out of dispatch tables."
summary: "Dispatch tables enumerate decisions and point to pure units or thin integrators. Do not perform I/O or side effects in the dispatch table itself."
---

Dispatch tables enumerate decisions and point to pure units or thin integrators. Do not perform I/O or side effects in the dispatch table itself.

```python
# Bad: side effects captured at decision site
handlers = {
    UserStatus.ACTIVE: lambda u: log_and_notify(handle_active_user(u)),
}

# Good: handlers are pure; effects happen at the action boundary
handlers = {
    UserStatus.ACTIVE: handle_active_user,
}

result = handlers[user.status](user)
log_result(result)
notify(result)
```

Guidance:

1. Place effects in actions at boundaries; keep handlers pure where feasible.
2. Pass time/loggers/resources explicitly at the boundary; do not close over them in handlers.