# Indexes

This is the retrieval layer. There is no vector database, no embedding pipeline, and no
search infrastructure.

Instead there are index files: catalogues of what exists, each entry a link plus a one-line
summary. The agent reads the relevant index *before* answering anything, uses it to decide
which pages to open, and then opens them.

That's it. It works better and further than people expect.

---

## Why not embeddings

The honest answer is that for a personal wiki, the index approach wins on nearly every axis
that matters:

- **It's inspectable.** You can read the index. When retrieval goes wrong, you can see why,
  because the thing that failed is a list you can look at rather than a similarity score you
  can't.
- **It's exact.** No near-misses, no semantically-adjacent wrong page.
- **There's nothing to maintain.** No re-indexing, no stale embeddings after an edit, no
  infrastructure that breaks in six months.
- **The summaries do work embeddings can't.** A one-line human-readable summary written at
  filing time carries intent — "this is the page where the decision got made" — which a chunk
  embedding does not encode.
- **It degrades legibly.** When the index gets too big, you notice, because reading it is
  slow. An embedding index degrades silently by returning slightly worse matches.

The tradeoff is real: this doesn't do fuzzy full-text search over page bodies. When you
genuinely need that, add a search tool as a supplement — the index stays the primary map.

---

## The split, and why it happened

The original design was one index file. That's what the pattern this system came from
describes, and it notes the approach works well at roughly hundreds of pages.

The live wiki is at 1,597. Well past that.

The fix wasn't embeddings — it was splitting the index by domain:

```
index.md                  ← master, ~50 lines. People, pointers to domain indexes, meta.
index-<domain>.md         ← one per domain. The full catalogue for that domain.
```

The master index changes only when a whole domain or meta page is added, so it's stable and
tiny. Domain indexes grow with their domain, and you only ever load the one you need.

The read path becomes:

1. Master index → which domain is this about?
2. That domain's index → which pages?
3. Those pages.

Cost is roughly flat as the wiki grows, because step 2 only ever loads one domain's catalogue.

The books domain went a step further and split again — separate indexes for authors, series
and candidates — once it alone passed 700 pages. That's the same move applied recursively, and
it's the answer whenever one index gets uncomfortable: **split on the axis you actually query
by.**

---

## Format

Each index is a flat list, grouped by page type:

```markdown
### Entities

- [Some Thing](home/entities/some-thing.md) — one-line summary of what it is and why it matters
- [Another Thing](home/entities/another-thing.md) — one-line summary
```

Frontmatter marks it as an overview page for the domain.

Two things carry the weight here:

**The one-line summary is the actual retrieval signal.** It should say what the page is *for*,
not restate the title. "Comparison of four options, decided on the second one" beats "notes
about options." Writing these lazily is the main way this approach fails.

**Order is by type, not alphabetical.** Sources, entities, references, projects. The agent is
usually looking for a kind of thing, and grouping by kind means it can skip whole blocks.

---

## The second axis: relations

Indexes answer *what exists, by subject*. They do not answer *what is connected to this*, and
that is a different question you ask constantly — what runs on this host, what backs this up,
what did that decision affect.

That's what the `## Relations` tables are for. Every page that has one carries rows of
`Subject | Predicate | Object`, with predicates drawn from a controlled 36-term vocabulary, and
together they form a small typed graph across the whole wiki. It is not a second index; it's a
second *axis* over the same pages, and it earns its keep the moment the answer you need spans
folders.

**One rule shapes everything about how it's read: each fact is stored exactly once**, on
whichever page it reads most naturally on. The alternative — writing both directions — is the
mirroring failure from [11 — Keeping It Honest](11-keeping-it-honest.md) wearing a different hat,
and it would drift the same way.

The consequence is that **a page's own table shows only about half of what the wiki knows about
it.** So the graph is read with a script rather than by opening the page:

```bash
./scripts/relations.py esphome        # inbound AND outbound edges, wherever they're stored
```

Depth 1 — direct neighbours — is the usable unit and is what the project skills run
automatically. Deeper walks answer "what is the blast radius of changing this", which is a real
question and a much bigger answer.

**Why a controlled vocabulary rather than free text.** Because a free predicate field becomes
unqueryable within months. That is not a prediction; it's twice-measured. The first drift was
synonyms — `is_made_by`, `produced_by` and `made_by` all live for the same relation. The second
was worse and is the more useful story: the check enforcing the vocabulary had been scoped to a
single folder, reported clean for months, and when the graph was finally measured end to end,
**185 of 709 relations sat outside that scope carrying 124 off-vocabulary predicates** — `backed
up by` on eight pages against `backed_up_by` on one. "What backs up this service?" had no answer
a script could give.

The repair doubled the vocabulary to 36 terms, every added pair justified by at least three rows
of evidence already in the wiki. Extend a vocabulary from drift you can see, not from cases you
can imagine.

---

## The rules that keep it working

**Never preload indexes.** The contract explicitly tells the agent *not* to read indexes at
session start. They're read at the point of use, by the operation that needs them. A session
where you only edit one project page shouldn't pay for nine domain catalogues.

**Update the index in the same operation that creates the page.** Not later, not in a batch.
An unindexed page is functionally invisible — it exists on disk and the agent will never find
it. The lint pass flags orphans for exactly this reason.

**The master index changes rarely.** If you're editing it often, something is miscategorised.

---

## When this will stop working

Being honest about the ceiling:

- A single domain index somewhere in the low thousands of entries starts getting expensive to
  read. The books split happened around 700 and was comfortable.
- Questions that genuinely span every domain at once are the weak case — the agent either
  reads many indexes or guesses which ones matter.
- Finding a specific phrase inside page bodies is not what this does. That's a search tool's
  job, and adding one alongside is reasonable.

None of these are near-term problems for a personal wiki, and all of them have a next move
that isn't "install a vector database."

---

**Next:** [07 — Operations](07-operations.md).
