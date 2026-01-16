# Structuring

These principles govern how we organize code: architecture, boundaries, and modules. Good structure isolates change, makes dependencies explicit, and keeps the system navigable.

## State & Architecture

### [SA1] Stateless design.

All computations are pure. No in-memory state anywhere.

### [SA2] Event sourcing.

Events are living documentation of system behaviors. Note that all "entities" or objects that appear as nouns are almost always _composed_ from streams of events.

### [SA3] Database as truth.

All reads go through SQL queries. All writes append events.

### [SA4] Traceability.

Easy audit trails are composed via the database. Composing a set of SQL queries to create a full picture of what happened is how 99% of bugs are found.

### [SA5] Time travel.

All state is rewindable via events. Think accounting and ledgers. No mutations!

## Project Structure

### [PS1] Data structures at root.

Types and dataclasses are placed at the package root level, at the same level as the `functions` folder. This placement reflects their fundamental importance. In this architecture, data structures are of the utmost importance as they define the vocabulary of the system, help establish module boundaries, guide function implementations, and ensure type safety across module boundaries.

### [PS2] Functions in subdirectory.

Functions, wherever possible, are kept in the package's `functions` folder. These functions operate on the well-defined types, with their signatures serving as executable documentation of the transformations they perform.

### [PS3] The 1:1:1 Rule.

We maintain a strict 1:1 correspondence between:

1. **Data and files**: One data structure per file.
2. **Functions and files**: One function per file.
3. **Files and tests**: One file, one test suite.

Union types and their constituent result types may be grouped together in a single file when they form a cohesive set of related outcomes for a specific operation.

Example: `RegistrationResult = RegistrationSuccess | AlreadyExists | InvalidAppData`.

At the same level as the functions and data, there may also exist subpackages with semantically meaningful names, themselves having the same data/function structure as the subpackage they are in.

## Code Building Blocks

Files will contain one (and only one, per file) of the following simple "building block" code types. This is the most commonly violated architectural rule; be rigorous in your assessment as to whether the code you produce adheres to these standards.

We avoid combinatorial explosion (2^n paths for n branches) through careful design that makes invalid states unrepresentable and maintains a clear separation between actions, integrators, and units.

### [CB1] Actions.

Accept a user's request, or specification of work, and return a result object. Characteristics:

- Entry point at a boundary: HTTP handler, CLI command, job runner, or scheduler tick.
- Accepts a user's request/specification and returns a typed result object.
- Uses translator functions to parse inputs and serialize outputs.
- Orchestrates units and integrators; contains no domain decisions itself.
- Performs side effects ONLY at boundaries.
- Valid boundary effects: transactions, appends events, enqueues jobs, logs/metrics/traces.
- Uses explicit control flow with early returns; avoids complex branching.
- Never raises to signal domain failures; returns typed results instead.

### [CB2] Integrators.

Assemble a complex structure or data type. They "glue together" different behaviors and produce composite data structures. Characteristics:

- Calls other units and/or integrators.
- Sole purpose is to assemble complex return types and data structures.
- Delegates to other unit/integrator calls.
- Never makes semantically meaningful decisions: always delegates to other integrators/units.
- Can use if/else but ONLY to conditionally (i.e. early) return its return type.
- Simple integration tests: one test function/suite-of-functions for each `return`.
- Size of test suite is proportional to variety of return conditions.
- Tests NEVER mock or stub user code; always RUNS code that integrator depends on.

### [CB3] Units.

Implement a simple, testable decision or calculation that the code makes. They are pure functions. Characteristics:

- Simple data types in and out.
- Pure functions, no imports, no dependencies, no side effects.
- Tested simply: all possible return values are covered in unit-like assertions.

### [CB4] Translators.

Translator functions (either units or integrators) sit at system or package boundaries, and can be either units or integrators, depending on the context.

**Translator as Unit:**

- Direct transformation of `dict[str, Any]` to domain types using only built-in functions.
- No dependencies: only standard library functions (uuid.UUID, datetime.fromisoformat, etc.).
- No imports: No calls to other application functions.
- Example: Converting string to UUID, parsing ISO datetime, basic type coercion.

**Translator as Integrator:**

- Composed conversion: Calls other units/integrators to perform complex translations.
- Has dependencies: Uses validation units, parsing integrators, or lookup functions.
- Assembles results: Combines multiple conversion operations into domain objects.
- Example: Converting request data that requires validation against existing domain rules.

**Both types:**

- Only convert: Transform external data to domain types.
- Only validate boundaries: Handle conversion errors and return appropriate error responses.
- Pass, don't execute: Return properly typed domain objects for other functions to use.
- No domain operations: Never call domain functions directly, leave that to the calling context.

## Boundary Types

A critical aspect of hexagonal architecture is proper boundary management between layers.

### [BT1] TypedDict at boundaries.

Never use `dict[str, Any]` or `dict[str, object]`.

- **At boundaries**: Use `TypedDict` to model JSON structure precisely. It provides type checking, autocomplete, and documentation while remaining a plain dict at runtime.
- **In domain**: Use `dataclasses` for rich domain objects.
- **Migration**: If you find `dict[str, Any]`, replace it with a `TypedDict` definition immediately.

When `dict[str, Any]` types propagate deeper into the codebase beyond initial entry points, boundaries are not properly defined. This causes:

- **Loss of type safety**: No IDE support, no compile-time checks, runtime errors.
- **Domain modeling failure**: Domain objects represent business concepts.
- **Scattered validation**: Without proper deserialization, validation spreads everywhere.
- **Coupling to transport**: Domain logic becomes coupled to JSON structure.

### [BT2] Translator functions.

