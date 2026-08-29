---
title: "ESP32-C6"
type: entity
created: 2026-08-12
domain: knowledge
subdomain: null
publish: true
status: reference-only
tags: [demo]
sources: ["esphome-eink-dashboard-walkthrough"]
---

# ESP32-C6

## Summary

A RISC-V microcontroller with Wi-Fi 6, Bluetooth LE and native 802.15.4 (Thread and Zigbee).
Notable against older ESP32 variants for lower deep-sleep current, which is the number that
decides battery life on anything that wakes periodically.

## Relations

| Subject | Predicate | Object |
|---|---|---|
| ESP32-C6 | `is_a` | microcontroller |
| ESP32-C6 | `supports` | Thread |
| ESP32-C6 | `runs` | [ESPHome](esphome.md) |
| ESP32-C6 | `replaces` | ESP32-C3 (for low-power builds) |
| [hallway-display](../../home/entities/hallway-display.md) | `uses` | ESP32-C6 |

## Key Facts

- Deep-sleep current is materially lower than the C3, which is the reason to pick it for
  battery builds
- Native 802.15.4 means Thread without an extra radio — useful even if you don't use it today
- Wi-Fi 6 support is largely irrelevant at this scale; don't let it drive the decision

## When to Use

Pick it when the device sleeps most of the time and runs on a battery. If the device is mains
powered, the deep-sleep advantage doesn't apply and a cheaper variant is fine.

## Compared To

Against the **ESP32-C3**: better sleep current, native Thread, slightly higher cost. Against
the **ESP32-S3**: the S3 has more RAM and USB-OTG, which matter for displays and audio; the C6
wins on power. Choose by whether the constraint is compute or battery.

## Sources

- [ESPHome E-Ink Dashboard Walkthrough](../../sources/esphome-eink-dashboard-walkthrough.md)
