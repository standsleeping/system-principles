---
id: PURPOSE_BUILT_DOUBLES
title: "Use purpose-built boundary test doubles."
essence: "Purpose-built doubles encapsulate boundary behavior cleanly; ad-hoc mocks scatter assumptions across tests."
---

Use purpose-built test doubles for external boundaries rather than general-purpose mocking libraries. Create dedicated helpers for each boundary type: HTTP clients, sessions, filesystem, environment variables, databases. These helpers encapsulate the boundary's behavior and provide a cleaner testing interface than ad-hoc mocks.