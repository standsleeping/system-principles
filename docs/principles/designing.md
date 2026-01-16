# Designing

Systems model the world. Our understanding of the world changes over time, and the design of the system must react in turn.

No project ever begins with complete information. In fact, complete information is never ultimately reached; we are never finished with our design.

## Boundaries

What *distinct sources* of change are we listening for, and reacting to, to deepen our understanding of the domain we are modeling?

Let's call these wellsprings of change "Parnas Points."

We will design the building blocks of our system around these sources of change.

### [BD1] Start simple, add *useful* complexity.

Per Gall, we must always start simple, and be attentive to changes that add _useful complexity_ to our model of the world over time.

### [BD2] Structure reflects sources of change.

Per Parnas, we must focus our designs such that the structure of our system reflects the sources of change.

### [BD3] Only two types of change: provide more, require less.

Per Hickey, we allow only two types of change: _providing more_ and _requiring less_. This approach to design allows the system to evolve over time in a stable way, and makes breaking changes nearly impossible.

### [BD4] A module is a hidden decision.

A module isn't a subroutine. It's a decision, an assumption, or a source of change, hidden behind an interface which protects the module's users from that source of change.

### [BD5] Design is not workflow.

Your design is not your workflow. The actual running code will use many modules, as needed, in a flexible way. We create simple systems by composing simple components together, each representing a concept that stands by itself, and that we can change in isolation.

### [BD6] Framework for design.

1. Identify assumptions or decisions that might change as we learn.
2. Hide each behind a modular boundary.
3. The goal is not to model _execution_, nor to model _entities_.
4. The goal is to **isolate sources of change**.
5. We seek to couple things that change together.
6. We try to decouple things _that change for different reasons_.
7. Tease apart the who, what, when, where, why, and how.

## Abstraction

### [AB1] See entanglement, not hiding.

Abstraction means "to draw away" or "to pull apart" and is more about **entanglement** than **hiding**. It is a skill that you sharpen by learning to see intertwined things that could otherwise be independent. The word we use for improving abstractions in software is *simplification*.

### [AB2] Untangle the six aspects.

To simplify in practice:

1. Untangle who, what, when, where, why, and how.
2. Identify components that depend on behaviors, and redesign them to depend on data.

### [AB3] Reduce interleaving to simplify.

To "simplify" something is to _reduce interleaving_ of its components or concerns. To the extent that interleaving can be identified, and thus reduced and therefore compared (before vs. after), "simplicity" is _an objective measurement_ and thus has less to do with aesthetics or personal preferences and more to do with tools and repeatable processes. This conception of objective simplicity is relatively new in computing, so the tools for measuring it are underdeveloped. We must take special *manual* care in analyzing complexity.

### [AB4] Test simplicity by reassembly.

**Simplicity is measured by ease of reassembly.** My working description of achieving simplicity in practice: "pull the system apart, and build it back together again, many times over."

## Cognitive Load

### [CL1] Use working memory as your complexity limit.

An intuitive measure of complexity is _cognitive load_. We can only simplify things we understand. We have limited working memory, and can only hold a few things together in our minds at one time. Intertwined things must often be considered together in order to understand the whole. The cognitive burden is combinatorial and multiplies with each additional slot taken in working memory during the process of understanding.

### [CL2] Name the aspects to pull them apart.

A straightforward way to start pulling things apart: ask questions and *assign names* to the following *aspects* of a program: who, what, when, where, why, and how.

## Change

### [CH1] Allow only accretion and relaxation.

We allow two types of change: _providing more_ (accretion) and _requiring less_ (relaxation). This approach to design allows the system to evolve over time in a stable way, and makes breaking changes nearly impossible.

### [CH2] Never mutate; create new with new names.

Never mutate or update. Create new things with new names. The old and new must coexist together. Removal of the old only happens when adoption of the new reaches 100%.

### [CH3] Provide more by strengthening outputs.

"Providing more" means:

1. Strengthening postconditions.
2. Returning more information.
3. Providing richer data structures.
4. Adding guarantees.

If providing more, ask:

1. What data structure(s) capture the "more" we are providing?
2. What functions depend on the new data structure?

### [CH4] Require less by relaxing inputs.

"Requiring less" means:

1. Relaxing preconditions.
2. Accepting broader inputs.
3. Requiring fewer inputs.

If requiring less, ask:

1. What data constraints can we remove or make optional?
2. What functions need to be updated to handle the broader input space?
3. What default values or behaviors handle the now-optional cases?

## Logic

### [LG1] Do not store knowledge as control flow.

Each `if` encodes an assumption and a decision. Local branching couples code to context. It hardens behavior and raises change cost.

### [LG2] Hoist decisions toward rule sets.

Pull `if` statements toward the places where related decisions live and change together. The higher you hoist them, the more declarative the program. Hoisted decisions collapse into rule sets. Higher still, rule sets become configuration: inputs to your program.

### [LG3] Treat decisions as data.

Treat decisions as data wherever possible. This defers commitment and reduces code paths.

### [LG4] Encode predicates in the model.

An `if` partitions the state space. **The predicate is a fact derived from an underspecified model**. Encode those facts in the model early, with types, invariants, or simple state machines.

Examples of `if` complexity:

1. `if (isValid)` for **data** (invalid states).
2. `if (shouldDoX)` for **behavior** (conditional execution).
3. `if (currentState === X)` for **flow** (sequencing/coordination).
4. `if (format === 'json')` for **transformation** (data reshaping).

Move logic into rules, not code paths, and invalid states will start to disappear.
