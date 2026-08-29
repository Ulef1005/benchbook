---
title: "Hallway Display Build"
type: project
created: 2026-08-14
domain: projects
subdomain: null
publish: false
status: completed
tags: [demo]
sources: ["esphome-eink-dashboard-walkthrough"]
---

# Hallway Display Build

## Summary

Build a battery-powered e-ink panel for the hallway showing the day's calendar, outside
temperature, and bin day. Target: at least three months on a charge. Completed 2026-08-20.

Ongoing operation lives at [hallway-display](../../home/entities/hallway-display.md); this page
is the historical build record.

## Use Cases

| Need | Why |
|---|---|
| Calendar at a glance on the way out | Phone works but nobody checks it in the hallway |
| Outside temperature | Decides coat, every morning |
| Bin day reminder | The actual reason this got built |

Explicitly **not** interactive — no touch, no buttons. Anything requiring input belongs on a
phone.

## Hard- and Software

| Option | Cost | Pros | Cons |
|---|---|---|---|
| **ESP32-C6 + 4.2" e-ink** ✅ | ~€40 | Lowest sleep current; e-ink needs no power to hold an image | Slow refresh; no colour |
| ESP32-C3 + same panel | ~€32 | Cheaper | Higher sleep current — projected ~6 weeks, under target |
| Small LCD + mains power | ~€25 | Fast, colour | Needs a socket in the hallway. There isn't one |
| Repurposed tablet | €0 | Already owned | Battery lasts a day; screen is a light source at night |

**Selected: ESP32-C6 + 4.2" e-ink.** The mains-power option was ruled out first — running a
cable to that wall was the whole problem. Between the C6 and C3, sleep current alone decided
it: the C3 missed the three-month target and the ~€8 difference is irrelevant against a
rebuild.

Software: [ESPHome](../../knowledge/entities/esphome.md), config in `scripts/hallway-display/`.

## Plan / Phases

### Phase 1 — Breadboard ✅

- [x] Flash ESPHome to the C6, confirm Wi-Fi and OTA
- [x] Drive the panel, confirm partial refresh works
- [x] **Measure sleep current with a meter** — 41 µA

### Phase 2 — Layout ✅

- [x] Calendar, temperature, bin day on one screen
- [x] Full refresh every 20 partials to clear ghosting

### Phase 3 — Enclosure and mounting ✅

- [x] Frame, battery mounted behind
- [x] Hung by the door

### Phase 4 — Operational entity ✅

- [x] Create [hallway-display](../../home/entities/hallway-display.md) with
      `change_history: true` and the current state

## Open Questions

- [x] Is three months achievable on one charge? → **Yes.** At a 15-minute wake interval,
      measured draw projects to ~5 months.
- [x] Wake interval? → **15 min.** Started at 5; the underlying data doesn't change faster than
      15, and the shorter interval cost most of the battery life for nothing.

## Log

### [2026-08-27] Firmware pinned after a battery scare

Battery dropped to a week's charge remaining after an ESPHome upgrade. Sleep current had gone
41 µA → 1.2 mA. Rolled back and pinned to 2026.7.2; recorded on the entity page. **The logs
showed nothing** — this was only visible on a meter and in the battery curve.

### [2026-08-22] Wake interval raised to 15 min

Projected life went from 6 weeks to ~5 months. Should have started here.

### [2026-08-20] Built, mounted, project completed

All four phases done. Operational entity created; project moved to `completed/`.

### [2026-08-14] Project created, plan approved

Options table filled in and the C3 ruled out on sleep current before anything was bought.
