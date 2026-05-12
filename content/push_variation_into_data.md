---
id: PUSH_VARIATION_INTO_DATA
title: "Push variation into data."
essence: "When variants change faster than the code that processes them, represent the variation as rows of data, not as a growing union of types."
related: [ENCODE_BY_FAILURE_MODE, NO_KNOWLEDGE_AS_CONTROL_FLOW, DATA_DRIVEN_DISPATCH, HOIST_DECISIONS, CONSTANTS_ARE_VARIABLES, ALA_CARTE_POLYMORPHISM, DEPEND_ON_VALUES]
---

Every domain has a spine and a frill. The spine (account, customer, ledger, transaction) changes slowly and deserves precise types. The frill (promotion variants, eligibility rules, regional carve-outs, plan tiers) changes constantly. Encode the frill in types and every new variant becomes a code change: a new constructor, an exhausted match, a release.

Invert the representation. The *shape* of a variation is a type; the *variations themselves* are values of that type. Adding a new variation becomes a data change (a new row, a new config entry, a new database record), not a code change.

```python
# Frill as type proliferation: the union grows with every new rule
type Discount = (
    NewCustomerDiscount
    | LoyaltyTierDiscount
    | SeasonalDiscount
    | StudentDiscount
    | ReferralDiscount
    | BundleDiscount   # next quarter brings another
)

def apply(d: Discount, total: Cents) -> Cents:
    match d:
        case NewCustomerDiscount(): ...
        case LoyaltyTierDiscount(tier): ...
        # every consumer carries this match and must update on each addition

# Frill as data: the type is fixed; the rows multiply
@dataclass(frozen=True)
class DiscountRule:
    id: RuleId
    eligibility: Mapping[str, object]
    amount_pct: Decimal
    active_from: datetime
    active_to: datetime | None

RULES: list[DiscountRule] = load_rules_from_config()

def apply(rule: DiscountRule, total: Cents) -> Cents:
    return Cents(int(total * (1 - rule.amount_pct)))
```

Use when:

1. The set of variants changes faster than the code processing them.
2. Rules are owned by people who don't write code (ops, finance, legal).
3. New variants need to ship without a deploy.

Resist when:

1. Variants have genuinely different behavior, not just different parameters. A type union still wins when cases are not parameterizations of each other.
2. The variant axis is small and stable (a five-state payment status, a three-state subscription).

This is the directional cousin of `NO_KNOWLEDGE_AS_CONTROL_FLOW` (knowledge as data, not branches), `DATA_DRIVEN_DISPATCH` (dispatch as a dict, not a match), and `HOIST_DECISIONS` (scattered ifs → rule set → config). It is the positive move that `ENCODE_BY_FAILURE_MODE`'s "messy domains" bucket points to.
