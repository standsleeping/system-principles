# Polymorphism and Dispatch

This document provides balanced, principles-driven guidance for structuring polymorphic behavior and dispatch in this codebase. It complements `principles/design.md` (Logic, Values) and `principles/typing.md` (Separate Decisions from Behavior).

## Principles

### [PD1] Separate decisions from behavior.
Keep the choice of what to do (the decision) separate from how to do it (the behavior). Prefer data-driven dispatch tables (decisions as data) or interpreters, vs. embedding decisions in match statements or method overrides. Prefer representing domain as plain data with behavior in functions, and make time/identity explicit inputs rather than hidden globals.

Example (move decision out of control flow):

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

Example (multiple operations over same data):

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

Use when:
1. Domain logic has changing interpretations
2. Multiple operations exist over the same data
3. Runtime configuration or inspectable decisions are needed

Trade-offs:
1. Adding new variants requires updating each relevant map
2. No static checker to ensure coverage; combine with [PD7]

Guidance:
1. Pair dispatch maps with property-based tests to exercise invariants

### [PD3] Use in-place pattern matching only at boundaries or tiny, stable sets.
Pattern matching inside domain logic complects structure and behavior, increasing branching complexity. Keep it to parsing, serialization, or very small, stable cases.

Example (acceptable boundary match):

```python
# Parsing HTTP JSON payload to domain enum at the boundary
match payload.get("status"):
    case "active":
        status = UserStatus.ACTIVE
    case "suspended":
        status = UserStatus.SUSPENDED
    case _:
        return bad_request("invalid status")
```

Use when:
1. Boundary parsing/serialization
2. Tiny, stable sets; throwaway code; hot paths
3. Time/clock extraction at boundaries; pass time forward as data

Avoid:
1. Large matches that encode domain policy in core logic

### [PD4] Use à la carte polymorphism for extensibility.
Bias toward a data-first, interpreter-based style: model structure and policy as immutable data; implement operations as pure functions over that data; pass dispatch tables/registries explicitly (not via globals).

Use compositional, type-level encodings when you must allow many variants and many operations to evolve independently under strict modularity constraints.

In Python, both heavy type machinery and "clever" dynamic magic tend to complect concerns. Prefer simple values, explicit interpreters, and observable decisions you can diff, test, and recombine. Keep decisions as data and behavior orthogonal; make effects explicit at the edges.

Example (Python-friendly approximation):

```python
# Compose interpreters explicitly; avoid inheritance webs
class Eval(Protocol):
    def __call__(self, expr: "Expr") -> int: ...

class Pretty(Protocol):
    def __call__(self, expr: "Expr") -> str: ...

evaluators: list[Eval] = [eval_literals, eval_add, eval_mul]
prettiers: list[Pretty] = [pp_literals, pp_add, pp_mul]

def eval(expr: "Expr") -> int:
    for f in evaluators:
        expr = f(expr)
    return expr  # after passes
```

Use when:
1. Extensible language implementations, DSLs, or plugin systems
2. Many operations and variants must evolve independently

Avoid:
1. Inheritance webs where behavior is split across subclasses; prefer explicit composition/dispatch

### [PD5] Decisions as data.
Represent dispatch choices as values (e.g., dicts, maps). Decisions become inspectable, serializable, composable, and testable. This aligns with a functional core where data flows through transformations. Prefer configuration and error information as data to keep control declarative and handling composable.

Example (inspectable, testable decisions):

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

Example (avoid side effects in tables):

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
1. Place effects in actions at boundaries; keep handlers pure where feasible
2. Pass time/loggers/resources explicitly at the boundary; do not close over them in handlers

### [PD7] Manage exhaustiveness explicitly.
Since Python lacks total pattern exhaustiveness, use enums for variants, default handlers where appropriate, and validation tests that assert all enum members are mapped.

Guidance:
1. Use property-based tests to generate variant coverage and assert dispatch invariants
2. Prefer running core logic in a REPL/simulator without external I/O

Example (validate coverage in tests):

```python
def test_handlers_cover_all_statuses() -> None:
    assert set(handlers.keys()) == set(UserStatus)
```

## See Also

1. `principles/design.md` (Logic, Values)
2. `principles/typing.md` (Separate Decisions from Behavior)


