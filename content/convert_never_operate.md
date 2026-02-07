---
id: CONVERT_NEVER_OPERATE
title: "Translators only convert, never operate."
essence: "Translators are pure shape converters: no business logic, no decisions, no side effects."
---

A translator transforms data representations. It never performs business logic, makes decisions, or triggers side effects.

The most common pattern is converting **Interchange Data** (TypedDicts) to **Domain Data** (Dataclasses).

```python
# Good: pure conversion
def http_to_domain_translator(
    request: Request
) -> tuple[TranslatorError | None, UserCommand | None]:
    data = await request.json()

    if not data.get("email"):
        return TranslatorError("Missing 'email'"), None

    return None, UserCommand(
        user_id=uuid.UUID(data.get("user_id", str(uuid.uuid4()))),
        email=data["email"]
    )

# Bad: translator performs business logic
def http_to_domain_translator(request: Request) -> UserCommand:
    data = await request.json()
    user = UserCommand(email=data["email"])

    # Business operation doesn't belong here
    if is_premium_user(user.email):
        user.permissions = ["admin"]

    return user
```