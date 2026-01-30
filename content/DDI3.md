---
id: DDI3
title: "Translators bridge the gap."
summary: "Don't let interchange types leak deep into the domain. Parse them into domain types at the boundary."
---

Don't let interchange types leak deep into the domain. Parse them into domain types at the boundary.

**Input Flow**: `External JSON` → `Interchange Type (TypedDict)` → `Translator` → `Domain Type`
- The translator validates structure and parses values (string → UUID).
- The domain type constructor guarantees the object is valid.

**Output Flow**: `Domain Type` → `Translator` → `Interchange Type (TypedDict)` → `External JSON`
- The translator converts rich types (UUID) back to primitives (string).
- The interchange type ensures the output shape matches the API contract.