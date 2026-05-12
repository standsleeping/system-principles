---
id: ENCODE_BY_FAILURE_MODE
title: "Encode by failure mode."
essence: "Silent corruption belongs in types; loud failures can stay as runtime checks; messy domains resist exhaustive encoding."
related: [PRECISION_MATCHES_STABILITY, SHAPE_NOT_INVARIANTS, ILLEGAL_STATES_UNREPRESENTABLE, CHASE_CHECKS_UPSTREAM, PUSH_VARIATION_INTO_DATA]
---

Three buckets decide where an invariant lives. The question is what a violation looks like if nothing else catches it.

**Silent corruption goes in types.** If a violation produces wrong data without an immediate error (a transposed argument, a unit mix-up, a stale identifier reused as fresh), the type system is the only thing that can catch it. The cost of encoding is justified because the alternative is a quiet bug that surfaces months later in a customer report.

```python
# Silent: int doesn't distinguish account from user from amount
def transfer(from_id: int, to_id: int, cents: int) -> None: ...

transfer(user.id, account.id, balance)  # transposed; no error, wrong money moved

# Encoded: NewType makes a transposed call a type error at the boundary
AccountId = NewType("AccountId", int)
Cents = NewType("Cents", int)

def transfer(from_id: AccountId, to_id: AccountId, amount: Cents) -> None: ...
```

**Loud failures can stay as runtime checks.** If a violation throws on contact (a malformed JSON parse, a missing column, a divide by zero), a runtime check with a good error message is often enough. Encoding it in the type system is not free; it costs API surface area, refactor load, and reader attention. Spend that budget where the failure would otherwise be silent.

```python
# Loud on its own: a malformed payload throws at the first access.
# No need to encode the row's shape into a refined TypedDict for every caller.
def parse_user(row: dict) -> User:
    return User(id=UUID(row["id"]), email=row["email"])
    # KeyError or ValueError surfaces immediately at the boundary;
    # the failure is impossible to miss, so the type system has nothing to add.
```

**Messy domains resist exhaustive encoding.** Real businesses have exceptions, grandfathered customers, regulatory carve-outs, and policies that change quarterly. The type system wants crispness; the domain does not provide it. Encode the spine in types; push the variation into data (see `PUSH_VARIATION_INTO_DATA`). A type model that tries to capture every business reality becomes a maintenance burden that fights every product change.

This complements `PRECISION_MATCHES_STABILITY`, which keys the encoding decision to volatility, and `SHAPE_NOT_INVARIANTS`, which limits encoding cost at interchange edges. Both ask different questions; this one asks: *what would a violation look like if we did nothing?*
