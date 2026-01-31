---
id: HOIST_DECISIONS
title: "Hoist decisions toward rule sets."
summary: "Pull `if` statements toward the places where related decisions live and change together. The higher you hoist them, the more declarative the program. Hoisted decisions collapse into rule sets. High..."
---

Pull `if` statements toward the places where related decisions live and change together. The higher you hoist them, the more declarative the program. Hoisted decisions collapse into rule sets. Higher still, rule sets become configuration: inputs to your program.

```
Scattered ifs  →  Grouped ifs  →  Rule set  →  Config file
(hardest)                                      (easiest to change)
```

Each level of hoisting makes the decision easier to find, easier to change, and easier to hand to someone else.