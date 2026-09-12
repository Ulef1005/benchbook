# Page Conventions — Detail

> Loaded on-demand: read this file before creating or substantially editing any wiki page
> (INGEST), or during LINT's frontmatter/section checks. Not loaded at session start — see
> `agents-core.md § 5 Page Conventions` for what stays in core.

## YAML Frontmatter

**Universal — required on every wiki page:**

```yaml
---
title: "Page Title"
type: source | entity | reference | overview | project
created: YYYY-MM-DD
domain: knowledge | projects | null
subdomain: <value> | null
publish: false
tags: [tag1, tag2]
sources: ["source-page-slug"]
---
```

**Universal — optional:**

```yaml
source_url: "https://..."          # primary online origin URL when known
raw_file: "raw/<filename>"         # provenance pointer; LINT scans this for archival
status: <see below>                # required on entity (non-people) and project pages
repo_url: "https://github.com/..." # software/tool entities; enables release tracking
channel: <origin-slug>             # source pages: recurring origin — drives the 3-source entity trigger
change_history: true               # opt-in; owned operational-instance entities only
```

**`publish` field:** every page defaults to `publish: false`. A human flips it to `true` per
page. Keep the field even with no publishing pipeline — it marks *"I have consciously decided
this is shareable."*

**`status` field by page type:**

| Page type | Allowed values | Notes |
|---|---|---|
| `entity` (products, gear, tools) | `owned \| considered \| retired \| reference-only` | Skip on people-entities. |
| `project` | `planned \| active \| on-hold \| deployed \| completed \| abandoned` | `completed`/`deployed` trigger a move to `wiki/projects/completed/`; `abandoned` to `wiki/projects/abandoned/`. `deployed` is software-specific and additionally requires `## Version Control`, `## Backup Concept`, and `## Cron Jobs`. |
| All others | omit | |

**Tags vocabulary (controlled, extensible):**

| Facet | Values | Applies to |
|---|---|---|
| Reference shape | `concept`, `comparison`, `ranking`, `buying-guide`, `guide` | required on every `reference` page (pick one) |
| Page shape | `review`, `guide`, `spec`, `manual`, `tutorial` | source pages, optional |
| Voice | `personal-take` | optional; marks pages with personal opinion vs. neutral synthesis |

New tag values are added deliberately — propose in `agents-core.md`, don't coin ad-hoc.

## Required vs Optional Fields

LINT flags any required field that is missing or empty.

**Required on every page:** `title`, `type`, `created`, `domain`, `publish`, `sources` (may be
`[]`).

**Required on specific page types:**

- `status` — entity (non-people) and project pages
- `tags` — `reference` pages must include exactly one shape tag; optional elsewhere
- `subdomain` — only in domains that define subdomains; may be `null`

## Generic Entity Page Conventions

For concepts, products, tools, frameworks, channels — the typical residents of
`wiki/knowledge/entities/`. The same template applies to any `<domain>/entities/` page.
Include only sections with actual content.

| Section | Purpose |
|---|---|
| `## Summary` | What it is (2–4 sentences) |
| `## Relations` | Triplet table: `Subject \| Predicate \| Object` — links this entity to others via typed predicates from the 36-term controlled vocabulary in `agents-domain-knowledge.md`. Query the full neighbourhood, including edges stored on other pages, with `./scripts/relations.py <slug>` |
| `## Key Facts` | Discrete attributes that don't fit a triplet |
| `## When to Use` | Actionable recommendation, use cases, gotchas |
| `## Compared To` | Direct comparison with close alternatives; link to a reference page if one exists |
| `## Sources` | Source pages that contributed (frontmatter `sources:` is the machine-readable mirror) |

## People Entity Conventions

Person pages (`wiki/people/<slug>.md`) have no `status:` field.

`wiki/people/` is **humans only**. Software personas, products, tools and channels belong in
`wiki/<domain>/entities/` or `wiki/knowledge/entities/` per the Entity Placement Rule.

## Change History Conventions

Opt-in via `change_history: true`. Applies to **owned operational-instance entity pages** —
pages representing a specific thing you own and operate, whose configuration, software, or
setup changes meaningfully over time. Excluded: static spec-sheet entities, project pages
(they already have `## Log`), and people pages.

**Two required sections** when `change_history: true` is set:

| Section | Position | Purpose |
|---|---|---|
| `## Current State` | Near the top, after `## Summary` | Key-facts snapshot, **overwritten in place** when state changes. Versions, config, what's deployed right now. |
| `## Change History` | Last main section | Append-only, **newest first**. What changed and when. |

**Entry format:**

```
- YYYY-MM-DD — event description ([Source](../../sources/source-page.md) or free text)
```

