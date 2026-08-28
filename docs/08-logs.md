# Logs

One chronological, append-only file recording what happened to the wiki and when.

It looks trivial and it carries a surprising amount of weight, because it answers a question
nothing else does: **what was I doing, and when?** Indexes tell you what exists. Pages tell
you what's true. Only the log tells you the shape of the last three months.

---

## Format

```markdown
## [YYYY-MM-DD] <op> | Subject

One to three lines. Roughly forty words maximum.
```

Newest entries append at the bottom. Five valid operations, and no others:

| Op | When |
|---|---|
| `ingest` | External material was processed into the wiki |
| `create` | A page was created |
| `lint` | A maintenance pass ran |
| `query` | A significant question was answered |
| `skill` | A skill was run |

The consistent prefix is deliberate — it makes the log parseable with ordinary shell tools:

```bash
grep "^## \[" log.md | tail -10
```

Ten seconds, no tooling, and you know what's been happening. That property is worth
protecting; it's why the format is rigid.

---

## Why `query` belongs here

Four of the five operations change files, so git already records them. `query` doesn't — you
asked something, got an answer, and nothing on disk changed.

That makes queries the one class of event git genuinely cannot reconstruct, and therefore the
one with the strongest claim on a log entry. A question you needed answered is real
information about what you were working on.

It also pairs with a habit worth building: **if a query produced a substantial answer, file it
as a page.** Otherwise you'll ask it again in four months, pay for it again, and possibly get
a different answer.

---

## What does *not* go here

This is the part that took a failure to learn, and it's the most transferable thing in this
document.

There is deliberately **no `update` operation.**

`update` existed originally. It was the escape hatch: anything not clearly one of the other
four became an `update`. An audit found **17 of 26 recent entries were `update`, averaging 139
words against a 1–3 line spec** — and most duplicated text already written onto a project page
in the same session. The log was growing roughly ten times faster than intended and had
stopped being fast to skim, which was its only job.

Removing the operation forced every one of those events somewhere better:

| The event | Where it belongs | Why not the log |
|---|---|---|
| Project progress, decisions, build narrative | that project's own `## Log` section | you'd look for it on the project page, not by date |
| Infrastructure or entity state change | that entity's `## Change History` | the entity page is the single source for its own state |

The resulting heuristic, which generalises well beyond this system:

> **If an event seems to need a long log entry, that's the signal it belongs on a page
> instead** — with at most a one-line pointer from the log.

---

## Three logs, not one

Worth being explicit, because the naming collides:

| Log | Scope | Order |
|---|---|---|
| The global log | Wiki-structural events | Newest at bottom |
| A project's `## Log` | That project's progress and decisions | Newest at bottom |
| An entity's `## Change History` | That thing's state changes | **Newest at top** |

The ordering inconsistency is intentional. The global log and project logs are read as
timelines, front to back. A change history is read top-down to answer "what changed most
recently," so the newest entry goes where your eye lands first.

---

## Archival

When the global log passes a length threshold, the oldest entries move to a dated archive file
until it's back under a working size. Entries are never deleted — only relocated.

This is one of exactly two write operations the lint pass is permitted to perform, and like the
other one it only moves things. See [11 — Keeping It Honest](11-keeping-it-honest.md).

---

**Next:** [09 — Projects](09-projects.md).
