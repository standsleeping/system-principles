---
id: EV1
title: "Store facts with time."
summary: "Hickey points out that the Resource Description Framework lacks a time component. \"Sally likes pizza...\" _as of when, exactly?_"
---

Hickey points out that the Resource Description Framework lacks a time component. "Sally likes pizza..." _as of when, exactly?_

Store facts as 5-tuples:

1. **Entity**. Who or what (e.g. Sally).
2. **Attribute**. The property (e.g. likes).
3. **Value**. The actual value (e.g. pizza).
4. **Time**. When this fact was asserted.
5. **Operation**. Are we adding or retracting?

This temporal model means the user can:

1. Track the full history of changes.
2. Query the database "as of" any point in time.
3. Know when facts became true or stopped being true.