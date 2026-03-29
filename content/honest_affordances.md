---
id: HONEST_AFFORDANCES
title: "Affordances must be honest."
essence: "Interactive styling is a promise; only apply it when the action it implies is actually available."
---

A highlight, underline, pointer cursor, or color change that signals "you can act on this" is a promise. If clicking does nothing, the promise is broken and the user loses trust in the interface's visual language.

Gate interactive styling on actual capability, not potential capability:

1. If data hasn't loaded yet, don't show the affordance until it has
2. If an item has no target (no docs, no link, no action), leave it visually inert
3. If a mode enables interaction on a subset of elements, only mark that subset

The cost of a missing affordance (user doesn't know they can click) is lower than a false affordance (user clicks and nothing happens). The first is a discovery problem; the second erodes confidence in every other affordance on the page.
