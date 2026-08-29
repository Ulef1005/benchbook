---
title: "ESPHome"
type: entity
created: 2026-08-12
domain: knowledge
subdomain: null
publish: true
status: reference-only
tags: [demo]
sources: ["esphome-eink-dashboard-walkthrough", "mdns-workshop-note"]
repo_url: "https://github.com/esphome/esphome"
---

# ESPHome

## Summary

A firmware generator for ESP32 and ESP8266 microcontrollers. You describe a device in YAML —
which sensors, which display, what to publish — and it compiles and flashes firmware. Removes
the need to write embedded C for the common cases, and handles OTA updates, so a device you've
mounted on a wall stays updatable.

## Relations

| Subject | Predicate | Object |
|---|---|---|
| ESPHome | `runs_on` | [ESP32-C6](esp32-c6.md) |
| ESPHome | `enables` | OTA firmware updates |
| ESPHome | `uses` | [mDNS](mdns.md) |
| [hallway-display](../../home/entities/hallway-display.md) | `uses` | ESPHome |

## Key Facts

- Configuration is YAML; secrets live in a separate file referenced with `!secret`
- OTA updates require the device to be reachable on the network at flash time
- Some display components hold locks that prevent deep sleep — see § When to Use

## When to Use

Good for anything sensor-shaped where you'd otherwise write firmware by hand, and especially
good when the device is somewhere physically inconvenient — OTA is the feature that matters.

**Gotcha worth knowing before you build:** certain display drivers keep the board awake, which
silently destroys the power budget on a battery build. Symptoms look like a battery problem;
the logs look fine. Verify sleep current with a meter rather than trusting the configuration.

## Compared To

Hand-written firmware gives finer control and is worth it when timing matters. ESPHome wins on
maintenance — a YAML file you can read in two years beats C you'd have to re-understand.

## Sources

- [ESPHome E-Ink Dashboard Walkthrough](../../sources/esphome-eink-dashboard-walkthrough.md)
- [mDNS Workshop Note](../../sources/mdns-workshop-note.md)
