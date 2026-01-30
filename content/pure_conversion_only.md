---
id: PURE_CONVERSION_ONLY
title: "Pure conversion only."
summary: "Translators must transform interchange data from requests into properly typed domain objects, handle conversion errors with appropriate HTTP responses, and never perform domain operations (only con..."
---

Translators must transform interchange data from requests into properly typed domain objects, handle conversion errors with appropriate HTTP responses, and never perform domain operations (only convert types and pass to domain layer).