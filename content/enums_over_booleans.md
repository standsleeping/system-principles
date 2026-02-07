---
id: ENUMS_OVER_BOOLEANS
title: "Use enums over booleans."
essence: "A boolean hides states that already exist; an enum names them and makes the compiler enforce them."
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