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

## No Casting

Casting (`cast(Type, val)`) tells the type checker to ignore reality and trust you. It silences valid warnings and hides bugs.

### [NC1] Fix the upstream type.

If you need to cast, it means the upstream type is wrong or too loose. Fix the source definition.

### [NC2] Use runtime narrowing.

If the type is loose (`Any`, `object`, or a union) because it comes from an external source, use `isinstance()` checks to narrow it. The type checker will then "know" the type is correct in that branch.

```python
# Bad: Silencing the checker
val = cast(str, data["name"])

# Good: Runtime verification
val = data.get("name")
if isinstance(val, str):
    # val is known to be str here
    process(val)
```

## Domain Data vs Interchange Data

Distinguish between how data is represented *inside* your domain vs. how it is represented *at the boundaries*.

### [DDI1] Use TypedDict for interchange.

**Use for**: JSON blobs, API requests/responses, database rows, configuration files.

`TypedDict` is a "shape" (structural type). It says "this dictionary has these keys".
- **Pros**: Serializes natively to JSON. compatible with external systems that speak "dict".
- **Cons**: No methods, no properties, no invariants (a negative radius is valid int), clumsy for deep nesting.
- **Feature**: Can be `total=False` (partial), useful for patch requests or sparse data.

```python
class UserPayload(TypedDict):
    id: str
    email: str
    # No guarantees that email is valid, just that it's a string.
```

### [DDI2] Use Dataclasses for domain.

**Use for**: Business entities, value objects, internal logic.

`Dataclasses` are "types" (nominal type). They say "this is a User".
- **Pros**: Can enforce invariants (`__post_init__`), have properties (`@property`), methods, and identity.
- **Cons**: Need serialization steps to leave the system.
- **Feature**: `frozen=True` makes them hashable and immutable, perfect for passing around safely.

```python
@dataclass(frozen=True)
class User:
    id: UUID
    email: EmailAddress  # Refined type!
    
    @property
    def domain(self) -> str:
        return self.email.split("@")[1]
```

### [DDI3] Translators bridge the gap.

Don't let `TypedDict`s leak deep into the domain. Parse them into Dataclasses at the boundary.

**Input Flow**: `External JSON` → `TypedDict` → `Translator` → `Dataclass`
- The translator validates structure (`TypedDict`) and parses values (str → UUID).
- The Dataclass constructor guarantees the object is valid.

**Output Flow**: `Dataclass` → `Translator` → `TypedDict` → `External JSON`
- The translator converts rich types (UUID) back to primitives (str).
- The `TypedDict` ensures the output shape matches the API contract.

## *Parse* into stronger types (don't *validate* to booleans)

Validation returns booleans; parsing returns stronger types that carry the proof forward.

Strengthen inputs rather than weakening outputs, and carry proofs forward in types.

- Prefer strengthening inputs: instead of `foo(xs: list[T]) -> T | None`, use `foo(xs: NonEmptyList[T]) -> T`.
- Parse at the edge (or at the branch) into types that encode form-level invariants; avoid scattering boolean checks.
- Push proof upward, but no further: construct the most precise type needed for the next computation step; don’t over-parse.
- Validators should look like parsers: return proof-carrying values, not booleans.

Naming guidance (keep it simple):
- Raw external: `...Request` or `...FormData`
- Parsed and safe for domain: `...Input`
- Proof-carrying parts: `EmailAddress`, `ConfirmedPassword`, `AcceptedTerms`

Example signature shift:
```python
# Before: weak output, callers handle None
def head(xs: list[T]) -> T | None: ...

# After: strong input, total function
def head(xs: NonEmptyList[T]) -> T: ...
```

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
