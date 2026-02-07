---
id: TRANSLATORS
title: "Translators."
essence: "Boundary functions that only convert and validate shape: they pass properly typed domain objects onward, never executing domain logic."
---

Translator functions (either units or integrators) sit at system or package boundaries, and can be either units or integrators, depending on the context.

**Translator as Unit:**

- Direct transformation of `dict[str, Any]` to domain types using only built-in functions.
- No dependencies: only standard library functions (uuid.UUID, datetime.fromisoformat, etc.).
- No imports: No calls to other application functions.
- Example: Converting string to UUID, parsing ISO datetime, basic type coercion.

**Translator as Integrator:**

- Composed conversion: Calls other units/integrators to perform complex translations.
- Has dependencies: Uses validation units, parsing integrators, or lookup functions.
- Assembles results: Combines multiple conversion operations into domain objects.
- Example: Converting request data that requires validation against existing domain rules.

**Both types:**

- Only convert: Transform external data to domain types.
- Only validate boundaries: Handle conversion errors and return appropriate error responses.
- Pass, don't execute: Return properly typed domain objects for other functions to use.
- No domain operations: Never call domain functions directly, leave that to the calling context.