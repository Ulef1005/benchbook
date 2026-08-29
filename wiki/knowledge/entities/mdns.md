---
title: "mDNS"
type: entity
created: 2026-08-29
domain: knowledge
subdomain: null
publish: true
status: reference-only
tags: [demo, validation-test]
sources: ["mdns-workshop-note"]
---

# mDNS

## Summary

Multicast DNS (RFC 6762) — a protocol that lets devices on a local network resolve each
other's hostnames (e.g. `printer.local`) without a central DNS server, by having each device
answer for its own name over multicast. Almost always deployed alongside DNS-SD (RFC 6763) for
zero-config service discovery; together they're the mechanism behind Bonjour, Avahi, and most
smart-home device auto-discovery.

## Relations

| Subject | Predicate | Object |
|---|---|---|
| [ESPHome](esphome.md) | `uses` | mDNS |
| mDNS | `enables` | zero-config service discovery |
| mDNS | `requires` | link-local multicast (224.0.0.251, UDP 5353) |

## Key Facts

- Paired with DNS-SD (RFC 6763) for service discovery, not just name resolution
- Multicast is link-local by default — does not cross routers/VLANs without a reflector
- Common failure mode: a device becomes undiscoverable purely because it moved network
  segments, with no other symptom

## When to Use

Reach for this page when troubleshooting "device isn't showing up" reports for anything that
relies on auto-discovery (ESPHome, printers, Chromecast-style devices) — check VLAN/guest-network
segmentation before assuming a device-side fault.

## Sources

- [mDNS Workshop Note](../../sources/mdns-workshop-note.md)

---

*Created as part of a 2026-08-29 end-to-end workflow validation exercise — safe to remove.*
