# Keeping It Honest

A knowledge base maintained by an eager agent has two failure modes, and they pull in
opposite directions.

**Rot:** entries stop being written, pages go stale, the record quietly stops matching
reality. This is the one everybody expects.

**Bloat:** the agent writes *too much*, in the wrong places, duplicating itself. Pages grow
past the point of usefulness. The log fills with narrative. A central list mirrors things that
then drift from their sources. This is the one that actually happens, and it's worse, because
a rotting wiki looks empty and a bloated one looks productive.

There is a third, quieter one that only shows up later: **the maintenance layer itself rots.**
The rules, checks and skills you build to prevent the first two go stale, get bypassed, or turn
out never to have run. Rule 6 below is about that.

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

## Rule 2 — there is no todo list

**The rule:** open work lives on the page the work belongs to. Project todos in that project's
`## Open Questions`, entity todos on the entity page, contradictions in a review queue that LINT
drains before it looks for new work. There is no central list.

This rule was wrong twice before it was right, and both failures are instructive.

**Version 1 — the mirror.** A single todo file copied open items out of project pages, on the
theory that one list of everything is convenient. A lint pass found **60 of roughly 76 mirrored
items had drifted from the pages they came from** — closed on the page but still open in the
list, reworded, or pointing at a phase that no longer existed.

The lesson looked obvious: any duplicated state will diverge, silently, and you will trust the
wrong copy. If two places show the same fact, one of them must be a link.

**Version 2 — pointer-only.** So the file stopped copying and started linking: names of projects,
plus a hand-curated section for wiki-meta decisions and deferred items. No duplication. This
held for months and felt correct.

It was still wrong, just more slowly. Measured four separate times across four weeks, **roughly a
third of the remaining entries had a stale or wrong premise.** The worst of it was the *Deferred*
section, the part that couldn't drift because nothing else owned it: of the last five items,
**every single one** turned out on inspection to be already done, already decided, or resting on
something that had stopped being true. One had been waiting on a condition that was met the day
after it was filed.

**The lesson that actually generalises** is sharper than "don't duplicate state":

> **A file whose whole job is to tell you what is open, and which is a third wrong, is worse than
> no file — because you trust it.**

An empty spot in the wiki prompts you to look. A confident, stale list stops you looking. The
pointer-only version fixed the drift and left the rot, because the rot was never about
duplication — it was about a list whose entries no one was responsible for re-reading. Both
versions were a second index over work that already had a home.

**What replaced it.** Nothing, deliberately. Every item moved to the page that owns it, where
you'd have looked for it anyway, and where whoever touches that page next is forced to walk past
it. If you want one view of everything open, *generate* it — `grep` the unchecked boxes out of
the `## Open Questions` sections across the project folder. A derived view can only be stale for
as long as it takes to re-run it.

**The one list that survived** is the review queue (`wiki/log/review.md`), and the reason it
survives is that it holds exactly one kind of item — a contradiction that needs a human decision
— and LINT is required to drain it before it does anything else. It has an owner and a clearing
mechanism. That's the test worth applying to any standing list you're tempted to keep: **who is
obliged to empty this, and when?** Without an answer, you're building version 2 again.

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

## Rule 6 — the agent's own tooling rots too, and nobody checks it

Everything above is about the wiki. This one is about the layer you build to maintain the wiki,
which turns out to rot the same way and is much easier to ignore — because it isn't content, so
no content check looks at it.

**The rule:** the skill directory on disk is the source of truth. Any page that lists your
skills is a **view** over it, and a mechanical check fails when the two disagree in either
direction — a skill with no listing, or a listing with no skill.

**What went wrong.** Three separate pages ended up claiming to be the roster, which meant three
manual audits in five weeks and three different answers. The documentation step that was
supposed to keep them in step had a measured **29% miss rate** — not because anyone was careless,
but because it was unenforced prose in a checklist, and unenforced prose is a suggestion.

This repo was not exempt. The first run of the ported check found `benchbook-design` shipping in
`.claude/skills/` and listed in no roster at all, two weeks after it landed.

**The generalisable part** is not "keep your docs in sync". It's:

> **A stated fact that a script can verify should be verified by a script.** If it can't be, the
> claim is an opinion, and you should write it as one.

"The roster lists every skill" is checkable in four lines of code. So it gets checked, and the
sync step stops depending on anyone remembering.

**Two fields make the rest mechanical.** `maturity: draft|tested|hardened` separates *"unused
because new"* from *"unused because dead"* — states that look identical from usage data and
demand opposite responses. `outputs: <glob>` names the page shape a skill produces, which turns
"is this repeated work already covered?" into a comparison against git history rather than a
judgement call. Both are one line of YAML; both are in [10 — Skills](10-skills.md).

**The detector's first real output was nothing.** Run against four and a half months of history,
it reported zero new-skill candidates and one bypass. That is the result being reported honestly,
and it belongs here rather than in a list of wins: a maintenance check that has to justify itself
with findings will find some. `Clean — nothing to observe` must be a blessed output, or you have
built a machine for generating work.

**One thing deliberately did not ship.** The version of this running in the source wiki also
harvests session transcripts to count invocations. That reads a specific tool's private files,
and this repo has been tool-agnostic since the day it went public — so the transcript layer
stayed behind and only the parts that run on git and the filesystem travelled. Worth naming as a
general habit: when you port a system, the parts that assume your particular setup are the parts
that will quietly break for everyone else.

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
the wrong folder for their declared type — run as a plain script (`scripts/lint.py`) rather than
as model judgement. Cheaper, deterministic, and repeatable, which is the one property a check
cannot do without.

**Those checks, and only those, gate commits.** `scripts/pre-commit.sh` runs the script and
blocks on errors. Warnings never block. The judgement checks are not involved at all — they need
a model, and a commit hook that needs a model is a commit hook people disable within a week.

The line between "advisory" and "blocking" is drawn at *does this require an opinion*. A missing
required field has exactly one correct answer, so a machine may refuse the commit. Whether two
pages contradict each other does not, so a machine may only mention it. Getting that boundary
wrong in either direction is costly: gate on judgement and people bypass the gate habitually;
gate on nothing and the deterministic failures accumulate anyway.

---

## The pattern behind all of these

Each rule above started as a reasonable-sounding convention and failed in one of three ways: it
allowed two copies of something to exist, it produced output nobody read, or it was a claim
nothing ever checked.

So the four questions worth asking of any rule you add:

1. **Does this create a second copy of a fact?** If yes, one of them has to become a link.
2. **What percentage of content will this flag?** If it's more than a few percent, the rule
   isn't ready — it will train you to ignore its output.
3. **Who is obliged to re-read this, and when?** A rule that produces a standing list nobody
   owns produces a stale list, and a stale list is worse than an empty one. If the answer is
   "whoever notices", the rule needs a mechanism, not better wording.
4. **Can a script verify it?** If yes, it should — an unenforced convention has a measurable
   miss rate, and in this wiki that number was 29%.

---

**Next:** [12 — Case Studies](12-case-studies.md) — four things built and tracked with this
system, including the parts that didn't work.
