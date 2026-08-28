---
name: research
description: "Research a topic across multiple sources, synthesise what's actually being said, then optionally file the result as a wiki source page. Use when the user says 'research [topic]', 'what's new with [topic]', 'what are people saying about [topic]', 'look up recent discussion on [topic]', or wants fresh external research captured into the wiki. Presents takeaways first, then asks whether to ingest — as a source-only page or a full INGEST with entity pages."
license: MIT
metadata:
  version: 1.0.0
  category: knowledge
---

# Research

## Purpose

The pattern: **acquire → synthesise → offer to file.**

That last step is the one that matters. Research that stays in the chat window is research
you'll redo in four months, pay for again, and possibly reach a different conclusion from for
no good reason.

---

## Step 1 — Sharpen the question

Restate what you're about to search for, and confirm it if it's ambiguous.

"Research Kubernetes" is not a question. "Which lightweight Kubernetes distribution suits a
three-node ARM cluster" is. The difference decides whether the output is a wall of general
background or something you can act on.

Ask what the research is *for* — a purchase, a build decision, general orientation. That
changes what counts as a good answer.

---

## Step 2 — Gather from several angles

Use whatever search and fetch capability your tool has. **Vary the angle rather than repeating
the same query** — different sources surface different things:

| Angle | Finds |
|---|---|
| General web / docs | The official story, current versions, stated capabilities |
| Discussion forums | What breaks in practice, and what people migrated away from |
| Code hosting | Whether it's actually maintained — last commit, open issue count, release cadence |
| Comparisons and reviews | The alternatives you didn't know to consider |

**Check recency explicitly.** A confident three-year-old blog post ranks well and may describe
software that no longer works this way. Note the date on anything load-bearing.

**Note what you couldn't find.** A gap is a finding — "no one seems to have written about
running this on ARM" is genuinely useful and stops the reader assuming you checked.

---

## Step 3 — Synthesise, and separate fact from consensus

Present:

1. **What the thing is** — brief, only if the user needs orienting
2. **Key takeaways** — 5–10, each concrete
3. **Where sources disagree** — explicitly. This is the most valuable part
4. **Maintenance and recency signals** — is this alive?
5. **What you couldn't establish**

Distinguish clearly between **what's documented**, **what people report**, and **what you're
inferring**. Those are three different confidence levels and flattening them produces
confident-sounding mush.

Cite as you go. Every load-bearing claim should be traceable to where it came from.

---

## Step 4 — Offer to file it

Ask, with a recommendation:

| Option | When |
|---|---|
| **Source page only** | Orientation research, no clear entities yet |
| **Full INGEST** | The research identified specific tools/products worth their own entity pages |
| **Don't file** | Genuinely throwaway — a quick factual lookup |

Recommend filing whenever the research informed a decision. **The reasoning behind a decision
is the thing nothing else captures**, and in three months you won't remember why the popular
option lost.

---

## Step 5 — If filing, hand off to INGEST

Follow `agents-core.md § 3 INGEST` — domain is almost always `knowledge`:

- Source page at `wiki/sources/<slug>.md` — `## Summary` → `## Key Takeaways` → `## Sources`
- `source_url:` is the primary source; list the rest under `## Sources`
- Propose entity pages for anything that recurs across sources — approval required per entity
- A **reference page only if 4+ options were genuinely compared**, and only with approval
- Two-way link entities and the source
- Update `wiki/index-knowledge.md` and append one `ingest` line to the log

**Never fabricate a source.** If a claim came from your own knowledge rather than something you
fetched, say so on the page — `agents-core.md` requires disclosing non-wiki sources, and that
applies to research just as much as to answering a question.

---

## Note on tooling

This skill is deliberately vague about *which* search tools to use — it works with whatever
your agent has. If you have specialised research tooling, name it here in your own copy; the
procedure above is what matters, not the plumbing.
