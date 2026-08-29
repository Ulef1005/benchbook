---
title: "Todo"
type: overview
created: 2026-08-29
domain: null
subdomain: null
publish: false
tags: [meta]
sources: []
---

# Todo

The single todo location.

> **Pointer-only for projects.** Project todos live on each project page's `## Open Questions`
> section and are **not** duplicated here. In the original wiki, 60 of ~76 mirrored items had
> drifted from their source pages before this rule changed. Any duplicated state will diverge,
> silently, and you will trust the wrong copy.

## Active Projects

*(empty — links only, no mirrored items)*

## Planned Projects

- [office-air-quality-sensor](projects/office-air-quality-sensor.md) — plan gated pending sensor choice (closed 2026-08-29, still needs plan approval)

## Wiki Meta

Hand-curated. Pending decisions, schema proposals, reference updates, deferred items.

- [ ] `scripts/lint.py` doesn't exist yet — mechanical checks are currently run by hand every time, at model-token cost, contrary to the "cheaper, repeatable, runnable on every commit" goal stated in `agents-lint-checks.md`. Worth porting from the source wiki.

## LINT Findings

Rewritten by each LINT run. See `wiki/log/lint-2026-08-29.md` for full detail.

- **1 real contradiction** (`office-air-quality-sensor.md`): `## Hard- and Software` still says
  "Selected: TBD" but the open question was closed with NDIR selected — the two sections
  disagree. *(Planted deliberately as a validation test of this exact check — confirms the
  judgement-check design works when actually applied.)*
- **0 broken relative links**, **0 duplicate/sync-artifact files**, **0 raw/-path body links**
  across all 18 wiki pages (checked by hand, `scripts/lint.py` absent — see Wiki Meta above)
- Predicate vocabulary: all `## Relations` rows use controlled-vocabulary predicates
- Entity placement: no misplacements found; `mDNS` correctly filed as a general concept under
  `knowledge/entities/`
