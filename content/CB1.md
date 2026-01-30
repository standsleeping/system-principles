---
id: CB1
title: "Actions."
summary: "Accept a user's request, or specification of work, and return a result object. Characteristics:"
---

Accept a user's request, or specification of work, and return a result object. Characteristics:

- Entry point at a boundary: HTTP handler, CLI command, job runner, or scheduler tick.
- Accepts a user's request/specification and returns a typed result object.
- Uses translator functions to parse inputs and serialize outputs.
- Orchestrates units and integrators; contains no domain decisions itself.
- Performs side effects ONLY at boundaries.
- Valid boundary effects: transactions, appends events, enqueues jobs, logs/metrics/traces.
- Uses explicit control flow with early returns; avoids complex branching.
- Never raises to signal domain failures; returns typed results instead.