# Modeling

These principles dictate how we think about data, types, and state. Good models make illegal states unrepresentable and carry proofs forward in types.

## Values

### [VL1] Depend on values, not behaviors.

Our code should always depend on values (i.e. data), not behaviors (i.e. code):

1. "Values" are just data, or anything that has no behavior.
2. Replace method calls with data passing between components.
3. Components should transform values instead of calling each other.
4. Building blocks should agree on data shape, not on implementation.
5. Decisions should live in one place, and dependencies in another.
6. Data is flexible: it can travel across functions, threads, or networks.
7. Every value is a potential message, and messages allow concurrency.
8. When components only transform values, they can run in parallel.

### [VL2] State entangles values and time.

Stateful approaches are squarely at odds with simple designs, because by definition, state entangles values and time.

## Events

### [EV1] Store facts with time.

Hickey points out that the Resource Description Framework lacks a time component. "Sally likes pizza..." _as of when, exactly?_

Store facts as 5-tuples:

1. **Entity**. Who or what (e.g. Sally).
2. **Attribute**. The property (e.g. likes).
3. **Value**. The actual value (e.g. pizza).
4. **Time**. When this fact was asserted.
5. **Operation**. Are we adding or retracting?

This temporal model means the user can:

1. Track the full history of changes.
2. Query the database "as of" any point in time.
3. Know when facts became true or stopped being true.

## Effects

### [EF1] Capture time-dependent results explicitly.

Effects are complex; they entangle _who_ and/or _what_ and/or _how_ with **when**. When the _time you run the code_ can impact what the outcome is, you have effects, and thus, complexity.

In some cases this is unavoidable. In the cases where it is, you must take special care. Use a result structure (`EffectResult`) to store the results of any operation where the _time you run the code_ can impact what the outcome is.

## Type Design

### [TD1] Make illegal states unrepresentable.

1. Move "Any" types as close as possible to the dependency you can't control.
2. Transform "Any" into meaningful types as soon as possible.
3. Move try/except as close to the dependency you can't control.
4. Convert errors into result types and design for handling them.
5. Shrink the representable state space down to the set of valid states.
6. Input parsing is not business logic. Keep them distinct!

### [TD2] Chase runtime checks upstream.

Chase runtime checks all the way upstream. Ask at every boundary line what conditions upstream allow for this runtime check to be necessary. If you chase it all the way upstream to the interface, you'll end up with a more clear, more explicit, easier to use API for your users. You have successfully made invalid states unrepresentable.

### [TD3] Strengthen inputs, don't weaken outputs.

- Prefer making functions total by strengthening parameter types (e.g., `NonEmptyList[T]`) rather than weakening return types to `| None`.
- Parse into precise types at the boundary or immediately at branch entry when a branch needs stronger invariants.
- Build proofs once and carry them forward in types; avoid repeating boolean checks.

### [TD4] Types as module boundaries.

Each package's public interface is defined primarily through its data types.

Development follows a type-first workflow, where data structures and types that model the domain are often designed first, with pure functions that transform these types are implemented next. Type signatures guide and constrain implementations.

The prohibition on circular dependencies is reinforced by our type system. Modules can only depend on types from their dependencies, creating a clear, unidirectional flow.

### [TD5] Use enums over booleans.

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

### [TD6] Include temporal information.

State-centric models lose temporal information. Track **when** facts became true.

```python
class User:
    status: UserStatus
    status_changed_at: datetime  # When did this become true?
```

See Events (EV1) for event sourcing and Entity-Attribute-Value-Time models.

### [TD7] Match type precision to stability.

Types exist on a precision spectrum—from `Any` to refined types like `EmailAddress`. Precision should match stability:

- **Loose types** belong near volatility: external boundaries we can't control, or rapidly-changing areas where locking down prematurely would cause rework.
- **Precise types** belong in stable domains where invariants matter and understanding has solidified.

Track where your types fall on this spectrum. If a loose type has drifted into the domain core, tighten it. If a precise type sits at a volatile boundary, you may be over-specifying.

