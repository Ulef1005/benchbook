---
title: "Office Air Quality Sensor"
type: project
created: 2026-08-28
domain: projects
subdomain: null
publish: false
status: planned
tags: [demo]
sources: []
---

# Office Air Quality Sensor

## Summary

A CO₂ and particulate sensor for the office, reporting somewhere visible enough that it
actually changes behaviour. The room gets stuffy by mid-afternoon and nobody notices until
it's bad.

## Use Cases

| Need | Why |
|---|---|
| CO₂ reading, visible without asking | Stuffiness is noticed too late to act on |
| Alert above a threshold | The point is to open a window *before* the headache |
| History over a day | To find out whether it's occupancy or the heating |

## Hard- and Software

| Option | Cost | Pros | Cons |
|---|---|---|---|
| True NDIR CO₂ sensor | ~€35 | Measures CO₂ directly; accurate | Larger, needs a warm-up period |
| eCO₂ (VOC-derived) sensor | ~€12 | Cheap, small | *Estimates* CO₂ from VOCs — drifts, and misreads on cleaning products |
| Commercial monitor | ~€90 | Works out of the box | Cloud account; no local data |

**Selected: TBD** — pending the open question below. Leaning NDIR, since an estimate that
misreads whenever someone uses a cleaning spray fails the one job this has.

Would reuse [ESPHome](../knowledge/entities/esphome.md) and the approach proven in
[hallway-display-build](completed/hallway-display-build.md).

## Plan / Phases

> **Deferred — awaiting manual plan approval.**

1. Choose the sensor and confirm the reading is trustworthy on a breadboard
2. Decide where the reading is displayed
3. Enclosure and placement
4. Threshold alerting
5. Create the operational entity page

**No implementation work has begun** and none may begin until the plan is approved. This is the
plan approval gate — see [09 — Projects](../../docs/09-projects.md).

## Open Questions

- [x] **NDIR or eCO₂?** → **NDIR** (validation-test decision, 2026-08-29) — an estimate that
      misreads on cleaning products fails the one job this sensor has; the ~€23 premium over
      eCO₂ buys a reading worth trusting.
- [ ] Mains or battery? Mains is easy here, which removes the constraint that shaped the
      hallway build — worth not copying that design out of habit.
- [ ] Where does the reading go — a small display, an existing dashboard, or a notification?

## Log

### [2026-08-29] Sensor choice closed — NDIR (validation test)

Closed as part of an end-to-end workflow validation pass — not a real decision, safe to
revert. Demonstrates the wiki-project-open "close an open question" action: `[ ]` → `[x]`,
decision recorded inline, `## Hard- and Software` still says "Selected: TBD" and was
deliberately left unsynced to check whether LINT's contradiction-detection catches it.

### [2026-08-28] Project created, plan gated

Options table filled in. Sensor choice is the blocking decision; nothing gets bought or built
until it's settled and the plan is approved.
