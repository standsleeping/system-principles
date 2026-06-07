---
id: PURITY_LICENSES_SURFACE
title: "Purity licenses public surface."
essence: "Hide a function for entanglement, not for size: pure, unit-covered functions may be public without limit, while a growing cluster of impure privates is a module waiting to be born."
related: [MODULES_HIDE_DECISIONS, FUNCTIONAL_PATTERNS, TYPES_AS_BOUNDARIES, WORKING_MEMORY_LIMIT, MOCKING_INDICATES_PROBLEMS]
---

The leading underscore makes hiding feel free. Nothing pushes back when you add one more helper, so a module swells into a junk drawer: privacy costs nothing to grant, the public surface never grows to embarrass you, and the design pressure that a widening interface would have applied never arrives. Size is not the smell. The missing forcing function is.

The real axis is purity, not count. A pure function has no hidden state, so exposing it leaks nothing and costs only a name; accept unboundedly many of them as public, each carrying its own unit coverage, and the module stays honest because every part is independently nameable, callable, and testable. Reserve privacy for what is genuinely entangled: functions that share mutable state, that enforce an invariant only together, or that are meaningful only partway through a protocol. Hide entanglement, never mere quantity.

```python
# A pure, general helper, hidden by reflex and called from three places.
# Strings in, string out: no state to leak, nothing to entangle.
def _classes(*parts: str) -> str:
    return " ".join(p for p in parts if p)

# The underscore buys nothing here. Lift it to the shared builder module,
# beside escape_attr and element, and give it the unit test it never had.
def classes(*parts: str) -> str:        # now public
    """Join non-empty class tokens into a class attribute value."""
    return " ".join(p for p in parts if p)
```

The deep-module objection — that many small public units yield shallow modules and information leakage — binds on stateful interfaces, where each exposed unit leaks a contract its callers come to depend on. Pure functions have no implementation state to leak, so that pressure never reaches them. Width is cheap when the surface is pure and expensive when the surface hides state; the same instinct that says "narrow the interface" for a stateful module says nothing about a wall of pure functions.

When privates accrete anyway, read the cluster as a missing module. A shared prefix or suffix across several helpers is the tell: the repeating name *is* the absent object's name. Extract it into its own unit with a public, tested surface rather than hiding one more method inside the host. The cure for too many privates is not better hiding; it is a new boundary.

```python
# A shared prefix is the tell, but read the cluster before you extract.

# Coherent recursion: one concern (model tree -> HTML) behind a narrow public
# face (render_document / render_frame / render_island). Leave these private.
def _render_node(node): ...
def _render_child(child): ...
def _render_root(frame): ...

# Junk drawer: separate concerns wearing one prefix. `_validate_*` is no
# implementation detail of its host; it is a Validator waiting to be born.
# The repeating name is the absent object's name. Extract it.
def _validate_user(user): ...
def _validate_order(order): ...
def _validate_payment(payment): ...
```
