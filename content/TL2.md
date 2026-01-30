---
id: TL2
title: "Return explicit error values."
summary: "Translators return conversion errors as values, not exceptions. Use tuple returns: `(Error | None, Result | None)`."
---

Translators return conversion errors as values, not exceptions. Use tuple returns: `(Error | None, Result | None)`.

```python
# Good: errors as values
def db_row_to_domain_translator(
    row: UserRowDict
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

# Bad: exceptions for control flow
def db_row_to_domain_translator(row: dict[str, object]) -> User:
    if not row:
        raise ValueError("Empty row")  # Forces exception handling

    return User(id=uuid.UUID(row["id"]), email=row["email"])
```