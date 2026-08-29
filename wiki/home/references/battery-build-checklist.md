---
title: "Battery Build Checklist"
type: reference
created: 2026-08-21
domain: home
subdomain: computing
publish: false
tags: [guide, demo]
sources: []
---

# Battery Build Checklist

## Summary

The steps that decide whether a battery-powered sensor lasts months or days. Written after
[hallway-display-build](../../projects/completed/hallway-display-build.md), where two of these
were learned the expensive way.

## Before ordering anything

- [ ] **Decide the wake interval from the data, not from feel.** How often does the underlying
      value actually change? Every-minute wakes cost roughly 15× the battery of every-15-minute
      wakes and usually show the same number.
- [ ] **Budget the power from the wake interval**, then pick the board. Not the other way round.
- [ ] Check the display or sensor holds no lock that blocks deep sleep.

## On the breadboard, before the enclosure

- [ ] **Measure sleep current with a meter.** Not the logs. The logs will look correct on a
      board that never sleeps.
- [ ] Compare the measurement against the datasheet figure. Expect to be several times worse —
      the regulator and peripherals draw too.
- [ ] Project the battery life from the *measured* number and confirm it clears the target
      before building an enclosure around it.

## After it's running

- [ ] **Pin the firmware version.** Record the pin and the reason.
- [ ] Re-measure sleep current after any firmware upgrade, before trusting it.
- [ ] Expose battery voltage as a sensor so decline is visible before it's a failure.

## The two learned the hard way

**Sleep current is invisible in logs.** A firmware upgrade raised it 30× on
[hallway-display](../entities/hallway-display.md) and nothing in the logs changed. It surfaced
as a battery reading a week later. Any upgrade on a battery device needs a meter, not a log
check.

**The wake interval is worth more than the board choice.** Going from 5 to 15 minutes turned
six weeks into five months — a bigger gain than any hardware decision in the build, and free.
