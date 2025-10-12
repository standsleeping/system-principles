# Typing

A boolean carries no information beyond its value. To use it meaningfully, you must remember where it came from and what it represents.

**A boolean indicates a coordination problem.** Say you write `process(data, retry=True)`. You're compressing an intention ("handle this with retry logic" let's say) into a **single bit**.

The function receives this bit, and must then decode: "the caller wants retry, so I'll use exponential backoff with these parameters." But what if you meant immediate retry? Or just one retry?

The boolean created a bottleneck: both sides must agree on what that bit means, and there's no way to verify the agreement or adapt as needs change.

This is called **[boolean blindness](https://www.cs.cmu.edu/~15150/previous-semesters/2012-spring/resources/lectures/09.pdf)**: when you test something and reduce the result to a single bit, you blind yourself to the information you just discovered, then spend effort trying to recover it later.

## Functions Return Evidence

Functions should return the information callers need to act, not just yes/no.

### [FRE1] Avoid returning bool.

Before writing `foo() -> bool`, ask: what information does the caller need after the check? Usually it's not just "yes/no" but the validated result, found value, or error details.

```python
# Enables blindness
def is_valid(x: str) -> bool: ...
def contains(d: dict, k: str) -> bool: ...

# Returns evidence
def validate(x: str) -> ValidInput | None: ...
def lookup(d: dict[K, V], k: K) -> V | None: ...
def try_process(item: Item) -> tuple[Result | None, list[Error]]: ...
```

### [FRE2] Acceptable bools.

Pure predicates where no additional context exists: `is_empty(list)`, `is_prime(n)`, `is_even(n)`.

## Types Carry Proofs

Branches don't create facts; they surface proofs the type checker can use. Validate once at boundaries, then carry proofs in types.

### [TCP1] Validate at boundaries.

Push validation to system edges. Don't scatter checks throughout the codebase.

```python
from typing import NewType

PositiveInt = NewType('PositiveInt', int)

def validate_positive(n: int) -> PositiveInt | None:
    return PositiveInt(n) if n > 0 else None

def divide_by(denominator: PositiveInt) -> float:
    return 100.0 / denominator  # No check needed—type carries proof
```

### [TCP2] Refined types propagate proofs.

Once validated, the type carries the proof forward. Functions accepting refined types don't need defensive checks.

Examples: `NonEmptyList[T]`, `VerifiedJwt`, `ParsedEmail`, `PositiveInt`.

### [TCP3] Pattern match to refine.

Pattern matching on sum types lets the compiler track what information is available in each branch:

```python
match grades.get("Alice"):
    case None:
        print("Not found")
    case grade:  # compiler knows grade is int
        print(f"Grade: {grade}")
```

For domain logic that changes frequently, consider data-driven dispatch instead (see `design.md` Logic, Values).

## Explicit State Modeling

Boolean fields in data models indicate missing domain concepts.

### [ESM1] Use enums over booleans.

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

### [ESM2] Include temporal information.

State-centric models lose temporal information. Track **when** facts became true.

```python
class User:
    status: UserStatus
    status_changed_at: datetime  # When did this become true?
```

See `design.md` (Events) for event sourcing and Entity-Attribute-Value-Time models.

## Separate Decisions from Behavior

Complecting structure (what states exist) with behavior (what to do) makes both harder to change independently.

### [SDB1] Data-driven dispatch for domain logic.

```python
# Pattern matching complects structure and behavior
match user.status:
    case UserStatus.ACTIVE:
        handle_active(user)
    case UserStatus.SUSPENDED:
        handle_suspended(user)

# Decisions as data
handlers = {
    UserStatus.ACTIVE: handle_active,
    UserStatus.SUSPENDED: handle_suspended,
}
result = handlers[user.status](user)
```

The second approach separates decisions (the dispatch table) from handlers (what to do), making operations easier to add and test independently.

See `design.md` (Logic, Values) for when to prefer this over in-place branching.
