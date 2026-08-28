# Projects

A project page tracks something you're building. This is the page type that diverges most
from the pattern this system came from, whose examples are research, reading and team
knowledge — all of which are about things you're *learning*.

Building is a different shape. It has state, it has a lifecycle, and its most valuable content
isn't the summary — it's the decision record, including the options that lost.

---

## Required sections

Every project page carries these, in order, and the lint pass checks for them:

| Section | Content |
|---|---|
| `## Summary` | 2–4 sentences. What this is and why. |
| `## Use Cases` | What it needs to actually do, concretely. |
| `## Hard- and Software` | Options considered, in a table, with pros and cons — then a "Selected" subsection. Supporting infrastructure links to entity pages. |
| `## Plan / Phases` | Implementation phases with checkboxes. **Gated — see below.** |
| `## Open Questions` | Unresolved decisions blocking progress. |
| `## Log` | Chronological, append-only. |

Deployed software projects additionally require `## Version Control`, `## Backup Concept` and
`## Cron Jobs`. Those three exist because they are precisely what you fail to write down and
desperately need eighteen months later, at which point the answer is a forensic exercise.

The `## Hard- and Software` options table is quietly the most valuable section in the whole
system. It's where "why not the obvious alternative?" gets answered, permanently, at the
moment you actually know the answer.

---

## The plan approval gate

The strongest human-in-the-loop rule in the system, and the one I'd most encourage copying:

> While a project is in `planned` status, `## Plan / Phases` contains only a high-level phase
> list marked *"Deferred — awaiting manual plan approval."* **No implementation work may
> begin** — no code, no files, no API calls — until the human explicitly approves the plan.
> On approval, status moves to `active` and the plan is written out in full.

The problem this solves is specific to agentic tools and immediately recognisable: you
describe an idea, and forty seconds later there are eleven files. They're plausible. Some are
even good. But you never made the architectural decisions — they were made for you, at speed,
and now they're load-bearing and you're reviewing them backwards.

The gate forces the plan to be a separate, reviewable artifact from the execution. It costs
one round trip and it is worth it every single time.

---

## Status lifecycle

```
planned → active → deployed / completed
   ↓         ↓
on-hold   abandoned
```

| Status | Meaning |
|---|---|
| `planned` | Specified, plan not yet approved. Nothing built. |
| `active` | Approved, in progress. |
| `on-hold` | Deliberately paused. **Reason recorded.** |
| `deployed` | Running in production. Requires the three extra sections. |
| `completed` | Done, not a running service. |
| `abandoned` | Stopped for good. **Reason recorded.** |

Status changes move the file: `completed` and `deployed` to a `completed/` folder,
`abandoned` to `abandoned/`, with inbound links updated.

**`on-hold` and `abandoned` require a recorded reason, and that's the point of having them.**
Git shows no commits since July; it cannot tell you whether that means finished, blocked,
abandoned, or waiting on a decision — and those demand entirely different responses when you
return. One line — *"paused 2026-07-13, the concept needs a refactor, specifics TBD"* — saves
an hour of archaeology and possibly a rebuild of something you deliberately stopped.

Nothing is deleted. An abandoned project keeps its full plan, including phases never built.
Projects get revived; this document exists because one was.

---

## The completion fork

When a project produces something that *runs*, its final phase is: **create or confirm an
operational entity page for the deployed state.**

Then the record forks:

- The **project page** freezes and moves to `completed/`. It is the historical build record —
  how this came to exist, what was rejected, what went wrong.
- The **entity page** becomes the living document — what this currently is, what version, what
  changed recently.

Both questions are legitimate; they're just asked at different times by different needs. "How
was this built and why?" is archaeology. "What's running right now?" is operations. A single
page that tries to be both answers neither quickly, and the operational half decays because
it's buried under build history.

Before creating a new entity page, the rule is to check for existing coverage — a roster page
or an adjacent entity may already document the deployed state, and a duplicate is worse than a
pointer.

---

## Cross-domain updates

When work in another domain touches a project — an ingested article that affects a build
decision, say — the agent appends a one-line entry to that project's `## Log`.

This is how a project page stays current without anyone deliberately maintaining it. The
information arrives through a side door and gets filed anyway.

---

**Next:** [10 — Skills](10-skills.md).
