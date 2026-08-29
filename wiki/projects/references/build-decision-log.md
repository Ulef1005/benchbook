---
title: "Build Decision Log"
type: reference
created: 2026-08-22
domain: projects
subdomain: null
publish: true
tags: [concept, demo]
sources: []
---

# Build Decision Log

## Summary

Decisions that apply across more than one build, so they don't get re-litigated per project.
This is what `projects/references/` is for: notes supporting **multiple** projects, rather than
belonging to any one of them.

## Standing decisions

### Always measure before enclosing

Confirmed on [hallway-display-build](../completed/hallway-display-build.md). Any power or
thermal assumption gets measured on a breadboard before anything is glued, screwed or mounted.
A wrong number found at the breadboard costs an afternoon; found after mounting it costs the
build.

### "Already owned" is not free

From [kitchen-tablet-dashboard](../abandoned/kitchen-tablet-dashboard.md), abandoned partly on
this. Reusing a device you already have has real costs — power, mounting, degradation, and the
constraints the original design imposes. Price them before treating reuse as the cheap option.

### Pin firmware on anything hard to reach

If reflashing means standing on a chair or removing a mount, pin the version and record why.
Applies to [hallway-display](../../home/entities/hallway-display.md); will apply to
[office-air-quality-sensor](../office-air-quality-sensor.md) if it ends up mounted.

### Mains changes the design, so don't inherit battery constraints

Noted while planning [office-air-quality-sensor](../office-air-quality-sensor.md). The hallway
build's design was shaped almost entirely by having no power socket. The office has one — so
deep-sleep current, wake intervals and e-ink stop being requirements. **Copying a good design
into a different constraint set is a common way to build the wrong thing.**

## Why these live here

Each of these came out of one project but binds the next one. Left on the originating project
page they'd be found only by someone already reading that page — which is nobody, at the moment
they'd be useful.
