---
title: "Hallway Display"
type: entity
created: 2026-08-20
domain: home
subdomain: computing
publish: true
status: owned
change_history: true
tags: [demo]
sources: ["esphome-eink-dashboard-walkthrough"]
---

# Hallway Display

## Summary

A battery-powered e-ink status panel by the front door. Shows the day's calendar, outside
temperature, and whether the bins go out tonight. Built 2026-08-20; the build record is at
[hallway-display-build](../../projects/completed/hallway-display-build.md).

## Current State

> Overwritten in place when something changes. For how it got here, see § Change History.

| | |
|---|---|
| **Board** | [ESP32-C6](../../knowledge/entities/esp32-c6.md) |
| **Firmware** | [ESPHome](../../knowledge/entities/esphome.md) 2026.7.2 — **pinned**, see below |
| **Display** | 4.2" e-ink, partial refresh, full refresh every 20 updates |
| **Power** | 5000 mAh LiPo · measured 41 µA sleep current |
| **Wake interval** | 15 min |
| **Expected battery life** | ~5 months at current interval |
| **Config** | `scripts/hallway-display/` |

**Firmware is pinned to 2026.7.2.** 2026.8.x changed the display component's sleep handling and
sleep current went from 41 µA to 1.2 mA — roughly four days of battery instead of five months.
Do not upgrade without re-measuring with a meter; the logs look identical either way.

## Operations

- **Reflash:** OTA from the config directory. The device is only reachable in the ~8 s window
  after a wake, so start the flash and wait for it to catch one.
- **Battery check:** reported as a sensor; a reading below 3.4 V means about a week left.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Panel shows a stale screen | Wake failed, board still asleep | Power-cycle; check battery voltage |
| Ghosting builds up | Full-refresh counter reset | Force one full refresh |
| Battery draining in days | Sleep current regression — see the pin above | Roll back firmware, re-measure |

## Change History

- 2026-08-27 — Pinned ESPHome to 2026.7.2 after 2026.8.1 raised sleep current from 41 µA to
  1.2 mA. Caught by a battery reading, not by logs.
- 2026-08-22 — Wake interval 5 min → 15 min. Projected life 6 weeks → ~5 months; the data
  doesn't change faster than that anyway.
- 2026-08-20 — Built and mounted. Initial sleep current measured at 41 µA
  ([hallway-display-build](../../projects/completed/hallway-display-build.md)).
