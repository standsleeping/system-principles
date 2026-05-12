---
id: WITNESS_TYPES_GATE_STEPS
title: "Witness types gate the next step."
essence: "Each protocol step consumes the prior step's witness type and produces the next, so the type system enforces order. Skipping, repeating, or inverting a step becomes a type error, not a runtime bug."
related: [REFINED_TYPES_PROPAGATE_PROOFS, ILLEGAL_STATES_UNREPRESENTABLE, STRENGTHEN_INPUTS, CHASE_CHECKS_UPSTREAM, ENCODE_BY_FAILURE_MODE]
---

`REFINED_TYPES_PROPAGATE_PROOFS` says: validate once, then trust the type. This principle extends that idea to multi-step protocols. Each step takes the prior step's witness type as input and returns a tighter witness, so the type system enforces step ordering. A skipped, repeated, or inverted step becomes a type error rather than a runtime bug.

The witness is not richer data; it is evidence that a step ran. A `LoggedInUser` carries the same person as a `User`, plus the static fact that authentication occurred. Functions that require authentication take `LoggedInUser`; the only way to obtain one is to pass through `login`. Authorization then produces `AuthorizedUser`, obtainable only by passing a `LoggedInUser` through `authorize`. The signature `charge_card(user: AuthorizedUser, ...)` makes a charge attempt by an unauthenticated or unauthorized user not a forbidden code path; it is a non-existent one.

```python
# Ungated: every downstream call defends itself with the same checks
def view_admin(user: User, resource: Resource) -> Page:
    if not user.is_logged_in:
        raise AuthError(...)
    if not user.can_access(resource):
        raise AuthError(...)
    return render(resource)

# Forgetting either check is a silent AuthZ bug. The type system permits the bug.

# Gated: the chain gives each step a distinct input type
@dataclass(frozen=True)
class LoggedInUser:
    _user: User  # private constructor; produced only by login()

@dataclass(frozen=True)
class AuthorizedUser:
    _user: LoggedInUser  # private constructor; produced only by authorize()
    resource: Resource

def login(creds: Credentials) -> LoggedInUser | None: ...
def authorize(user: LoggedInUser, resource: Resource) -> AuthorizedUser | None: ...

def view_admin(user: AuthorizedUser) -> Page:
    return render(user.resource)  # no checks; uncallable without both proofs
```

The chain converts a class of bugs from "did we remember every check on every path?" into "does the call site have the right witness type?" A reviewer reading `view_admin(user)` no longer traces upward to confirm both checks ran. The signature is the audit trail.

Use when:

1. A protocol has ordered steps where skipping one is a silent failure (auth, payment capture, transaction commit, parser stages: `RawAst → ResolvedAst → TypedAst`).
2. The same entity flows through multiple checks and each success should be visible to downstream code.
3. You catch yourself re-checking the same predicate at multiple call sites.

Resist when:

1. The protocol has one step. A plain refined type from `REFINED_TYPES_PROPAGATE_PROOFS` is enough.
2. Steps are commutative. If order doesn't matter, the witness chain encodes a constraint that does not exist.
3. The chain would be deep and the language lacks ergonomics for it. Verbose wrapping can push the cost above the benefit.

Two construction disciplines keep the chain honest. Witness constructors must be private to the step that produces them; if any caller can build a `LoggedInUser` directly, the gate is a fiction. And the witness must carry, not lose, the prior witness; a chain that drops `LoggedInUser` on the way to `AuthorizedUser` cannot later answer "who authorized?" In both, the unsafe construction lives inside one module and the only public exit is the witness type.

This principle is the multi-step extension of `REFINED_TYPES_PROPAGATE_PROOFS`, the protocol-level application of `STRENGTHEN_INPUTS`, and the answer to `CHASE_CHECKS_UPSTREAM` when the upstream is itself a sequence of checks. It is the bucket from `ENCODE_BY_FAILURE_MODE` where the violation (skipped auth, charged-but-uncommitted, used-resolved-name-before-resolution) is both silent and catastrophic.
