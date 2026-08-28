# Page Types

Every page declares a `type` in frontmatter. The type determines which template applies, which
fields are required, and which folder it belongs in — all three are checked mechanically.

The four core types carry almost everything:

| Type | What it is | Lives in |
|---|---|---|
| **source** | What some external material said | `sources/` (global) |
| **entity** | A thing the material was *about* | `people/`, `<domain>/entities/`, or `knowledge/entities/` |
| **reference** | A comparison or ranking across several entities | `<domain>/references/` |
| **project** | Something being built or tracked | `projects/` |

Domains may add their own — the books domain, for example, added author, series and candidate
types when the core four genuinely couldn't hold them. That's allowed, through proposal and
approval, and it's covered in [12 — Case Studies](12-case-studies.md).

---

## The entity-first principle

The most important convention here is which type you reach for by default.

**Entities are the norm. References are the exception.**

The tempting move, when a source compares five things, is to write one page comparing five
things. It reads well once. Then a second source covers two of those five, and you either
edit the comparison — losing the first source's framing — or you create a second comparison
page, and now the same claim exists in two places and will drift.

So the rule is:

- **1–3 things compared** → individual entity pages, cross-linked with a `## Compared To`
  section on each
- **4+ things ranked or compared** → a reference page may be justified, *and* it needs human
  approval

Entities compose. References don't. An entity page accumulates across every source that
mentions it; a reference page is a snapshot that starts going stale the moment it's written.

The live wiki has 268 entities against 59 references, and the references are being converted
to entities lazily — whenever one is next touched, rather than in a big migration.

---

## Frontmatter

Required on every page:

```yaml
---
title: "Page Title"
type: source | entity | reference | project | ...
created: YYYY-MM-DD
domain: <domain> | null
publish: false
tags: []
sources: []
---
```

Conditionally required:

| Field | When |
|---|---|
| `status` | entity (non-people) and project pages |
| `subdomain` | domains that use them; may be null only when genuinely cross-subdomain |
| `tags` | reference pages must carry exactly one "shape" tag — concept, comparison, ranking, buying-guide, or guide |

Useful optional fields:

| Field | Purpose |
|---|---|
| `source_url` | The online original |
| `raw_file` | Provenance pointer to the local copy; the lint pass reads this for archival |
| `repo_url` | For software entities — enables release tracking |
| `channel` | On source pages: the recurring origin. Drives the "third source from one origin" trigger for creating a channel entity |
| `change_history` | Opt-in, for entities whose state genuinely changes over time |

`publish: false` is the default on every page. See [13 — Privacy](13-privacy.md).

The `sources:` array and the body's relative links are **two-way mirrors** of each other: the
entity records which sources contributed, the source body links to the entities it produced.
One-directional links rot invisibly, which is why both directions are enforced.

---

## The Entity Placement Rule

The single hardest recurring judgement call, so it gets an explicit rule:

| The entity is… | It goes in |
|---|---|
| A specific human | `people/` |
| Something you own or operate — a specific instance | `<domain>/entities/` |
| A general concept, product, tool, or framework | `knowledge/entities/` |

The decision is made by **what the thing is**, not by how many domains reference it. Your
particular server is a home entity; its operating system is a knowledge entity; the person who
recommended it is a people entity. Cross-folder relations between all three are normal.

Two clarifications that resolve most of the remaining ambiguity:

- **`people/` is humans only.** Software personas, channels, brands and products are not
  people, however much they have names and personalities.
- **The call is made once, at first ingest.** Existing entities get reviewed when they're
  next touched, not proactively. Otherwise you spend your time re-filing instead of writing.

---

## Two entity patterns worth knowing

**Generic entity pages** — concepts, products, tools — use a light template: what it is, a
relations table using a controlled vocabulary of predicates, discrete key facts, when to use
it, what it compares to, and which sources contributed.

**Operational-instance entities** — a specific machine or service you run — opt into two extra
sections via `change_history: true`:

- `## Current State`, near the top, **overwritten in place**. Versions, config, what's
  deployed right now.
- `## Change History`, at the bottom, **append-only, newest first**. What changed and when.

That split is the useful bit. "What is true now" and "how it got that way" are different
questions asked at different times, and a page that interleaves them answers neither quickly.

Note the deliberate inconsistency: change history is newest-*first*, while the global log is
newest-*last*. The page section is read top-down for "what changed recently"; the log is read
as a timeline. Same data shape, opposite ordering, because they're used differently.

---

## Source pages embed their content

A source page carries the full transcript or text inline, under `## Content`, not just a
summary and a link.

This makes the wiki self-contained: the source survives the original URL going away, which it
eventually will. There are documented exemptions — material that genuinely can't be embedded,
or where the summary already fully distils it — but they're tagged explicitly, and the tag
requires the page to say *why* in its own body rather than just carrying the marker.

That "self-documenting exemption" pattern is worth stealing generally: any escape hatch from a
rule should require stating the reason on the page, or it becomes a rubber stamp within a
month.

---

**Next:** [06 — Indexes](06-indexes.md).
