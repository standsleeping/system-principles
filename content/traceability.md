---
id: TRACEABILITY
title: "Traceability."
essence: "If you can't reconstruct what happened from database queries alone, your system is missing data."
---

Easy audit trails are composed via the database. Composing a set of SQL queries to create a full picture of what happened is how 99% of bugs are found.

When something goes wrong, you open a SQL console and start asking questions. "What events happened for this user?" "What was the state at this timestamp?" If you can't answer these questions with queries, your system is missing data.