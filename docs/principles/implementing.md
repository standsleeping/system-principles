# Implementing

These principles govern how we write code: patterns, style, and dispatch. Good implementation separates decisions from behavior and keeps code predictable.

## Polymorphism & Dispatch

The section addresses a fundamental question: how do we handle different cases in our code? We always prefer data-driven dispatch over traditional control flow (match statements, if/else chains, inheritance) where possible.

### [PD1] Separate decisions from behavior.

Don't embed "what to do" inside "how to do it." Instead of a match statement that both decides and executes, use a dispatch table (dictionary) that maps cases to handlers.

Avoid storing knowledge as control flow. Prefer data-driven dispatch tables (decisions as data). Represent the domain as plain data with behavior in functions, and make time/identity explicit inputs rather than hidden globals.

```python
# In-place decision (complects decision + behavior)
match user.status:
    case UserStatus.ACTIVE:
        return handle_active_user(user)
    case UserStatus.SUSPENDED:
        return handle_suspended_user(user)

# Decision as data (separation)
handlers = {
    UserStatus.ACTIVE: handle_active_user,
    UserStatus.SUSPENDED: handle_suspended_user,
}
return handlers[user.status](user)
```

### [PD2] Prefer data-driven dispatch for evolving domain logic.

When the set of operations grows or changes, dictionary-based (data-driven) dispatch cleanly isolates decisions, enabling straightforward extension and testing.

```python
# Two operations over UserStatus without touching the enum
to_label = {
    UserStatus.ACTIVE: "Active",
    UserStatus.SUSPENDED: "Suspended",
}

to_color = {
    UserStatus.ACTIVE: "green",
    UserStatus.SUSPENDED: "gray",
}

label = to_label[user.status]
color = to_color[user.status]
```

When you have multiple operations over the same set of variants, dispatch tables scale better. You can add to_label, to_color, to_permissions maps independently without touching the enum or other maps.

Use when:

1. Domain logic has changing interpretations
2. Multiple operations exist over the same data
3. Runtime configuration or inspectable decisions are needed

Trade-offs:

1. Adding new variants requires updating each relevant map.
2. No static checker to ensure coverage; combine with PD7.

### [PD3] Use in-place pattern matching only at boundaries or tiny, stable sets.

Pattern matching inside domain logic complects structure and behavior, increasing branching complexity. Keep it to parsing, serialization, or very small, stable cases.

```python
# Acceptable boundary match: parsing HTTP JSON payload to domain enum
match payload.get("status"):
    case "active":
        status = UserStatus.ACTIVE
    case "suspended":
        status = UserStatus.SUSPENDED
    case _:
        return bad_request("invalid status")
```

Use when:

1. Boundary parsing/serialization.
2. Tiny, stable sets; throwaway code; hot paths.
3. Time/clock extraction at boundaries; pass time forward as data.

Avoid:

1. Large matches that encode domain policy in core logic

### [PD4] Use a-la-carte polymorphism for extensibility.

Bias toward a data-first, interpreter-based style: model structure and policy as immutable data, and implement operations as pure functions over that data; pass dispatch tables/registries explicitly, don't hide them in globals or class hierarchies.

Use compositional, type-level encodings when you must allow many variants and many operations to evolve independently under strict modularity constraints.

In Python, both heavy type machinery and "clever" dynamic magic tend to complect concerns. Prefer simple values, explicit interpreters, and observable decisions you can diff, test, and recombine. Keep decisions as data and behavior orthogonal; make effects explicit at the edges.

```python
# Compose interpreters explicitly; avoid inheritance webs
class Eval(Protocol):
    def __call__(self, expr: "Expr") -> int: ...

class Pretty(Protocol):
    def __call__(self, expr: "Expr") -> str: ...

evaluators: list[Eval] = [eval_literals, eval_add, eval_mul]
prettiers: list[Pretty] = [pp_literals, pp_add, pp_mul]
```

Here Expr is a data structure (an AST representing expressions like Add(Lit(1), Lit(2))). The evaluators and prettiers are separate *interpreters*. Each walks the same data structure but produces different outputs.

Use when:

1. Extensible language implementations, DSLs, or plugin systems.
2. Many operations and variants must evolve independently.

Avoid:

1. Inheritance webs where behavior is split across subclasses; prefer explicit composition/dispatch.

### [PD5] Decisions as data.

Represent dispatch choices as values (e.g., dicts, maps). Decisions become inspectable, serializable, composable, and testable... just like data! This aligns with a functional core where data flows through transformations. Prefer configuration and error information as data to keep control declarative and handling composable.

```python
handlers = {
    UserStatus.ACTIVE: handle_active_user,
    UserStatus.SUSPENDED: handle_suspended_user,
}

# Can inspect for documentation or metrics
exposed = {k.name: v.__name__ for k, v in handlers.items()}

# Serialize configuration (e.g., to review diffs)
config = {k.value: v.__name__ for k, v in handlers.items()}
```

### [PD6] Keep dependencies out of dispatch tables.

Dispatch tables enumerate decisions and point to pure units or thin integrators. Do not perform I/O or side effects in the dispatch table itself.

```python
# Bad: side effects captured at decision site
handlers = {
    UserStatus.ACTIVE: lambda u: log_and_notify(handle_active_user(u)),
}

# Good: handlers are pure; effects happen at the action boundary
handlers = {
    UserStatus.ACTIVE: handle_active_user,
}

result = handlers[user.status](user)
log_result(result)
notify(result)
```

Guidance:

1. Place effects in actions at boundaries; keep handlers pure where feasible.
2. Pass time/loggers/resources explicitly at the boundary; do not close over them in handlers.

### [PD7] Manage exhaustiveness explicitly.

Since Python lacks total pattern exhaustiveness, use enums for variants, default handlers where appropriate, and validation tests that assert all enum members are mapped.

```python
def test_handlers_cover_all_statuses() -> None:
    assert set(handlers.keys()) == set(UserStatus)
```

Guidance:

1. Use property-based tests to generate variant coverage and assert dispatch invariants.
2. Prefer running core logic in a REPL/simulator without external I/O.

### [PD8] Data-driven dispatch for domain logic.

Complecting structure (what states exist) with behavior (what to do) makes both harder to change independently.

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

## Style Rules

### [SR1] Functional programming patterns.

- Prefer functions and composition over classes and inheritance.
- Functions are almost always pure and have no side effects.
- Functions follow SRP and are small/focused.
- Functions always have clear input and output types.
- Functions never mutate their arguments.

