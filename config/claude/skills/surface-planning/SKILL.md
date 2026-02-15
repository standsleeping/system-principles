---
name: surface-planning
description: Map how a concept's actions and state surface to users across channels (web UI, CLI, MCP, API). Verify operational principle discoverability and flag gaps.
---

# Surface Planning

Map how a concept surfaces to users. A concept that is perfectly designed but poorly surfaced is still a bad experience. Concepts, unlike internal mechanisms, are always user-facing (p. 65).

## When to use

- After assembling a concept definition (Stage 6)
- When planning how a concept will be exposed across multiple channels
- When auditing whether users can actually discover and use a concept

## Process

1. For each channel the concept will appear in (web UI, CLI, MCP, API, etc.):
   a. Map each action to its surface element — what the user sees or types (button, command, tool, endpoint, route).
   b. Map each state component to how it's made visible — and whether it's always shown, on-demand, or hidden.
   c. Describe how the user discovers the operational principle through this channel.
2. Identify gaps: actions or state with no surface in any channel.
3. Gaps are a signal. An unsurfaced action may be an exposed mechanism, or it may indicate a missing UI element.

## Artifact

```
ActionSurface {
  action:     str
  element:    str
  label:      str
}

StateSurface {
  component:  str
  element:    str
  visibility: "always" | "on-demand" | "hidden"
}

ConceptSurface {
  concept:    str
  channel:    "web-ui" | "cli" | "mcp" | "api"
  actions:    ActionSurface[]
  state:      StateSurface[]
  op_hint:    str
}

ConceptManifest {
  concept:    str
  surfaces:   ConceptSurface[]
  gaps:       str[]
}
```

## Validation

- Are all actions surfaced in at least one channel?
- Does the same concept use consistent language/labels across channels?
- Can a user learn the operational principle from each surface, or only from documentation?
