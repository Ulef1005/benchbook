---
title: "Kitchen Tablet Dashboard"
type: project
created: 2026-07-30
domain: projects
subdomain: null
publish: false
status: abandoned
tags: [demo]
sources: []
---

# Kitchen Tablet Dashboard

## Summary

Mount an old tablet in the hallway as an always-on dashboard for calendar, weather and bin day.
**Abandoned 2026-08-10** — see the Log. Superseded by
[hallway-display-build](../completed/hallway-display-build.md), which solved the same problem
with e-ink.

## Use Cases

| Need | Why |
|---|---|
| Calendar at a glance on the way out | Nobody checks their phone in the hallway |
| Weather / coat decision | Every morning |
| Bin day | The actual motivating problem |

## Hard- and Software

| Option | Cost | Pros | Cons |
|---|---|---|---|
| **Old tablet, wall-mounted** ✅ (chosen, then abandoned) | €0 | Already owned; colour; touch | Needs power; screen is a light source; battery degrades if left charging |
| Buy a dedicated panel | ~€120 | Purpose-built | Expensive for the problem |

**Selected: the old tablet** — on the reasoning that a device already owned is free, and free
is hard to argue with.

That reasoning turned out to be wrong, and the way it was wrong is the useful part of this
page. See the Log.

## Plan / Phases

### Phase 1 — Software ✅

- [x] Dashboard page rendering calendar, weather, bin day
- [x] Kiosk-mode browser, screen-on lock

### Phase 2 — Mounting ✗ (never started)

- [ ] Wall mount and cable routing

## Open Questions

- [x] Can the screen be dimmed enough at night? → **No, not usefully.** Minimum brightness was
      still a visible glow in a dark hallway.
- [x] Is there a power socket within reach? → **No.** This was the decisive one.

## Log

### [2026-08-10] Abandoned — three reasons, in order of decisiveness

1. **No power socket within reach of the wall.** Running a cable was the entire original
   problem and this design reintroduced it. Should have been checked in week one; it was
   assumed rather than measured.
2. **The screen is a light source.** Minimum brightness was still a glow in a dark hallway at
   night. An always-on display in a hallway has to be invisible when unlit, and an LCD can't
   be.
3. **Battery degradation.** A tablet left permanently on charge swells within a year or two.
   "Already owned, therefore free" ignored the cost of destroying the thing.

**The generalisable mistake: "free because already owned" was treated as a decision rather
than a constraint to test.** The tablet was free; making it work was not.

Superseded by [hallway-display-build](../completed/hallway-display-build.md) — e-ink needs no
power to hold an image, emits no light, and runs months on a battery. All three failures above
became the requirements that picked it.

### [2026-07-30] Project created

Dashboard page built and running in a browser within the first session.
