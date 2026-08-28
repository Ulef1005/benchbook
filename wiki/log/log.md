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
index/log/overview/todo stubs. Domains: knowledge, projects.
