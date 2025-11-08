# Translators

Data crosses boundaries constantly: from JSON to domain objects, SQL rows to entities, one context to another. Each crossing is a potential source of type errors and coupling.

**Translators** are pure conversion functions that transform data at architectural boundaries. They convert representations without performing business logic, ensuring your domain stays decoupled from external formats.

## Pure Boundary Conversion

Translators exist solely to convert data at system boundaries. They validate structure, transform types, and return errors when conversion fails.

### [PBC1] Translators only convert, never operate.

A translator transforms data representations. It never performs business logic, makes decisions, or triggers side effects.

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

### [PBC2] Return explicit error values.

Translators return conversion errors as values, not exceptions. Use tuple returns: `(Error | None, Result | None)`.

```python
# Good: errors as values
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

# Bad: exceptions for control flow
def db_row_to_domain_translator(row: dict[str, object]) -> User:
    if not row:
        raise ValueError("Empty row")  # Forces exception handling

    return User(id=uuid.UUID(row["id"]), email=row["email"])
```

### [PBC3] Validate structure, not business rules.

Translators check that data has the right shape and types. Domain validators check business rules.

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

## Translator Composition

Complex conversions are built by composing simple translators. Keep unit translators pure and dependency-free; use integrator translators to orchestrate.

### [TC1] Unit translators are self-contained.

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

### [TC2] Integrator translators compose unit translators.

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

### [TC3] Chain translators with explicit error propagation.

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

## Boundary-Specific Translators

Each system boundary needs its own translator type. Network translators handle HTTP, database translators handle rows, domain translators handle context switching.

### [BST1] One translator per boundary type.

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

### [BST2] Domain → External uses domain language.

When translating domain objects to external formats, use domain concepts in the translator. Don't leak external concerns into the domain.

```python
# Domain → External API
def domain_to_api_translator(
    order: Order
) -> tuple[TranslatorError | None, dict[str, object] | None]:
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

### [BST3] Cross-domain translators enforce boundary rules.

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

## Integration Patterns

Translators integrate with repositories, handlers, and other boundary components. Inject them as dependencies.

### [IP1] Inject translators into boundary components.

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

### [IP2] Use translators in request handlers.

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

### [IP3] Keep translator error types consistent.

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

## Summary

Translators convert data at boundaries. They validate structure, transform types, and return errors as values. They never perform business logic or access external systems.

**Key principles:**

- **[PBC1]** Translators only convert, never operate
- **[PBC2]** Return explicit error values
- **[PBC3]** Validate structure, not business rules
- **[TC1]** Unit translators are self-contained
- **[TC2]** Integrator translators compose unit translators
- **[TC3]** Chain translators with explicit error propagation
- **[BST1]** One translator per boundary type
- **[BST2]** Domain → External uses domain language
- **[BST3]** Cross-domain translators enforce boundary rules
- **[IP1]** Inject translators into boundary components
- **[IP2]** Use translators in request handlers
- **[IP3]** Keep translator error types consistent