---
id: TIME_DEPENDENT_RESULTS
title: "Capture time-dependent results explicitly."
essence: "When time affects an operation's outcome, capture that result in an explicit structure rather than letting it vanish."
---

Effects are complex; they entangle _who_ and/or _what_ and/or _how_ with **when**. When the _time you run the code_ can impact what the outcome is, you have effects, and thus, complexity.

In some cases this is unavoidable. In the cases where it is, you must take special care. Use a result structure (`EffectResult`) to store the results of any operation where the _time you run the code_ can impact what the outcome is.