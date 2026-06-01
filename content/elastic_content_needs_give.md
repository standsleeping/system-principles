---
id: ELASTIC_CONTENT_NEEDS_GIVE
title: "Elastic Content Needs Give."
essence: "Content is bounded (sized by design) or elastic (sized by data); a chrome rail has no give. Put elastic content in a flow region or a rail's single ellipsizing slot, never as a peer among fixed controls — the mismatch is invisible until space runs out."
related: [LABEL_CONTAINMENT, SCROLL_CONTAINMENT, RESPONSIVE_COMPONENTS, FIXED_FLEXIBLE_REGIONS, PEER_RAIL, CONTENT_DRIVES_SIZE]
---

Every piece of content is either **bounded** — its size is fixed by *design* (a button, a slider, an icon, a label you author) — or **elastic** — its size is set by *data* (a record's name, a list, a table that can be any length). Every container has a **give**: a flow region grows and wraps or scrolls; a chrome rail is rigid. The rule is a match: elastic content may only live where there is give to absorb it. Putting elastic content where there is none is the defect, and it is invisible at a comfortable width — it surfaces only when space is constrained.

This is the cause behind a whole family of symptoms: a center column that grows a horizontal scrollbar, a title that floats onto its own wrapped line, a toolbar that clips a control, a table that pushes the page wide. Each is elastic content (or too much content) dropped into a container that cannot give.

## Bounded vs elastic

The distinguishing question is not "how big is it now" but "what sets its size":

- **Bounded** — fixed by design. A control's footprint, an icon, a label whose text you wrote. You can size a slot to it once and trust it (`LABEL_CONTAINMENT`).
- **Elastic** — set by data. A component name, a username, a file path, a list of rows. You cannot size a slot to it, because the next value may be longer. It must either be given room to grow, or be allowed to truncate.

The trap is treating elastic content as bounded because the sample you tested happened to fit.

## Where each kind of content belongs

| Content | Nature | Home | Absorbs variance by | Anti-pattern |
|---|---|---|---|---|
| Control (button, slider, input, icon, badge) | bounded | chrome strip / inline | fixed size | — |
| A control's own label | bounded | with its control; size the box to it | container widened (`LABEL_CONTAINMENT`) | box too narrow for the full label |
| Data-derived single line (title, name, path, breadcrumb) | elastic | a rail's *one* title slot, **or** a flow heading | ellipsis (rail) / wrap (flow) | a peer item in a strip → overflow, clip, or float |
| Prose / collection (lists, cards, rows) | elastic | flow region | wrap + vertical scroll at the region | a fixed-height rail |
| One intrinsically-wide block (table, code, chart) | elastic, one axis | a leaf element with its own `overflow-x` | horizontal scroll on the element | `overflow-x` on a layout container (`SCROLL_CONTAINMENT`) |

## Containers, by give

| Container | Give | Holds | Overflow rule |
|---|---|---|---|
| Fixed rail (header, status bar) | none — fixed height (`PEER_RAIL`) | bounded controls **+ at most one ellipsizing title slot** | never wraps, never scrolls |
| Wrapping chrome strip (a toolbar of many controls) | grows vertically (wraps to rows) | many bounded controls | wraps; no scroll; **no titles** |
| Flow region (the content body) | grows + vertical scroll | elastic content | wrap; vertical scroll at the region; horizontal clip |
| Leaf scroller | one-axis scroll | one oversized block | scrolls that axis only |

A fixed rail and a wrapping strip look alike but differ in give: the rail stays one row, the strip reflows. A title belongs in neither as a peer — it floats the moment a wrapping strip wraps, and it overflows or clips the moment a fixed rail is squeezed. It belongs in the rail's dedicated title slot (which ellipsizes) or in flow.

## Decision tree

1. **Is the size bounded by design?** → control or fixed label → chrome strip or inline; size the box to it (`LABEL_CONTAINMENT`). Done.
2. **Data-derived, single line?** → is there a rail with a free title slot? Yes → put it in that ellipsizing slot. No → a flow heading. Never a peer item in a strip.
3. **Multi-line or a collection?** → a flow region (vertical scroll). Never a fixed-height rail.
4. **One intrinsically-wide block?** → a leaf element with its own `overflow-x: auto`. Never a layout container.

## The rail corollary

The cheapest checkable consequence: **a fixed rail never wraps and never scrolls, so it carries bounded controls plus at most one ellipsizing title slot.** A rail that has wrapped to a second row is the signature of elastic content (or too much content) in a give-less slot — move the elastic part to flow or to the title slot, or, if the strip genuinely holds many bounded controls that must reflow, make it an explicit wrapping strip rather than a fixed rail.

## Design for the constrained case

The mismatch is latent: at a wide viewport the elastic content happens to fit, so the layout looks correct. It breaks only when a sidebar, an inspector, or a small window squeezes the container. "It looks fine on my screen" is the trap. Decide placement against the *narrowest supported width*, and verify there (`WIDTH_CONTROLLED_TESTING`); a width-swept overflow audit catches the cases the eye misses.

## Relationship to other principles

- `LABEL_CONTAINMENT` is the bounded case — make the box fit a label you control. This principle is the elastic case: you cannot size a box for arbitrary data, so you ellipsize or flow. The two are complementary; the dividing question is bounded-by-design vs. by-data.
- `RESPONSIVE_COMPONENTS` and `RESPONSIVE_TABLES` are *how* elastic content degrades once it is in the right region (hide by priority; restructure). This principle decides *which* region it goes in first.
- `SCROLL_CONTAINMENT` is the wide-block row of the table: horizontal scroll lives on the leaf, never the layout container.
- `FIXED_FLEXIBLE_REGIONS` and `PEER_RAIL` define the rigid containers that have no give.
- `CONTENT_DRIVES_SIZE` is the inverse view: where content *may* size its container, let it; where it may not (a rail), the content must adapt instead.
