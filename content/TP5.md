---
id: TP5
title: "Pattern match to refine."
summary: "Pattern matching on sum types lets the compiler track what information is available in each branch:"
---

Pattern matching on sum types lets the compiler track what information is available in each branch:

```python
match grades.get("Alice"):
    case None:
        print("Not found")
    case grade:  # compiler knows grade is int
        print(f"Grade: {grade}")
```

For domain logic that changes frequently, consider data-driven dispatch instead (see Implementing > Polymorphism & Dispatch).