---
id: CONCEPTUAL_INTEGRITY
title: "Conceptual integrity is the highest design property."
essence: "A system that reflects one set of design ideas, even at the cost of omitting features, is better than one that contains many good but uncoordinated ideas."
related: [REASSEMBLY, DESIGN_NOT_WORKFLOW, DESIGN_FRAMEWORK, MODULES_HIDE_DECISIONS, START_SIMPLE, REDUCE_INTERLEAVING, ENTANGLEMENT_NOT_HIDING]
---

Per Brooks, conceptual integrity is "the most important consideration in system design. It is better to have a system omit certain anomalous features and improvements, but to reflect one set of design ideas, than to have one that contains many good but independent and uncoordinated ideas."

Per Jackson (*The Essence of Software*, 2021), integrity has an operational test at the concept level: when concepts are composed, each still fulfills its purpose in isolation. The canonical violation is **concept overloading** — a feature accreted into the system stretches a concept to cover a second purpose, so neither is served cleanly; its dual is **concept redundancy**, two concepts competing for one purpose. Conceptual integrity is the property that keeps the mapping between concepts and purposes one-to-one.