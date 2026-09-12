---
name: wiki-project-open
description: "Load and orient to an existing wiki project. Use when the user says \"let's work on [project]\", 'open project [name]', 'continue [project]', 'pick up where we left off on X', or wants to resume an active or planned project. Reads the page and presents status, recent log entries and open questions so the user can immediately decide what to do next. Use whenever the user references a project by name and wants to do something with it — even without saying 'open'."
maturity: tested
license: MIT
metadata:
  version: 1.0.0
---

# Wiki Project Open

## Purpose

Get a human oriented in one screen. Resuming a project after three weeks means reconstructing
where you were, and that reconstruction is exactly what the page already holds.

---

## Step 1 — Identify the project

If named, derive the slug and go to Step 2.

If not: read `wiki/index-projects.md`, list what's under `### Active` and `### Planned`, and
ask which one — as a numbered list.

---

## Step 2 — Find and read it

Check in order:

```
wiki/projects/<slug>.md
wiki/projects/completed/<slug>.md
wiki/projects/abandoned/<slug>.md
```

If it's in `completed/` or `abandoned/`, say so up front — the user may be looking at history
rather than live work, and reviving an abandoned project is a real thing that happens.

If nothing matches, say so and offer `/wiki-project-start`.

---

## Step 2.5 — Load the project's relation neighbourhood

```bash
./scripts/relations.py <slug>
```

Every `## Relations` fact is stored **once**, on whichever page reads naturally, so the project
page shows only half its relations — the rest live on the entity pages that name it. This reads
the whole graph and reports both directions. Run it before Step 3 and read the pages it names;
that is the context for working on this project.

**Stay at the default depth 1.** Direct neighbours are what orientation needs. Depth 2 and 3 grow
fast enough to cost more than reading the whole domain index, and they answer a different
question — "what is the blast radius of changing this" — which is rarely the one you have.

**An empty result is normal — say so in one line and move on.** Relations are added at next touch
rather than backfilled, so most projects have none yet. Do not report it as a problem, do not
investigate it, and do not let it delay Step 3. *(This instruction exists because a step that
reports a problem on most runs trains the reader to ignore the step.)*

**If the project has no `## Relations` section and you go on to do real work on it, add one** —
this is the "next touch" the backfill relies on. It goes directly after `## Summary`. Predicates
come from the controlled vocabulary in `domains/knowledge/agents-domain-knowledge.md`. Record
only relations the page already states; never infer one to fill the table.

---

## Step 3 — Present a compact brief

No walls of text. This shape:

```
## [Project Name] — <status>

**Goal:** <one sentence from ## Summary>

**Last activity:** <date + one line from the most recent ## Log entry>

**Open questions:** <count> — <the first one, if any>

**Current phase:** <the first unchecked phase, or "plan not yet approved">
```

Two things to surface loudly if present:

- **`status: planned`** — the plan is gated. No implementation work may begin until the human
  approves it.
- **`on-hold` or `abandoned`** — lead with the recorded reason. That reason is the single most
  useful thing on the page right now.

Then ask: **"What do you want to work on?"**

---

## Step 4 — Act on the answer

Handle these inline; no separate skill needed.

| Request | Do this |
|---|---|
| Update or add a phase | Edit `## Plan / Phases` |
| Close an open question | Replace the `[ ]` with `[x]` and record the decision inline |
| Add a log entry | Append to `## Log` with today's date |
| Change status | Update frontmatter, then handle the move — see below |
| Approve the plan | `planned → active`, write the plan out in full |

**Status transitions move the file:**

- `completed` / `deployed` → `wiki/projects/completed/`
- `abandoned` → `wiki/projects/abandoned/`

On any move: **update inbound links elsewhere in the wiki** — the path just changed. And for
`deployed`, ensure `## Version Control`, `## Backup Concept` and `## Cron Jobs` exist.

**`on-hold` and `abandoned` require a recorded reason.** Ask for one if the user doesn't give
it. Without it, a future reader can't tell "finished" from "blocked" from "gave up", and those
demand completely different responses.

**If the project produced something that runs**, confirm the final-step operational entity page
exists before moving it to `completed/` — or note in the `## Log` which existing page covers it.

---

## Step 5 — Update the index

If status changed or the summary shifted, update the entry in `wiki/index-projects.md`.

Project progress goes in the project's own `## Log` — **not** in `wiki/log/log.md`. That's the
`update`-op rule; see `agents-core.md § 6`.
