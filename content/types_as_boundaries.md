---
id: TYPES_AS_BOUNDARIES
title: "Types as module boundaries."
essence: "Design the types first; their signatures guide and constrain every implementation that follows."
---

Each package's public interface is defined primarily through its data types.

Development follows a type-first workflow, where data structures and types that model the domain are often designed first, with pure functions that transform these types are implemented next. Type signatures guide and constrain implementations.

The prohibition on circular dependencies is reinforced by our type system. Modules can only depend on types from their dependencies, creating a clear, unidirectional flow.