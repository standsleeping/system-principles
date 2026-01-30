---
id: TL5
title: "Integrator translators compose unit translators."
summary: "Integrator translators orchestrate multiple conversions. They compose unit translators and validation functions."
---

Integrator translators orchestrate multiple conversions. They compose unit translators and validation functions.

```python
# Integrator: composes unit translators
def db_row_to_user_translator(
    row: dict[str, object]
) -> tuple[TranslatorError | None, User | None]:
    # Use unit translators
    err, user_id = parse_uuid(row.get("id", ""))
    if err:
        return err, None

    err, created = parse_timestamp(row.get("created_at", ""))
    if err:
        return err, None

    return None, User(
        id=user_id,
        email=row["email"],
        created_at=created
    )
```