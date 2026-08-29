---
title: "Low-Power ESP32 Boards Compared"
type: reference
created: 2026-08-13
domain: knowledge
subdomain: null
publish: true
tags: [comparison, demo]
sources: ["esphome-eink-dashboard-walkthrough"]
---

# Low-Power ESP32 Boards Compared

## Summary

Four ESP32 variants compared on the one axis that decides battery life: deep-sleep current.
Written while choosing a board for
[hallway-display-build](../../projects/completed/hallway-display-build.md).

> **Why this is a reference page and not four entity pages.** The rule is 4+ entities ranked or
> compared, with human approval — see `agents-page-conventions.md`. At 1–3 you'd write entity
> pages and cross-link them with `## Compared To`. Four crosses the line where a single table
> genuinely reads better than four pages.
>
> Note the cost: this page is a **snapshot**. It starts going stale immediately, whereas entity
> pages accumulate. Prefer entities when you can.

## Comparison

| Board | Deep sleep | Active | Thread | Notes |
|---|---|---|---|---|
| **ESP32-C6** | ~7 µA | ~80 mA | native | Best sleep current; the pick for battery builds |
| ESP32-C3 | ~43 µA | ~85 mA | no | ~6× the sleep draw — misses a 3-month target |
| ESP32-S3 | ~35 µA | ~110 mA | no | More RAM and USB-OTG; worth it for displays and audio |
| ESP32 (original) | ~150 µA | ~120 mA | no | Fine on mains, unusable on a battery |

Figures are datasheet-order-of-magnitude, not measured. **Measure your own** — the
[hallway-display](../../home/entities/hallway-display.md) build came in at 41 µA against a
~7 µA datasheet figure, because the panel and regulator draw too.

## Recommendation

- **Battery, wakes periodically** → C6. Sleep current dominates everything else.
- **Mains powered** → the sleep advantage is irrelevant; pick on RAM and peripherals.
- **Display or audio work** → S3, and accept the power cost.

## Compared To

Individual entity pages exist for [ESP32-C6](../entities/esp32-c6.md). The others don't have
pages yet — they'd be created if a build actually used one.

## Sources

- [ESPHome E-Ink Dashboard Walkthrough](../../sources/esphome-eink-dashboard-walkthrough.md)
