---
title: "Log"
type: overview
created: 2026-08-29
domain: null
subdomain: null
publish: false
tags: [meta]
sources: []
---

# Log

Chronological, append-only. Newest entries at the **bottom**.

Entry format — the consistent prefix makes this parseable with ordinary shell tools
(`grep "^## \[" log.md | tail -10`):

```
## [YYYY-MM-DD] <op> | Subject

One to three lines. ~40 words maximum.
```

Valid ops: `ingest`, `create`, `lint`, `query`, `skill`.

**There is deliberately no `update` op.** Project progress belongs in that project's `## Log`;
entity state changes belong in that entity's `## Change History`. See
`agents-core.md § 6 Log` for why.

---

## [2026-08-29] create | Wiki scaffold

Initial structure created from the benchbook starter: contract, satellites, folder tree,
index/log/overview/todo stubs. Domains: knowledge, home, projects.

## [2026-08-12] ingest | ESPHome E-Ink Dashboard Walkthrough

Source page plus two knowledge entities (ESPHome, ESP32-C6). Power-budget takeaways fed the
hallway display build. *(demo content)*

## [2026-08-14] create | Hallway Display Build

Project page created, options table filled, plan approved. C3 ruled out on sleep current
before anything was bought. *(demo content)*

## [2026-08-20] create | Hallway Display

Operational entity created as the build's final phase; project moved to `completed/`.
*(demo content)*

## [2026-08-28] create | Office Air Quality Sensor

Project created with a gated plan. Sensor choice blocks everything. *(demo content)*

## [2026-08-29] ingest | mDNS Workshop Note

Source page + `mDNS` entity created from workshop dictation; two-way linked to existing
`ESPHome` entity (`uses`). Part of an end-to-end workflow validation pass, not real content —
safe to remove.

## [2026-08-29] lint | Full manual run (script missing)

1 real contradiction found (planted as a test), 0 broken links, todo.md synced (was missing
the Planned project). `scripts/lint.py` doesn't exist — flagged as a gap. Report:
`wiki/log/lint-2026-08-29.md`.
