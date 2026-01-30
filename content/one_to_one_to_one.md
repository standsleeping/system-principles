---
id: ONE_TO_ONE_TO_ONE
title: "The 1:1:1 Rule."
summary: "We maintain a strict 1:1 correspondence between:"
---

We maintain a strict 1:1 correspondence between:

1. **Data and files**: One data structure per file.
2. **Functions and files**: One function per file.
3. **Files and tests**: One file, one test suite.

Union types and their constituent result types may be grouped together in a single file when they form a cohesive set of related outcomes for a specific operation.

Example: `RegistrationResult = RegistrationSuccess | AlreadyExists | InvalidAppData`.

At the same level as the functions and data, there may also exist subpackages with semantically meaningful names, themselves having the same data/function structure as the subpackage they are in.