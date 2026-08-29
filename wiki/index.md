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

- [Alex](people/alex-demo.md) — synthetic example showing the shape of a person page *(demo)*

`wiki/people/` is humans only. Software personas, channels, brands and products go to
`knowledge/entities/` or a domain's own `entities/`.

## Domain Indexes

- [Knowledge](index-knowledge.md) — what exists in the world: general concepts, tools, products
- [Home](index-home.md) — what you own and operate: hardware, devices, self-hosted services
- [Projects](index-projects.md) — what you're building, planning, or tracking

## Meta

- [Overview](overview.md) — cross-cutting themes and a paragraph per domain
- [Todo](todo.md) — pointers to active projects, wiki-meta decisions, latest LINT findings
- [Log](log/log.md) — chronological record of wiki-structural events
