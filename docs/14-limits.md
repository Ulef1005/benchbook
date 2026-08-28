# Limits

## What it's bad at

Honest list, from actually running it.

### It is not autonomous

The human gates are load-bearing, not training wheels. Someone confirms the domain, approves
new pages, resolves contradictions, and signs off on plans. Remove those and the failure isn't
that it stops working — it's that it keeps working while quietly becoming wrong, which is
worse.

If you want a system that files things unattended, this isn't it.

### Bulk imports distort everything

The books domain is roughly **47% of all pages** in the live wiki, from one library import.
That's not a problem in itself, but it means page counts stop reflecting where the value or
the work is, and one domain's conventions end up over-represented in anything measured
wiki-wide.

Import in bulk if you need to. Just don't trust aggregate statistics afterwards.

### The schema sprawls at the edges

Five page types in the live wiki have **exactly one page each** — types created for a single
document that never recurred. Each was locally reasonable and collectively they're clutter,
because a type with one instance is just a page with extra ceremony.

The Entity Placement Rule catches this for entities; nothing currently catches it for types.
A periodic "which types have fewer than three pages?" check would.

### Backlogs form and persist

At last count: **86 pages** over the length threshold, as a standing backlog, and **59
reference pages** slated for lazy conversion to entities whenever they're next touched.

Both are deliberate — lazy migration beats a big-bang rewrite, and a flagged backlog beats a
rule everyone ignores. But "lazy" means some of those pages will still be waiting in a year.
A backlog that only drains on contact never fully drains.

### Retrieval has a real ceiling

The index approach is better than it sounds and it isn't infinite. A single domain index in
the low thousands of entries gets expensive to read; questions genuinely spanning every domain
are the weak case; and finding a phrase inside page bodies isn't what this does at all. See
[06 — Indexes](06-indexes.md) for what to do about each.

### It requires a specific kind of tool, and a specific kind of person

You need an agentic tool with real filesystem access — one that can read and write many files
in a repo in a single pass. Which tool doesn't matter; a chat window you paste into does.

And you have to be willing to edit the contract. The shipped one is sanitized, but it is not
neutral — the page-length thresholds, the 4-entity reference rule, the predicate vocabulary
and the log's five operations are all *opinions*, formed against one person's material.
Adopted wholesale and never questioned, they'll steer you toward someone else's conventions,
and you'll experience that as the system being subtly wrong without being able to say why.

The contract is meant to be argued with. That's why it's a file in your repo rather than a
setting in a product.

### The first month is the hard part

The wiki is worth much more at month six than month one, and the work is front-loaded. Early
on you're writing pages and getting little back, because there's nothing to cross-reference
and no accumulated context to query. The payoff arrives when you first ask something and get
an answer assembled from four pages you'd forgotten writing.

That gap is the main reason people abandon this pattern. Knowing it's there helps.

---

## What it's genuinely good at

For balance, the things it does better than the alternatives:

- **Preserving reasoning.** Decisions with their rejected alternatives, at the moment you knew
  why. Nothing else captures this.
- **Recording negative results.** The failure pages are the highest-value ones, and the agent
  will write them when you wouldn't.
- **Surviving tool changes.** Markdown in git outlives whatever you're using to edit it.
- **Cross-domain connection.** Noticing that a decision in one project affects another is
  exactly the bookkeeping humans skip.
- **Being readable without the agent.** Which matters most on the day the agent is wrong.

---

**Back to:** the [README](../README.md).
