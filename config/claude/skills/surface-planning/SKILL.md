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

## Projection model

Surface planning is where the canonical concept interface is projected into concrete interaction paths:

```
Action is semantic.
Affordance is interface-specific.
Transport is mechanical.
Encoding is representational.
Surface is interactional.
Channel is operational packaging.
Projection is the relationship that binds them for one capability.
```

Keep those layers distinct. A concept action such as `enter(modeKey)` belongs in the concept definition. A button, route, CLI command, MCP tool, or slash command belongs in the surface manifest as the affordance projection for that action on one channel.

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

1. Pick the target channels the concept is expected to cover from `channels.json` (add registry entries first if a channel is new).
2. Record target-channel intent in `target_channels`. If an otherwise expected channel does not apply to this concept, put it in `channel_exclusions` with a reason.
3. For each target channel, record an **affordance projection** per action — how *this* channel invokes the canonical action (button, command, tool, route). The projection references the action by name; the action's signature stays at the concept level (see `concept-actions` "Action vs affordance").
4. For each outbound-capable target channel (`system->caller` or `bi`), record an **emission projection** per emission — how *this* channel delivers, publishes, subscribes to, or receives the canonical emission.
5. Map each state component to how it's made visible, and whether it's always shown, on-demand, or hidden.
6. Describe how the user discovers the operational principle through this channel (`op_hint`).
7. For any action or emission with no sensible projection on a channel, record an exclusion with a reason rather than silently dropping it. Coverage is satisfied by a projection *or* an exclusion.
8. Collect remaining gaps. An action unsurfaced everywhere may be an exposed mechanism, or a missing UI element; an emission unsurfaced everywhere may be an unmodeled notification, event, feed, or webhook gap.

## Artifact

```
ActionSurface {        // an affordance projection: how a channel invokes a canonical action
  action:     str      // references an action in the ConceptDefinition
  element:    str      // the affordance (button, command, tool descriptor, route, slash command)
  label:      str
}

EmissionSurface {      // an emission projection: how a channel delivers or exposes an outbound emission
  emission:   str      // references an emission in the ConceptDefinition
  element:    str      // callback, event stream item, feed item, notification, topic, toast
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

EmissionExclusion {
  emission:   str
  reason:     str      // why this emission is not projected on this channel
}

ChannelExclusion {
  channel:    str
  reason:     str      // why this concept does not target this channel
}

ConceptSurface {
  concept:     str
  channel:     str             // a registered channels.json key
  actions:     ActionSurface[] // affordance projections; key name kept for compatibility
  emissions?:  EmissionSurface[]
  state:       StateSurface[]
  exclusions?: Exclusion[]     // actions intentionally not surfaced here
  emission_exclusions?: EmissionExclusion[]
  op_hint:     str
}

ConceptManifest {
  concept:             str
  target_channels?:    str[]              // channels this concept is expected to cover
  channel_exclusions?: ChannelExclusion[] // concept-level channel exclusions
  surfaces:            ConceptSurface[]
  gaps:                str[]
}
```

## Coverage

For each channel a concept surfaces on, **every** concept action must have an affordance projection or an exclusion. For each outbound-capable surfaced channel, **every** concept emission must have an emission projection or emission exclusion. `concept-validation` enforces this (it reports uncovered `concept:channel:action` and `concept:channel:emission` triples), so a forgotten projection no longer passes silently. When `target_channels` is present, every target channel must also have a surface unless it appears in `channel_exclusions` with a reason. When `channels.json` is present, every surface, target channel, and channel exclusion must reference a registered key; projected emissions must use `system->caller` or `bi` channels.

## Persistence

Persist on approval: write each `ConceptManifest` to `concepts/surfaces/<name>.json`, and the optional `ChannelRegistry` to `concepts/channels.json`. See the `concept-design` skill's **Persistence protocol**.

## Validation

- Is every concept action either afforded or explicitly excluded on each surfaced channel?
- Is every concept emission either projected or explicitly excluded on each outbound-capable surfaced channel?
- If `target_channels` is present, does every target channel have a surface or concept-level exclusion?
- Does the same concept use consistent language/labels across channels?
- Can a user learn the operational principle from each surface, or only from documentation?
- Are affordances kept distinct from actions (no pointer gesture masquerading as a concept action)?
