# Domains

A domain is a top-level subject area. Every page belongs to exactly one, declared in
frontmatter and reflected in the folder it lives in.

Domains are the first thing the agent decides during an ingest, and getting that call right
is the highest-leverage moment in the whole workflow — nearly every downstream filing mistake
traces back to a wrong domain at step two.

---

## Why domains exist at all

A flat wiki works until it doesn't. The failure isn't dramatic; it's that the index grows
past the point where reading it is cheap, and the agent starts making worse retrieval
decisions because it's choosing from four hundred undifferentiated entries.

Domains fix this by partitioning both the folder tree *and* the index. The agent reads the
small master index, identifies the relevant domain, and then reads only that domain's
catalogue. Cost stays roughly flat as the wiki grows. See [06 — Indexes](06-indexes.md).

They also let the rules differ. A recipe and a book review need genuinely different treatment,
and a single set of conventions covering both would be too vague to steer either. Each domain
gets a satellite rules file, loaded only when working in that domain.

---

## Two kinds of domain

**Regular domains** hold subject matter and have their own folder, index, and rules file. In
the live wiki those are:

| Domain | What's in it |
|---|---|
| `home` | The physical/digital home — hardware, servers, automation, appliances, travel |
| `knowledge` | General concepts, tools, and products not tied to one thing you own |
| `projects` | Things being built or tracked |
| `books` | Reading — books, authors, series, to-read candidates |
| `cooking` | Recipes and meal planning |
| `sports` | Training and gear, split by sport |
| `gaming` | Games, split per game |
| `music` | Instruments and music gear |
| `wisdom` | Durable non-technical insight worth keeping |

**Special locations** cut across domains and behave differently:

| Location | Rule |
|---|---|
| `sources/` | **All** source pages, globally, regardless of domain. The `domain:` field is the only signal of where a source belongs; the index groups by it. |
| `people/` | Humans only. No status field, and a section used by the meal planner. |
| `log/` | The chronological record plus its archives and lint reports. |

`sources/` being global is a deliberate call that took a while to settle. Source pages are
frequently cross-domain, they're the most numerous single type, and filing them per-domain
means constantly re-litigating which domain a given article "really" belongs to. Making the
location global and the domain a *field* removes that argument entirely.

---

## Choosing a domain

The question is **what the page is**, not who will read it or how many domains reference it.

The hardest recurring call is entities, which gets its own rule — see the Entity Placement
Rule in [05 — Page Types](05-page-types.md). The short version:

- A **person** → `people/`
- A **specific thing you own or operate** → that domain's `entities/`
- A **general concept, product, or tool** → `knowledge/entities/`

So your particular server is a home entity; the operating system it runs is a knowledge
entity. Cross-folder relations between them are normal and expected.

---

## Domain-specific skills

Some domains accumulate enough recurring work to justify their own tooling. In the live wiki,
the books domain has skills for capturing a recommendation from a link or screenshot (with a
collision check against the existing library) and for reading titles out of social-media
carousel images. The projects domain has skills for starting, opening, and stress-testing a
project.

The pattern to copy is the trigger, not the specific skills: **when you find yourself
performing the same multi-step sequence in a domain for the third time, that's a skill.** See
[10 — Skills](10-skills.md).

---

## Practical advice on starting

**Start with two domains.** Not nine.

The nine above accumulated over months, each one added when existing domains genuinely
couldn't hold something. Copying all nine upfront gets you seven empty folders, an index full
of headings with nothing under them, and an agent making placement decisions between
categories that have no content to compare against.

Domains are cheap to add later and expensive to abandon half-populated.

**A note on skew.** In the live wiki, the books domain is roughly 47% of all pages — the
result of a bulk library import. That's fine, but it's worth knowing that one import can
dominate your page counts and make the wiki look more balanced or less balanced than the
actual work is. Page count is a poor proxy for where the value is.

---

**Next:** [05 — Page Types](05-page-types.md).
