---
id: BT1
title: "Translator functions."
summary: "Use translator functions as the standard pattern for converting external data (JSON, HTTP requests) into domain objects. These functions have a single, narrow responsibility:"
---

Use translator functions as the standard pattern for converting external data (JSON, HTTP requests) into domain objects. These functions have a single, narrow responsibility:

- **Pure conversion**: Transform interchange data from requests into properly typed domain objects.
- **Boundary validation**: Handle conversion errors with appropriate HTTP responses.
- **No domain logic**: Never perform domain operations, only convert types and pass to domain!