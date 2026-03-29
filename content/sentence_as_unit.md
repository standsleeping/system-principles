---
id: SENTENCE_AS_UNIT
title: "Render sentences as discrete visual units in structured content."
essence: "When content is designed to be individually annotated or manipulated, each sentence gets its own line, not paragraph flow."
---

Traditional paragraphs optimize for reading flow: sentences run together, the eye tracks continuously. This is correct for long-form prose.

Structured content has different requirements. When each sentence may be individually annotated, referenced, paraphrased, or manipulated, render it as its own block element with vertical spacing between siblings.

Sentence-per-line supports:

1. Per-unit interaction (hover, selection, annotation)
2. Visible unit boundaries (the user sees where one claim ends and the next begins)
3. Gap-awareness: logical leaps between sentences become spatially visible
4. Insertion points: new content (bridging sentences, elaborations) can be wedged between existing units without reflowing a paragraph

The principle: match visual structure to interaction granularity. If the system treats sentences as atoms, display them as atoms.

This does not apply to all prose. Narrative text, documentation, and explanatory writing should flow as paragraphs. The trigger is whether the content is designed to be operated on at the sentence level.
