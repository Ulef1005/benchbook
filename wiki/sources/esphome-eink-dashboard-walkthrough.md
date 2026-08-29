---
title: "ESPHome E-Ink Dashboard Walkthrough"
type: source
created: 2026-08-12
domain: knowledge
subdomain: null
publish: false
tags: [tutorial, demo]
sources: []
source_url: "https://example.com/esphome-eink-walkthrough"
channel: example-maker-channel
---

# ESPHome E-Ink Dashboard Walkthrough

## Summary

A build walkthrough for a battery-powered e-ink status display driven by an ESP32-C6 running
ESPHome. Covers partial-refresh handling, deep sleep between updates, and the power budget
that decides whether a build like this lasts weeks or days. The useful part is the section on
what *not* to do — full refreshes on every update, and a display driver that blocks deep sleep.

## Key Takeaways

- **Partial refresh is what makes e-ink usable.** A full refresh takes ~3 s and flashes the
  panel; partial refresh is ~0.3 s and silent. Budget a full refresh every ~20 partials to
  clear ghosting.
- **Deep sleep dominates the power budget**, not the display. The panel draws nothing while
  idle; the radio is the cost.
- **Wake interval is the real design decision.** Every-minute wakes cut battery life to days;
  15-minute wakes stretch it to months. Pick the interval from what the data actually changes
  at, not from what feels responsive.
- **Some display drivers hold a lock that prevents deep sleep entirely.** Verify sleep current
  with a meter before assuming the configuration works.
- The ESP32-C6 was chosen over older variants for its lower deep-sleep current and native
  Thread support, though Thread isn't used in this build.

## Content

> Excerpt — the full walkthrough is at the source URL.

"...so the thing that gets everyone the first time is the refresh mode. If you just set it up
the default way, every single update does a full refresh — that's the flashing you see, black
to white to black, takes about three seconds. Looks broken. What you actually want is partial
refresh for routine updates, and then a full refresh maybe every twenty updates or so, just to
clear the ghosting that builds up.
>
> The second thing is sleep current. I had a build where I was getting maybe four days out of
a battery that should have lasted two months, and it turned out the display component was
holding a lock that stopped the board entering deep sleep at all. It looked fine in the logs.
You have to actually put a meter on it..."

## Sources

- [ESPHome E-Ink Dashboard Walkthrough](https://example.com/esphome-eink-walkthrough) — the
  original walkthrough

Produced the entity pages [ESPHome](../knowledge/entities/esphome.md) and
[ESP32-C6](../knowledge/entities/esp32-c6.md), and informed the build recorded at
[hallway-display](../home/entities/hallway-display.md).