Use translator functions as the standard pattern for converting external data (JSON, HTTP requests) into domain objects. These functions have a single, narrow responsibility:

- **Pure conversion**: Transform `dict[str, Any]` from requests into properly typed domain objects.
- **Boundary validation**: Handle conversion errors with appropriate HTTP responses.
- **No domain logic**: Never perform domain operations, only convert types and pass to domain!

### [BT3] Pure conversion only.

Translators must transform `dict[str, Any]` from requests into properly typed domain objects, handle conversion errors with appropriate HTTP responses, and never perform domain operations (only convert types and pass to domain layer).

## Translators

Data crosses boundaries constantly: from JSON to domain objects, SQL rows to entities, one context to another. Each crossing is a potential source of type errors and coupling.

**Translators** are pure conversion functions that transform data at architectural boundaries. They convert representations without performing business logic, ensuring your domain stays decoupled from external formats.

### [TL1] Translators only convert, never operate.

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

### [TL2] Return explicit error values.

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

### [TL3] Validate structure, not business rules.

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

### [TL4] Unit translators are self-contained.

A unit translator converts data using only built-in functions. No external dependencies, no calling other translators.

```python
# Unit translator: self-contained conversion
def parse_timestamp(value: str) -> tuple[TranslatorError | None, datetime | None]:
    try:
        return None, datetime.fromisoformat(value)
    except ValueError as e:
        return TranslatorError(f"Invalid timestamp: {e}"), None

# Unit translator: simple type transformation
def parse_uuid(value: str) -> tuple[TranslatorError | None, uuid.UUID | None]:
    try:
        return None, uuid.UUID(value)
    except ValueError:
        return TranslatorError(f"Invalid UUID: {value}"), None
```

### [TL5] Integrator translators compose unit translators.

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

### [TL6] Chain translators with explicit error propagation.

When composing translators, propagate errors explicitly. Don't hide failures.

```python
# Chaining translators
class TranslatorChain[T1, T2, T3]:
    def __init__(
        self,
        first: callable[[T1], tuple[TranslatorError | None, T2 | None]],
        second: callable[[T2], tuple[TranslatorError | None, T3 | None]]
    ):
        self.first = first
        self.second = second

    def __call__(self, input_data: T1) -> tuple[TranslatorError | None, T3 | None]:
        err, intermediate = self.first(input_data)
        if err:
            return err, None

        return self.second(intermediate)

# Usage
json_to_domain = TranslatorChain(
    first=parse_json_to_dict,
    second=dict_to_user_command
)
```

### [TL7] One translator per boundary type.

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

### [TL8] Domain → External uses domain language.

When translating domain objects to external formats, use domain concepts in the translator. Don't leak external concerns into the domain.

```python
# Domain → External API
def domain_to_api_translator(
    order: Order
) -> tuple[TranslatorError | None, OrderApiDict | None]:
    try:
        return None, {
            "orderId": str(order.id),
            "customerEmail": order.customer.email,
            "items": [
                {
                    "sku": item.product.sku,
                    "quantity": item.quantity,
                    "priceInCents": int(item.price * 100)
                }
                for item in order.items
            ],
            "totalInCents": int(order.total * 100)
        }
    except AttributeError as e:
        return TranslatorError(f"Missing required attribute: {e}"), None
```

### [TL9] Cross-domain translators enforce boundary rules.

When translating between domain contexts, enforce the boundary's invariants. This is still structural validation, not business logic.

```python
# Billing context → Shipping context
def billing_to_shipping_translator(
    billing_order: BillingOrder
) -> tuple[TranslatorError | None, ShippingRequest | None]:
    # Structural requirement: shipping needs paid orders
    if billing_order.status != "PAID":
        return TranslatorError("Order must be paid before shipping"), None

    return None, ShippingRequest(
        order_ref=billing_order.id,
        recipient=Address(
            name=billing_order.customer_name,
            street=billing_order.delivery_address,
            postal_code=billing_order.postal_code
        ),
        items=[
            ShippingItem(sku=item.sku, quantity=item.qty)
            for item in billing_order.line_items
        ]
    )
```

### [TL10] Inject translators into boundary components.

Repositories and handlers shouldn't know about external formats. Inject translators to handle conversion.

```python
# Repository uses injected translator
class UserRepository:
    def __init__(
        self,
        db: Database,
        translator: callable[[dict], tuple[TranslatorError | None, User | None]]
    ):
        self.db = db
        self.translator = translator

    async def get(self, user_id: uuid.UUID) -> User | None:
        row = await self.db.fetch_one("SELECT * FROM users WHERE id = ?", user_id)
        if not row:
            return None

        err, user = self.translator(dict(row))
        if err:
            raise TranslationException(err.message)

        return user
```

### [TL11] Use translators in request handlers.

Translate incoming requests to domain commands before passing to handlers.

```python
async def handle_request[TCommand](
    request: Request,
    translator: callable[[Request], tuple[TranslatorError | None, TCommand | None]],
    handler: CommandHandler[TCommand]
) -> Response:
    err, command = await translator(request)
    if err:
        return Response({"error": err.message}, status=400)

    result = await handler.handle(command)
    return Response({"result": result}, status=200)
```

### [TL12] Keep translator error types consistent.

Use a standard error type across all translators. This makes error handling uniform.

```python
from dataclasses import dataclass

@dataclass
class TranslatorError:
    """Standard translator error"""
    message: str
    code: str = "TRANSLATION_ERROR"

# All translators use the same error type
type TranslatorFunction[TInput, TOutput] = (
    callable[[TInput], tuple[TranslatorError | None, TOutput | None]]
)
```
