# Design

Systems model the world. Our understanding of the world changes over time, and the design of the system must react in turn.

No project ever begins with complete information. In fact, complete information is never ultimately reached; we are never finished with our design.

## Boundaries

What *distinct sources* of change are we listening for, and reacting to, to deepen our understanding of the domain we are modeling?

Let's call these wellsprings of change "Parnas Points."

We will design the building blocks of our system around these sources of change.

Per Gall, we must always start simple, and be attentive to changes that add _useful complexity_ to our model of the world over time. Per Parnas, we must focus our designs such that the structure of our system reflects the sources of change. Per Hickey, we allow only two types of change: _providing more_ and _requiring less_. This approach to design allows the system to evolve over time in a stable way, and makes breaking changes nearly impossible.

A module isn't a subroutine. It's a decision, an assumption, or a source of change, hidden behind an interface which protects the module's users from that source of change.

Your design is not your workflow. The actual running code will use many modules, as needed, in a flexible way. We create simple systems by composing simple components together, each representing a concept that stands by itself, and that we can change in isolation.

Our framework for design:

1. Identify assumptions or decisions that might change as we learn.
2. Hide each behind a boundary.
3. The goal is not to model execution, or to model entities.
4. The goal is to **isolate sources of change**.
5. We seek to couple things that change together.
6. Decouple things that change for different reasons, at different times.
7. Tease apart the who, what, when, where, why, and how.

## Values

Our code should always depend on values (i.e. data), not behaviors (i.e. code):

1. "Values" are just data, or anything that has no behavior.
2. Replace method calls with data passing between components.
3. Components should transform values instead of calling each other.
4. Building blocks should agree on data shape, not on implementation.
5. Decisions should live in one place, and dependencies in another.
6. Data is flexible: it can travel across functions, threads, or networks.
7. Every value is a potential message, and messages allow concurrency.
8. When components only transform values, they can run in parallel.

Stateful approaches are squarely add odds with simple designs, because by definition, state entangles values and time.

## Abstraction

Abstraction means "to draw away" or "to pull apart" and is more about **entanglement** than **hiding**. It is a skill that you sharpen by learning to see intertwined things that could otherwise be independent. The word we use for improving abstractions in software is *simplification*.

The best approaches we have for simplification in practice:

1. Untangle who, what, when, where, why, and how.
2. Identify components that depend on behaviors, and redesign them to depend on data.

To "simplify" something is to _reduce interleaving_ of its components or concerns. To the extent that interleaving can be identified, and thus reduced and therefore compared (before vs. after), "simplicity" is _an objective measurement_ and thus has less to do with aesthetics or personal preferences and more to do with tools and repeatable processes. This conception of objective simplicity is relatively new in computing, so the tools for measuring it are underdeveloped.

**Simplicity is measured by ease of reassembly.** My working description of achieving simplicity in practice: "pull the system apart, and build it back together again, many times over."

## Cognitive Load

An intuitive measure of complexity is _cognitive load_. We can only simplify things we understand.

We have limited working memory, and can only hold a few things together in our minds at one time. Intertwined things must often be considered together in order to understand the whole.

The cognitive burden is combinatorial and multiplies with each additional slot taken in working memory during the process of understanding.

A straightforward way to start pulling things apart: ask questions and *assign names* to the following *aspects* of a program: who, what, when, where, why, and how.

## Change

Design and change are closely related concepts:

1. We allow two types of change: _providing more_ and _requiring less_.
2. We call these change types _accretion_ and _relaxation_.
3. Never mutate or update. Create new things with new names.
4. The old and new must coexist together.
5. Removal of the old only happens when adoption of the new reaches 100%.

"Providing more" means:

1. Strenghtening postconditions.
2. Returning more information.
3. Providing richer data structures.
4. Adding guarantees.

"Requiring less" means:

1. Relaxing preconditions.
2. Accepting broader inputs.
3. Requiring fewer inputs.

If providing more, ask:

1. What data structure(s) capture the "more" we are providing?
2. What functions depend on the new data structure?

If requiring less, ask:

1. What data constraints can we remove or make optional?
2. What functions need to be updated to handle the broader input space?
3. What default values or behaviors handle the now-optional cases?

## Events

Hickey points out that the Resource Description Framework lacks a time component.

"Sally likes pizza..." _as of when, exactly?_

We can address this limitation by storing facts as 5-tuples:

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

Effects are complex; they entangle _who_ and/or _what_ and/or _how_ with **when**.

the _time you run the code_ can impact what the outcome is, you have effects, and thus, complexity.

In some cases this is unavoidable. In the cases where it is, you must take special care.

Use a result structure (`EffectResult`) to store the results of any operation where the _time you run the code_ can impact what the outcome is.

## Logic

Each `if` encodes an assumption and a decision.

Local branching couples code to context. It hardens behavior and raises change cost.

Pull `if` statements toward the places where related decisions live and change together.

The higher you hoist them, the more declarative the program. Hoisted decisions collapse into rule sets. Higher still, rule sets become configuration: inputs to your program.

Treat decisions as data wherever possible. This defers commitment and reduces code paths.

An `if` partitions the state space. **The predicate is a fact derived from an underspecified model**.

Encode those facts in the model early, with types, invariants, or simple state machines.

Examples of `if` complexity:

1. `if (isValid)` for **data** (invalid states).
2. `if (shouldDoX)` for **benavior** (conditional execution).
3. `if (currentState === X)` for **flow** (sequencing/coordination).
4. `if (format === 'json')` for **transformation** (data reshaping).

Move logic into rules, not code paths, and invalid states will start to disappear.

## Types

Make illegal states unrepresentable:

1. Move "Any" types as close as possible to the dependency you can't control.
2. Transform "Any" into meaningful types as soon as possible.
3. Move try/except as close to the dependency you can't control.
4. Convert errors into result types and design for handling them.
5. Shrink the representable state space down to the set of valid states.
6. Input parsing is not business logic. Keep them distinct!

Chase runtime checks all the way upstream. Ask at every boundary line what conditions upstream allow for this runtime check to be necessary. If you chase it all the way upstream to the interface, you'll end up with a more clear, more explicit, easier to use API for your users. You have successfully made invalid states unrepresentable.

### Strengthen inputs, don't weaken outputs

- Prefer making functions total by strengthening parameter types (e.g., `NonEmptyList[T]`) rather than weakening return types to `| None`.
- Parse into precise types at the boundary or immediately at branch entry when a branch needs stronger invariants.
- Build proofs once and carry them forward in types; avoid repeating boolean checks.