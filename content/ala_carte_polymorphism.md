---
id: ALA_CARTE_POLYMORPHISM
title: "Use a-la-carte polymorphism for extensibility."
summary: "Bias toward a data-first, interpreter-based style: model structure and policy as immutable data, and implement operations as pure functions over that data; pass dispatch tables/registries explicitl..."
---

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