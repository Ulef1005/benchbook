# Keeping It Honest

A knowledge base maintained by an eager agent has two failure modes, and they pull in
opposite directions.

**Rot:** entries stop being written, pages go stale, the record quietly stops matching
reality. This is the one everybody expects.

**Bloat:** the agent writes *too much*, in the wrong places, duplicating itself. Pages grow
past the point of usefulness. The log fills with narrative. The todo list mirrors things that
then drift from their sources. This is the one that actually happens, and it's worse, because
a rotting wiki looks empty and a bloated one looks productive.

This document is the set of rules that came out of hitting the second one repeatedly, with
the numbers that caused each change. It's the most useful thing in this repo, because it's
the part you can't get from designing a schema on a whiteboard.

---

## Rule 1 — `update` is not a valid log operation

**The rule:** the central log accepts exactly five operations — `ingest`, `create`, `lint`,
`query`, `skill`. Each entry is 1–3 lines, ~40 words maximum. There is deliberately no
`update` operation.

**What went wrong.** `update` existed originally, and it was the escape hatch. Anything that
didn't fit the other four became an `update`. An audit found **17 of 26 recent entries were
`update`, averaging 139 words against a 1–3 line spec** — and most of them duplicated text
that had already been written onto a project page in the same session. The log was growing
roughly ten times faster than intended, and re-reading it was no longer a fast way to orient.

**The fix,** which is the generalisable part: things that felt like `update` almost always
belonged somewhere more specific.

| The change | Where it actually belongs | Why not the log |
|---|---|---|
| Project progress, decisions, build narrative | that project's own `## Log` section | you'd look for it on the project page, not by date |
| Infrastructure or entity state change | that entity's `## Change History` | the entity page is the single source for its own state |

The heuristic that fell out: **if an event seems to need a long log entry, that's the signal
it belongs on a page instead** — with at most a one-line pointer from the log.

---

## Rule 2 — the todo list points, it doesn't mirror

**The rule:** the central todo file links to project pages rather than copying their open
items. Project todos live on the project page and nowhere else.

**What went wrong.** It used to mirror them, on the theory that one list of everything is
convenient. A lint pass found **60 of roughly 76 mirrored items had drifted from the pages
they were copied from** — closed on the page but still open in the list, reworded, or
referring to a phase that no longer existed.

**The lesson:** any duplicated state will diverge, and it will diverge silently, and you will
trust the wrong copy. If two places show the same fact, one of them must be a link.

---

## Rule 3 — a rule that flags a quarter of your content is not a rule

**The rule:** split pages beyond roughly 500 words — measured *excluding* append-only
sections, with explicit exemptions for page types whose length is inherent, and a higher
threshold for dense reference pages.

**What went wrong.** The original version was just "keep pages concise, split beyond ~500
words." It turned out **27% of all pages breached it**. A check that fires on a quarter of
your content is noise: you stop reading the output, and the rule steers nothing.

**The fix** was to make it measurable rather than to relax it:

- **Exclude append-only sections** from the count. A project's build history growing over two
  years is not bloat; that's the page working correctly.
- **Exempt page types where length is inherent.** A page that transcribes a 10,000-word
  external source shouldn't be split into ten — that damages it. Same for page types whose
  own template mandates six-plus sections.
- **Raise the threshold for operational hub pages**, which are dense on purpose. Splitting one
  lookup into three is a downgrade, not a cleanup.
- **Show only the worst offenders** in the report, and treat the rest as a standing backlog
  with a known count.

The general form: when a check fires constantly, the usual problem is the check, not the
content. Fix the measurement before you fix the pages.

---

## Rule 4 — never link the raw folder from a page body

**The rule:** page bodies link to online URLs. The path to the local raw file lives in
frontmatter only.

**Why:** raw files get archived after 14 days. A body link to one is a link that will break,
and a page full of dead links teaches you to stop clicking links.

---

## Rule 5 — deployed code must be committed before the session ends

**The rule:** for code that lives in a live checkout on a server, an edit isn't done until
it's committed and pushed, in the same session.

**What went wrong:** a live checkout is not an auto-committing daemon. A hotfix applied in the
field and left uncommitted looks fine — the service runs — right up until the next deploy
overwrites it, or the next person reads the repo and sees code that isn't what's running.
Silent divergence between "what's deployed" and "what's in git" is the same bloat failure in
a different costume: two copies of a truth, drifting.

There's a matching gotcha the contract records: never in-place-edit a symlinked path in a
live checkout, because it replaces the symlink with a plain file and quietly breaks the link
back to the repo.

---

## The human gates

Everything above is about what the agent writes. This section is about what it isn't allowed
to do alone.

**Ask before creating pages.** During an interactive session the agent proposes a page and
waits. This sounds slow and isn't — most proposals are accepted in a word — but it keeps a
human in the loop on the shape of the knowledge base rather than only its contents.

**Flag contradictions, never silently overwrite.** When new input disagrees with what's on a
page, both versions get surfaced and the human decides. This is the single most important
gate. An agent that resolves conflicts on its own is an agent that can quietly delete the
correct answer.

**Propose schema changes; don't make them.** The contract is co-owned. The agent can argue
for a rule change — and should — but only a human commits it.

**The No-Deletion Rule.** Before deleting a file or dropping content during a rewrite, the
agent must name what's about to be lost and ask where it should go. Applies to migrations,
to content that doesn't fit the target page, and to links that would break.

**References need approval and a threshold.** Comparison pages are only created with human
sign-off *and* only when they'd actually compare enough things to be worth the page. When new
information affects an existing one, the agent flags it rather than editing it.

---

## LINT is report-only, on purpose

The maintenance pass reads the whole wiki, runs mechanical checks plus judgement-based ones
(is this entity in the right place? does this page contradict that one? is this stale?), and
writes a dated report.

**It does not edit page bodies or frontmatter.** Ever.

It has write access to exactly two mechanical operations, both of which only move files and
never delete them: archiving raw source files older than 14 days, and archiving the oldest log
entries once the log exceeds a length threshold.

This is a deliberate constraint and it's worth copying. An auto-fixing linter over
natural-language content is a machine for introducing subtle, unreviewed changes across
hundreds of files at once. Reporting keeps the agent's judgement in an advisory role, where
it's genuinely useful, and keeps the human as the only writer of record for anything
requiring judgement.

Mechanical, unambiguous checks — missing frontmatter fields, broken relative links, files in
the wrong folder for their declared type — run as a plain script rather than as model
judgement. Cheaper, deterministic, and it can be run on every commit.

---

## The pattern behind all of these

Each rule above started as a reasonable-sounding convention and failed in the same way: it
allowed two copies of something to exist, or it produced output nobody read.

So the two questions worth asking of any rule you add:

1. **Does this create a second copy of a fact?** If yes, one of them has to become a link.
2. **What percentage of content will this flag?** If it's more than a few percent, the rule
   isn't ready — it will train you to ignore its output.

---

**Next:** [12 — Case Studies](12-case-studies.md) — four things built and tracked with this
system, including the parts that didn't work.
