---
id: TD4
title: "Types as module boundaries."
summary: "Each package's public interface is defined primarily through its data types."
---

Each package's public interface is defined primarily through its data types.

Development follows a type-first workflow, where data structures and types that model the domain are often designed first, with pure functions that transform these types are implemented next. Type signatures guide and constrain implementations.

The prohibition on circular dependencies is reinforced by our type system. Modules can only depend on types from their dependencies, creating a clear, unidirectional flow.