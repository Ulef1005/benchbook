---
title: "Index — Knowledge"
type: overview
created: 2026-08-29
domain: knowledge
subdomain: null
publish: false
tags: [meta, index]
sources: []
---

# Index — Knowledge

Full catalogue for the knowledge domain. Every entry: `- [Title](path.md) — one-line summary`.

**The one-line summary is the retrieval signal.** It should say what the page is *for*, not
restate the title. "Comparison of four options, decided on the second" beats "notes about
options." Writing these lazily is the main way index-based retrieval fails.

### Sources

- [ESPHome E-Ink Dashboard Walkthrough](sources/esphome-eink-dashboard-walkthrough.md) — build walkthrough for a battery e-ink panel; the useful part is the power-budget mistakes *(demo)*

### Entities

- [ESPHome](knowledge/entities/esphome.md) — YAML-to-firmware generator for ESP32/ESP8266; OTA is the feature that matters, and some display drivers silently block deep sleep *(demo)*
- [ESP32-C6](knowledge/entities/esp32-c6.md) — RISC-V microcontroller; picked over the C3 on deep-sleep current, which is the number that decides battery life *(demo)*

### References

- [Low-Power ESP32 Boards Compared](knowledge/references/low-power-esp32-boards.md) — four variants on deep-sleep current, the number that decides battery life; a snapshot, so prefer entity pages where you can *(demo)*
