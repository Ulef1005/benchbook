---
title: "Overview"
type: overview
created: 2026-08-29
domain: null
subdomain: null
publish: false
tags: [meta]
sources: []
---

# Overview

The synthesis layer. Updated during INGEST post-flight **only when the big picture actually
shifted** — which is rarely.

## Themes

Cross-cutting observations that don't belong to a single domain. The connections between
things you've filed, rather than the things themselves.

- **Sleep current is the whole design constraint on battery builds.** It decided the board
  (C6 over C3), the wake interval, and — after a firmware upgrade raised it 30× — a version
  pin. Notably it is invisible in logs; only a meter and the battery curve show it. *(demo)*

## By Domain

### Knowledge

One walkthrough ingested, producing two entities: [ESPHome](knowledge/entities/esphome.md) and
[ESP32-C6](knowledge/entities/esp32-c6.md). Both are things that exist in the world — the
specific device built from them lives in `home`. *(demo)*

### Home

One owned device: [Hallway Display](home/entities/hallway-display.md), running and pinned to a
known-good firmware version. *(demo)*

### Projects

One completed ([hallway-display-build](projects/completed/hallway-display-build.md)) and one
planned with its plan still gated
([office-air-quality-sensor](projects/office-air-quality-sensor.md)). *(demo)*
