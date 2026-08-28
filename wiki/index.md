---
title: "Index"
type: overview
created: 2026-08-29
domain: null
subdomain: null
publish: false
tags: [meta, index]
sources: []
---

# Index

Master index. Kept deliberately short — roughly 50 lines. It changes only when a domain or a
meta page is added, never when an ordinary page is created.

The agent reads this first, identifies the relevant domain, then reads **only that domain's**
index. That two-step is what keeps retrieval cost flat as the wiki grows. See
[06 — Indexes](../docs/06-indexes.md).

## People

*(No people pages yet. `wiki/people/` is humans only.)*

## Domain Indexes

- [Knowledge](index-knowledge.md) — general concepts, tools, products, techniques
- [Projects](index-projects.md) — things being built, planned, or tracked

## Meta

- [Overview](overview.md) — cross-cutting themes and a paragraph per domain
- [Todo](todo.md) — pointers to active projects, wiki-meta decisions, latest LINT findings
- [Log](log/log.md) — chronological record of wiki-structural events
