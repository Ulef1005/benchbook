---
title: "mDNS Workshop Note"
type: source
created: 2026-08-29
domain: knowledge
subdomain: null
publish: true
tags: [guide, demo, validation-test]
sources: []
raw_file: "raw/validation-test-note.md"
---

# mDNS Workshop Note

## Summary

Workshop notes on mDNS (multicast DNS, RFC 6762) — how devices on a local network resolve
hostnames like `printer.local` without a central DNS server, and how the paired DNS-SD (RFC
6763) mechanism does zero-config service discovery on top of it. Covers why this is the
auto-discovery mechanism behind Bonjour/Avahi and a lot of smart-home gear, including
[ESPHome](../knowledge/entities/esphome.md) devices, and the most common way it silently
breaks.

## Key Takeaways

- mDNS lets each device answer for its own hostname via multicast (224.0.0.251 / UDP 5353)
  instead of a central DNS server
- DNS-SD (RFC 6763), layered on mDNS, is how a device advertises and discovers services
  (e.g. "who offers `_http._tcp` here?")
- Bonjour, Avahi, and ESPHome's device auto-discovery all build on this pair of protocols
- mDNS traffic is link-local and does not cross routers by default — a device moving to a
  different VLAN or a guest network silently loses discoverability
- Symptom pattern: "why can't I see my printer/ESPHome device" tickets very often trace back
  to exactly this segmentation issue
- Some routers offer an mDNS reflector/repeater to bridge segments deliberately

## Content

Quick note from a workshop talk on mDNS (multicast DNS, RFC 6762). It lets devices on a local
network resolve hostnames like `printer.local` without a central DNS server — each device
answers for its own name by listening on the multicast address 224.0.0.251 (or the IPv6
equivalent) on UDP port 5353. Paired with DNS-SD (RFC 6763) it's how mDNS does service
discovery too: a device can ask "who offers `_http._tcp` on this network?" and get a list
back, which is the mechanism Bonjour/Avahi and a lot of smart-home gear (like ESPHome devices)
build on for auto-discovery. The talk's main caution: mDNS traffic doesn't cross routers by
default (multicast is link-local), so it silently breaks the moment a device moves to a
different VLAN or a guest network — a lot of "why can't I see my printer/ESPHome device"
tickets trace back to exactly this. Some routers offer an mDNS reflector/repeater to bridge
segments on purpose.

## Sources

No public URL — captured from workshop notes. See `raw/validation-test-note.md` for the
original dictation.

---

*Created as part of a 2026-08-29 end-to-end workflow validation exercise — safe to remove.*
