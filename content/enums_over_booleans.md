---
id: ENUMS_OVER_BOOLEANS
title: "Use enums over booleans."
summary: "There is no place for boolean data types in entity modeling, almost ever."
---

There is no place for boolean data types in entity modeling, almost ever.

```python
# Boolean hides information
class User:
    is_active: bool

# Enum captures actual states
class UserStatus(Enum):
    PENDING_VERIFICATION = "pending_verification"
    ACTIVE = "active"
    SUSPENDED = "suspended"

class User:
    status: UserStatus
```