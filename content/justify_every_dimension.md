---
id: JUSTIFY_EVERY_DIMENSION
title: "Justify Every Dimension."
essence: "A token chosen without reference to its visual context is an arbitrary number with a name."
---

Every CSS property that produces pixels (padding, width, gap, font-size, border-width) is a design decision. Selecting a token because it falls within a recommended range is not a decision; it is a guess that happens to compile.

**Name the relationship.** Before writing a dimension, identify what it relates to. A header's padding relates to the footer's padding. A sidebar's width relates to the content area's minimum readable width. A gap relates to the padding of the elements it separates. If you cannot name the relationship, you do not yet know what value to use.

**Match, echo, or contrast.** Every dimension relates to its neighbors in one of three ways:

1. **Match**: same token, same visual weight. The header and footer of a shell use the same padding because they are structural counterparts.
2. **Echo**: proportional relationship. A section gap is larger than an item gap because the Gestalt grouping requires it; the specific token is chosen relative to the item gap.
3. **Contrast**: deliberately different to signal hierarchy. A heading's font-size is larger than body text; the specific step is chosen so the difference is immediately perceptible (see TOKEN_SCALE_PERCEPTION).

If a dimension doesn't match, echo, or contrast something specific, it has no justification.

**The test.** After writing a dimension, ask: "If someone changed this value, what else would need to change to stay proportional?" If the answer is "nothing," the value is either isolated (rare) or unjustified (common).
