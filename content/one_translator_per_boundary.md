---
id: ONE_TRANSLATOR_PER_BOUNDARY
title: "One translator per boundary type."
summary: "Create specialized translators for each architectural boundary. Don't create generic \"do everything\" translators."
---

Create specialized translators for each architectural boundary. Don't create generic "do everything" translators.

```python
# Network → Domain
async def http_to_domain_translator(
    request: Request
) -> tuple[TranslatorError | None, UserCommand | None]:
    data = await request.json()

    if not data.get("email"):
        return TranslatorError("Missing 'email'"), None

    try:
        user_id = uuid.UUID(data.get("user_id", str(uuid.uuid4())))
    except ValueError:
        return TranslatorError("Invalid 'user_id' format"), None

    return None, UserCommand(user_id=user_id, email=data["email"])

# Database → Domain
def db_row_to_domain_translator(
    row: dict[str, object]
) -> tuple[TranslatorError | None, User | None]:
    if not row:
        return TranslatorError("Empty row"), None

    try:
        return None, User(
            id=uuid.UUID(row["id"]),
            email=row["email"],
            created_at=datetime.fromisoformat(row["created_at"])
        )
    except KeyError as e:
        return TranslatorError(f"Missing column: {e}"), None
    except (ValueError, TypeError) as e:
        return TranslatorError(f"Invalid data format: {e}"), None
```