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

## Channels come from a registry

A **channel** is a named bundle of three orthogonal axes — **transport** (HTTP, WebSocket, IPC), **encoding** (JSON, HTML, plaintext), and **surface** (button, slash command, tool descriptor, route) — plus `direction`, `sync`, and `auth_model`. These are registered once per system in `concepts/channels.json` (schema: `channel-registry.schema.json`); a surface references a channel by its `key`. Registering channels in one place lets the coverage check reason about them and keeps two concepts surfacing on the same channel from re-declaring its axes. A starter registry to copy and trim:

```json
{
  "$schema": "channel-registry.schema.json",
  "channels": [
    {"key": "web-ui",    "transport": "HTTP",      "encoding": "HTML",      "surface": "button",          "direction": "bi",            "sync": "sync",      "auth_model": "session"},
    {"key": "cli",       "transport": "local",     "encoding": "plaintext", "surface": "command",         "direction": "caller->system","sync": "sync",      "auth_model": "local"},
    {"key": "mcp",       "transport": "stdio",     "encoding": "JSON",      "surface": "tool-descriptor", "direction": "caller->system","sync": "sync",      "auth_model": "capability"},
    {"key": "api",       "transport": "HTTP",      "encoding": "JSON",      "surface": "route",           "direction": "caller->system","sync": "sync",      "auth_model": "bearer"},
    {"key": "http-rest", "transport": "HTTP",      "encoding": "JSON",      "surface": "route",           "direction": "caller->system","sync": "sync",      "auth_model": "bearer"},
    {"key": "webhook",   "transport": "HTTP",      "encoding": "JSON",      "surface": "callback-url",    "direction": "system->caller","sync": "async",     "auth_model": "shared-secret"},
    {"key": "sse",       "transport": "HTTP",      "encoding": "JSON",      "surface": "event-stream",    "direction": "system->caller","sync": "streaming", "auth_model": "session"},
    {"key": "slack-bot", "transport": "HTTP",      "encoding": "JSON",      "surface": "slash-command",   "direction": "bi",            "sync": "async",     "auth_model": "OAuth"},
    {"key": "cron",      "transport": "local",     "encoding": "plaintext", "surface": "schedule",        "direction": "system->caller","sync": "async",     "auth_model": "service-account"},
    {"key": "rss",       "transport": "HTTP",      "encoding": "XML",       "surface": "feed-item",       "direction": "system->caller","sync": "async",     "auth_model": "none"}
  ]
}
```

## Process

1. Pick the channels the concept lives in from `channels.json` (add registry entries first if a channel is new).
2. For each chosen channel, record an **affordance** per action — how *this* channel invokes the canonical action (button, command, tool, route). The affordance references the action by name; the action's signature stays at the concept level (see `concept-actions` "Action vs affordance").
3. Map each state component to how it's made visible, and whether it's always shown, on-demand, or hidden.
4. Describe how the user discovers the operational principle through this channel (`op_hint`).
5. For any action with no sensible affordance on a channel, record an **exclusion** with a reason rather than silently dropping it. Coverage is satisfied by an affordance *or* an exclusion.
6. Collect remaining gaps. An action unsurfaced everywhere may be an exposed mechanism, or a missing UI element.

## Artifact

```
ActionSurface {        // an affordance: how a channel invokes a canonical action
  action:     str      // references an action in the ConceptDefinition
  element:    str      // the affordance (button, command, tool descriptor, route, slash command)
  label:      str
}

StateSurface {
  component:  str
  element:    str
  visibility: "always" | "on-demand" | "hidden"
}

Exclusion {
  action:     str
  reason:     str      // why this action is not surfaced on this channel
}

ConceptSurface {
  concept:     str
  channel:     str             // a registered channels.json key
  actions:     ActionSurface[] // affordances
  state:       StateSurface[]
  exclusions?: Exclusion[]     // actions intentionally not surfaced here
  op_hint:     str
}

ConceptManifest {
  concept:    str
  surfaces:   ConceptSurface[]
  gaps:       str[]
}
```

## Coverage

For each channel a concept surfaces on, **every** concept action must have an affordance or an exclusion. `concept-validation` enforces this (it reports uncovered `concept:channel:action` triples), so a forgotten action no longer passes silently. When `channels.json` is present, every surface's `channel` must be a registered key.

## Validation

- Is every concept action either afforded or explicitly excluded on each surfaced channel?
- Does the same concept use consistent language/labels across channels?
- Can a user learn the operational principle from each surface, or only from documentation?
- Are affordances kept distinct from actions (no pointer gesture masquerading as a concept action)?
