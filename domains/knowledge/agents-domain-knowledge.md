# benchbook — Domain Rules: Knowledge

> Loaded during INGEST for the knowledge domain. Read alongside `agents-core.md`.

---

## What belongs here

General concepts, tools, products, frameworks, techniques — things that exist in the world
independently of you. The knowledge domain is the default home for anything you've *learned
about* rather than *own*.

The distinction that matters, per the Entity Placement Rule in `agents-core.md`:

- A general product, tool or concept → `wiki/knowledge/entities/`
- The specific instance you own and operate → that domain's own `entities/` folder
- A human → `wiki/people/`

So a container runtime is a knowledge entity; the particular server you run it on is not.

**Default subdomain:** `null`.

**Page types this domain produces:** source, entity, reference.

Knowledge sources go to the **global** `wiki/sources/` folder, like every other source — only
the `domain: knowledge` frontmatter marks them as belonging here.

---

## Dispatch flow

**K1.** Create the source page at `wiki/sources/<slug>.md` — `## Summary` → `## Key Takeaways`
→ `## Content` (when fetchable) → `## Sources`.

**K2.** Identify the entities the source is *about*. Propose them; create only approved ones.
Apply the Entity Placement Rule for each — don't default everything to knowledge.

**K3.** Two-way link. The entity's `sources:` frontmatter gets the source slug; the source
body links to the entity with a relative link.

**K4.** Update existing entities silently where the source adds facts, and note it in the
report.

**K5.** Channel trigger — if this source's `channel:` value now has **three** sources, propose
a channel/author entity (template below).

**K6.** References — only if the source ranks or compares **4+ entities**, and only with human
approval. For 1–3, use entity pages with `## Compared To` cross-links.

---

## Predicate Vocabulary

Predicates in `## Relations` triplet tables must come from this list. LINT flags anything
else. **If a fact doesn't fit any predicate, it's usually a discrete attribute — put it in
`## Key Facts` rather than forcing a relation.**

| Predicate | Meaning | Inverse |
|---|---|---|
| `is_a` | type / category membership | — |
| `made_by` | manufactured / created by | `makes` |
| `makes` | manufacturer → its product | `made_by` |
| `includes` | bundles / contains | `part_of` |
| `part_of` | component of a larger whole | `includes` |
| `uses` | depends on / employs | `used_by` |
| `used_by` | employed by | `uses` |
| `runs` | hardware/host → software it runs | `runs_on` |
| `runs_on` | software → its host platform | `runs` |
| `integrates_with` | works together with (symmetric) | — |
| `competes_with` | alternative to (symmetric) | — |
| `replaces` | supersedes / successor of | — |
| `requires` | hard dependency | — |
| `supports` | optional capability / compatibility | — |
| `enables` | makes possible | — |
| `evaluates` | project/person considering the entity | `evaluated_for` |
| `evaluated_for` | entity → the project/person considering it | `evaluates` |
| `compared_to` | weighed side-by-side; **not** necessarily rivals — use `competes_with` for actual alternatives | — |

The subject of a row does not have to be the page's own entity — pick the direction that reads
naturally and use the inverse predicate when needed.

> **Why a controlled vocabulary.** In the original wiki this list was derived after the fact,
> from 66 existing entity pages, and the derivation immediately surfaced synonym drift —
> `is_made_by` / `produced_by` / `made_by` all in use for the same relation. Left alone, a free
> predicate field becomes unqueryable within months. If you're starting fresh, adopt the list
> now and extend it deliberately.

---

## Channel / Author Entities

Proposed at the **3rd** source from one origin (a YouTube channel, a blog author, a podcast),
created at `wiki/knowledge/entities/<origin-slug>.md`. Tracked via the `channel:` field on
source pages.

| Section | Purpose |
|---|---|
| `## Summary` | Who they are |
| `## What They Produce` | Subject matter, language, format |
| `## Quality` | Your own evaluation — reliability, blind spots, where they're worth trusting |
| `## Sources` | Auto-updated list of all ingested sources from this origin |

Channel entities do **not** get `## Relations`, `## When to Use`, or `## Compared To` — those
don't fit a producer.

The `## Quality` section is the point of these pages. Three sources in, you have an opinion
about whether this origin is reliable; writing it down is what stops you re-forming it every
time.

---

## Checklist

- [ ] Source page created with `## Content` embedded (or `content-exempt` tagged and justified)
- [ ] Entities proposed, not silently created
- [ ] Entity Placement Rule applied per entity
- [ ] Two-way links in place
- [ ] Predicates drawn from the controlled vocabulary
- [ ] Channel trigger checked (3rd source from this origin?)
- [ ] Reference only if 4+ entities compared **and** human approved
- [ ] `index-knowledge.md` updated
