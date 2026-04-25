---
id: EVENT_SOURCING
title: "Event sourcing."
essence: "A User isn't a row. It's the sum of UserCreated, EmailChanged, and the rest. The entity is a convenience view. The event stream is the truth."
---

Events are living documentation of system behaviors. Note that all "entities" or objects that appear as nouns are almost always _composed_ from streams of events.

A User isn't a row. It's the sum of UserCreated, EmailChanged, PasswordReset, and SubscriptionUpgraded events. The "current state" is a view derived from the event stream. The events are the truth; the entity is a convenience.