---
id: TL3
title: "Validate structure, not business rules."
summary: "Translators check that data has the right shape and types. Domain validators check business rules."
---

Translators check that data has the right shape and types. Domain validators check business rules.

Translators build context-free proofs; domain actions enforce policy and stateful rules.

- Translators SHOULD enforce (context-free):
  - Presence and basic normalization (trim/case-fold), simple formats (UUIDs, ISO dates, email syntax).
  - Cross-field form invariants that require no I/O (e.g., password == confirmation, exactly-one-of).
  - Smart constructors that only produce proof-carrying values on success (e.g., `EmailAddress`, `ConfirmedPassword`).
- Translators MUST NOT enforce (business/stateful):
  - Email uniqueness, invite validity, quotas/rate limits, time-based rules, or policy like password strength.
  - Anything requiring repositories, configuration, or clocks.

**Signup split example:**
- Translator (HTTP → SignUpInput): produces `SignUpInput = { email: EmailAddress, password: ConfirmedPassword, terms: AcceptedTerms }` or structured errors.
- Domain action: checks strength policy, uniqueness, eligibility/invites, then performs effects.

```python
# Translator: structural validation
def api_to_domain_translator(
    data: dict
) -> tuple[TranslatorError | None, Order | None]:
    if "items" not in data or not isinstance(data["items"], list):
        return TranslatorError("Missing or invalid 'items'"), None

    return None, Order(
        id=uuid.UUID(data["id"]),
        items=[Item(**item) for item in data["items"]]
    )

# Domain validator: business rules
def validate_order(order: Order) -> list[ValidationError]:
    errors = []
    if len(order.items) == 0:
        errors.append(ValidationError("Order must have at least one item"))
    if order.total < 0:
        errors.append(ValidationError("Order total cannot be negative"))
    return errors
```