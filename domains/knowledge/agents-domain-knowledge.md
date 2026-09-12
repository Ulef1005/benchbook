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

Predicates in a `## Relations` triplet table must come from this list, **on every page that
carries one** — not only knowledge entities. LINT flags anything else. **If a fact doesn't fit
any predicate, it's usually a discrete attribute — put it in `## Key Facts` rather than forcing
a relation.** That rule is load-bearing: an object that is prose rather than a page
(`monitors → "5 backup units, 2 workflows, 3 timers"`) is not a triple at all, however well the
predicate fits.

### Core — 18 predicates

The set that applies to any wiki, whatever you keep in it.

| Predicate | Meaning | Inverse |
|---|---|---|
| `is_a` | type / category membership | — |
| `made_by` | manufactured / created by a commercial maker | `makes` |
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
| `evaluates` | project/person **assessing, adopting, changing or deciding about** the entity. **This is the project→entity predicate** — see below | `evaluated_for` |
| `evaluated_for` | entity → the project/person assessing, adopting or changing it | `evaluates` |
| `compared_to` | weighed side-by-side for reference (symmetric) — **not** necessarily rivals; use `competes_with` for actual alternatives | — |

### Provenance and ownership — 8 predicates

| Predicate | Meaning | Inverse |
|---|---|---|
| `built_by` | entity → **your own project** that built, wrote or revised it. **Not `made_by`**, which means a commercial manufacturer: a bike is `made_by` its brand, whereas a podcast you generate is `built_by` the project that generates it | `builds` |
| `builds` | project → the artifact it produced | `built_by` |
| `owns` | person → the thing they own. The only person-facing predicate; use it where the owner actually matters | `owned_by` |
| `owned_by` | entity → its owner (a page in `wiki/people/`, or the household) | `owns` |
| `feeds` | data source → the consumer it supplies. Kept separate from `uses` because it records **provenance and direction of data flow**, not dependency | `fed_by` |
| `fed_by` | consumer → its data source | `feeds` |
| `triggered_by` | entity → what causes it to run (scheduler, bot command, event). Not `fed_by`, which is about data arriving rather than invocation | `triggers` |
| `triggers` | scheduler/trigger → what it invokes | `triggered_by` |

### Operations — 10 predicates *(only if you run services)*

**Skip this block if you don't operate infrastructure.** These five pairs exist because the
wiki this came from documents a home server fleet, and they're load-bearing *there* — but on a
wiki about books, recipes or research they will never fire. Dropping them costs nothing; LINT
only flags predicates you *use* that aren't listed, never predicates you don't use.

| Predicate | Meaning | Inverse |
|---|---|---|
| `backed_up_by` | entity → what protects its data. Deliberately not `uses`: a service does not *employ* a backup tool, it is *protected by* it — and that distinction is what makes a backup gap visible | `backs_up` |
| `backs_up` | backup system → what it protects | `backed_up_by` |
| `secures` | secret/credential store → what it holds secrets for | `secured_by` |
| `secured_by` | entity → where its secrets live | `secures` |
| `monitors` | observability tool → what it watches | `monitored_by` |
| `monitored_by` | entity → what watches it | `monitors` |
| `fronts` | reverse proxy → the service it exposes | `fronted_by` |
| `fronted_by` | service → the proxy in front of it | `fronts` |
| `stores_data_on` | entity → where its data physically lives. Distinct from `uses`: it answers *"what breaks, and what is lost, if that storage dies"* | `stores_data_for` |
| `stores_data_for` | storage → whose data it holds | `stores_data_on` |

The subject of a row does not have to be the page's own entity — pick the direction that reads
naturally and use the inverse predicate when needed. **Each fact is stored exactly once**, on
whichever page reads naturally, which is why a page's own table shows only half its relations
and why `scripts/relations.py` exists (see below).

### Which predicate for a project → entity relation?

**`evaluates`**, unless something more specific clearly fits. It is the *general* project→entity
predicate, not a purchase-only one: it covers assessing, adopting, rejecting and changing, and
it covers resolved outcomes as well as open ones — a project that dropped a tool still
`evaluates` it, and a migration project `evaluates` the deployment it is migrating.

Reach for `uses` when the project genuinely depends on the entity to run, `builds` when it
produces it, `replaces` when it supersedes it. Otherwise `evaluates`.

> This wording is the result of getting it wrong. The definition originally read *"project/person
> considering the entity (e.g. purchase decision)"*, which was narrower than ten months of actual
> use — narrow enough that a proposal for a new `targets`/`targeted_by` pair got written before
> anyone noticed `evaluates` already did the job. The fix was to widen the definition, not to add
> the pair. Worth copying as a habit: when a vocabulary looks like it has a gap, check whether an
> existing term is just described too tightly.

### Why a controlled vocabulary

In the original wiki this list was derived after the fact, from 66 existing entity pages, and
the derivation immediately surfaced synonym drift — `is_made_by` / `produced_by` / `made_by`
all in use for the same relation. Left alone, a free predicate field becomes unqueryable within
months.

**It drifted again three months later, and the second drift is the more useful lesson.** The
LINT check that enforces this vocabulary was scoped to knowledge entity pages, because that's
where relations started. By the time anyone measured, **709 triples existed and 185 of them sat
outside that scope, carrying 124 off-vocabulary predicates no check could see** — `backed up by`
on eight pages against `backed_up_by` on one, `runs on` beside `runs_on`. Inside the old scope,
0 of 524 rows were off-vocabulary: the check worked perfectly everywhere it looked, which is
exactly what made it hard to notice it wasn't looking everywhere.

So: **the vocabulary applies wherever the table appears, and the check's scope must match the
rule's scope.** A check that is right about the region it inspects is not the same thing as a
check that is right.

The repair took the vocabulary from 18 predicates to 36. Every pair added had to carry **at
least three rows of independent evidence** already present in the wiki — the pairs were derived
from the drift, not invented for completeness. Two candidates were declined on that basis
(`deployed_for`, because `part_of` already read correctly; `documented_by`, because `## Sources`
is where that belongs), and one pair was adopted at only two rows as a deliberate, flagged
exception. That is the bar worth copying: **extend the vocabulary from evidence you already
have, not from cases you can imagine.**

### Querying the graph

`./scripts/relations.py <page-slug>` reports a page's inbound *and* outbound edges. You need it
because each fact is stored exactly once — reading a page's own `## Relations` table shows you
roughly half of what the wiki knows about it.

```
./scripts/relations.py esphome              # inbound + outbound, depth 1
./scripts/relations.py hallway-display --depth 2   # walk two hops
./scripts/relations.py --orphans            # pages with no edges either way
```

**Depth 1 is the usable unit.** Depth 2+ grows fast and is for the rare "what is the blast
radius of this change" question, not for orientation. Traversal deliberately never follows the
three symmetric predicates (`integrates_with`, `competes_with`, `compared_to`) — each is a
2-cycle by definition, and walking them turns a neighbourhood into the whole graph. They're
still reported at depth 1, where they're useful.

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
