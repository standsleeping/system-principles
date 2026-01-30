---
id: LG2
title: "Hoist decisions toward rule sets."
summary: "Pull `if` statements toward the places where related decisions live and change together. The higher you hoist them, the more declarative the program. Hoisted decisions collapse into rule sets. High..."
---

Pull `if` statements toward the places where related decisions live and change together. The higher you hoist them, the more declarative the program. Hoisted decisions collapse into rule sets. Higher still, rule sets become configuration: inputs to your program.