## Type Patterns

Functions should return the information callers need to act, not just yes/no. Types carry proofs forward.

### [TP1] Avoid returning bool.

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

### [TP2] Acceptable bools.

Pure predicates where no additional context exists: `is_empty(list)`, `is_prime(n)`, `is_even(n)`.

### [TP3] Validate at boundaries.

Push validation to system edges. Don't scatter checks throughout the codebase.

```python
from typing import NewType

PositiveInt = NewType('PositiveInt', int)

def validate_positive(n: int) -> PositiveInt | None:
    return PositiveInt(n) if n > 0 else None

def divide_by(denominator: PositiveInt) -> float:
    return 100.0 / denominator  # No check needed—type carries proof
```

### [TP4] Refined types propagate proofs.

Once validated, the type carries the proof forward. Functions accepting refined types don't need defensive checks.

Examples: `NonEmptyList[T]`, `VerifiedJwt`, `ParsedEmail`, `PositiveInt`.

### [TP5] Pattern match to refine.

Pattern matching on sum types lets the compiler track what information is available in each branch:

```python
match grades.get("Alice"):
    case None:
        print("Not found")
    case grade:  # compiler knows grade is int
        print(f"Grade: {grade}")
```

For domain logic that changes frequently, consider data-driven dispatch instead (see Implementing > Polymorphism & Dispatch).

### [TP6] Fix the upstream type.

If you need to cast, it means the upstream type is wrong or too loose. Fix the source definition.

### [TP7] Use runtime narrowing.

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

### [TP8] Parse into stronger types.

Validation returns booleans; parsing returns stronger types that carry the proof forward.

- Translators SHOULD build context-free proofs: presence/shape, normalization, simple formats (UUID, ISO date, email syntax), and cross-field form invariants that require no I/O (e.g., password == confirm).
- Translators MUST NOT implement policy/stateful checks: uniqueness, invites, quotas/rate limits, time-based rules, or config-driven policies (e.g., password strength).
- Prefer strengthening inputs over weakening outputs: construct proof-carrying values (e.g., `EmailAddress`, `ConfirmedPassword`) and return a typed `...Input` object on success.
- Validators should look like parsers: return proof-carrying values, not booleans.

## Type Syntax

We always follow modern Python typing conventions and avoid legacy typing patterns.

### [TS1] Built-in generic types.

- Use: `list[T]`, `dict[K, V]`, `set[T]`, `tuple[T, ...]`
- Avoid: `List[T]`, `Dict[K, V]`, `Set[T]`, `Tuple[T, ...]`

### [TS2] Union syntax.

- Use: `T | None`, `str | int`, `list[str] | dict[str, int]`
- Avoid: `Optional[T]`, `Union[str, int]`

### [TS3] Generic classes.

- Use: `class Container[T]:` (PEP 695 syntax)
- Avoid: `T = TypeVar('T')` + `class Container(Generic[T]):`

### [TS4] Import minimization.

- Only import from `typing` when necessary (e.g., `Any`, `Protocol`, `Literal`)
- Never import: `List`, `Dict`, `Set`, `Tuple`, `Optional`, `Union`, `Generic`, `TypeVar`
- Built-in types and union syntax eliminate most `typing` imports
- Use `type` statement for type aliases instead of `TypeAlias`

### [TS5] Domain type safety.

- Never allow `dict[str, Any]` in domain layers.
- Instead of raising exceptions in domain logic, use Result types.
- Result types make success and failure explicit.
- Handle errors explicitly, so all possible outcomes are visible in the type signature.
- Domain functions should never throw, making them predictable.
- Test both success and failure paths without exception handling.

## Data Interchange

Distinguish between how data is represented *inside* your domain vs. how it is represented *at the boundaries*.

### [DDI1] Use TypedDict for interchange.

**Use for**: JSON blobs, API requests/responses, database rows, configuration files.

`TypedDict` is a "shape" (structural type). It says "this dictionary has these keys".
- **Pros**: Serializes natively to JSON. Compatible with external systems that speak "dict".
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