**Ordering** is newest-first, intentionally opposite to `wiki/log/log.md` (newest at bottom).
The page section is read top-down for "what changed most recently"; the log is read as a
timeline.

**Split rule — Change History vs global log:** page-local state changes (version bumps, config
changes, hardware swaps) → `## Change History`. Page creation, cross-cutting milestones, and
significant operations → `wiki/log/log.md`.

## Source Page Conventions

Source pages live at `wiki/sources/<slug>.md` — global, flat, regardless of domain. The
`domain:` frontmatter is the only signal of which domain a source belongs to; the index groups
by that field.

Canonical section template (include only sections with actual content):

| Section | Content | When |
|---|---|---|
| `## Summary` | 2–4 sentence overview | always |
| `## Key Takeaways` | Bulleted distilled facts | always |
| `## Content` | Full source text — transcript for video/audio, full text for PDFs and web clips | required when the source has fetchable content |
| `## Timestamps` | Timestamp-linked facts (e.g. `4:32 — claim confirmed`) | video/audio only |
| `## Sources` | URL link to the original | always |

Embedding the full content inline keeps the wiki self-contained — the source survives the
original URL going away, which it eventually will.

**`content-exempt` tag:** mark a source page with `tags: [..., content-exempt]` when
`## Summary` + `## Key Takeaways` already fully distil the source, or when it genuinely can't
be embedded (paywalled, print-only, unfetchable). LINT then skips the missing-`## Content`
warning. **Not a rubber stamp** — the page body must state *why*, or the exemption becomes
automatic within a month.

**`standalone-reference` tag:** mark any page terminal **by decision rather than neglect** —
research kept after a "not doing it" call, an abandoned project with no successor. LINT skips
the orphan warning. Same self-documenting standard: the page must state the decision in its
own body.

## Reference Page Conventions

Reference pages are the **exception**, not the default. The entity-first model is the norm.

**Create a reference page only when 4+ entities are ranked or compared in the source.** For
1–3 entities, create individual entity pages and link them with `## Compared To` cross-links.

Entities compose across every source that mentions them; a reference page is a snapshot that
starts going stale the moment it's written.

## Project Page Conventions

**Required sections, in order** (LINT-enforced):

1. `## Summary` — 2–4 sentences
2. `## Relations` — **required while `status` is `active` or `planned`**, directly after
   `## Summary`. See § Project Relations below
3. `## Use Cases` — what it needs to actually do, concretely
4. `## Hard- and Software` — options table with comparison, then a "Selected" subsection;
   supporting infrastructure as relative links to entity pages
5. `## Plan / Phases` — **GATED: stub only until the plan is manually approved.** Must carry a
   prominent *"Deferred — awaiting manual plan approval."* notice
6. `## Open Questions` — unresolved decisions blocking progress
7. `## Log` — chronological, append-only

`deployed` status additionally requires `## Version Control`, `## Backup Concept`, and
`## Cron Jobs`.

**Plan approval gate.** While a project is `planned`, no implementation work may begin — no
code, no files, no API calls — until the human explicitly approves the plan. On approval,
status moves to `active` and the plan is written out in full.

**Final-step rule.** If a project's completion produces an owned, running system, its
`## Plan / Phases` must end with a step creating (or confirming) an operational entity page
documenting the deployed state. The entity page becomes the living document; the project page
becomes the historical build record and moves to `completed/`. Check for existing coverage
first — a roster page or adjacent entity may already satisfy it.

## Project Relations

**`## Relations` is required on every project whose `status` is `active` or `planned`**,
positioned directly after `## Summary` — the same slot entity pages use. LINT enforces presence
and position; the predicate check enforces the contents.

**Scoped to open projects on purpose.** Requiring it on closed projects too would error on every
completed and abandoned page in the wiki, and since the error-class checks gate commits, that
wedges the repo for no benefit: a finished project's relations are of historical interest only.
Scope a new rule to the pages it actually helps.

**A row is written only if that fact is not already stored elsewhere.** Each fact lives exactly
once, on whichever page reads naturally, so most of an established project's relations already
sit on the entity pages that name it. The section therefore opens with a pointer:

```markdown
## Relations

Full neighbourhood, including relations stored on other pages: `./scripts/relations.py <slug>`
```

**A pointer-only section is a valid, complete section.** In the wiki this came from, 25 of the
40 open projects have no page-local row at all, because everything known about them was already
recorded elsewhere — or because nothing is recorded yet, which is also a true state.

**Never invent a relation to avoid an empty table.** One true row beats five plausible ones. A
sparse graph is merely incomplete; a graph with inferred edges in it is wrong, and you won't be
able to tell which edges those were six months later.

**Which predicate?** `evaluates`, unless something more specific fits — see
`domains/knowledge/agents-domain-knowledge.md` § Which predicate for a project → entity relation.
