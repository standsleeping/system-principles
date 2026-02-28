---
id: IDEMPOTENT_BY_DEFAULT
title: "Design operations to be idempotent."
essence: "Same request, same result, regardless of repetition."
---

Networks fail, clients retry, messages arrive twice. If an operation isn't idempotent, repetition causes damage. The core technique: declare the desired state rather than describe a delta.

```python
# Non-idempotent: each call changes the result
def increment_balance(account_id, amount):
    db.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?",
               amount, account_id)
    # Retry after timeout? Balance incremented twice.

# Idempotent: repeated calls produce the same outcome
def set_balance(account_id, amount):
    db.execute("UPDATE accounts SET balance = ? WHERE id = ?",
               amount, account_id)
    # Retry after timeout? Same balance written again.
```

`STATELESS_DESIGN` makes reads naturally idempotent (no state to corrupt). This principle extends the same safety to writes: the result of applying an operation once is indistinguishable from applying it many times.
