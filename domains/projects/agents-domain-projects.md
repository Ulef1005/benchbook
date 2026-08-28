# benchbook — Domain Rules: Projects

> Loaded during INGEST for the projects domain. Read alongside `agents-core.md`.

---

## What belongs here

A project is something you are actively building, planning, or tracking. Not something you're
learning about — that's knowledge.

**Default subdomain:** `null`. Active projects land directly in `wiki/projects/`. Completed
and deployed projects move to `wiki/projects/completed/`; abandoned ones to
`wiki/projects/abandoned/`.

**Page types this domain produces:**

- **No source page** — project content goes directly to `wiki/projects/<slug>.md`
- **Reference** — notes, decisions or guides supporting multiple projects →
  `wiki/projects/references/`

**Chat-driven by default:** projects are usually born from a conversation, so INGEST pre-flight
steps 1 (read the raw file) and 4 (extract source URL) are typically skipped.

---

## Frontmatter conventions

- `type: project`
- `domain: projects` — always. Never multi-domain; cross-domain content is referenced with
  relative markdown links.
- `subdomain: null`
- `status: planned | active | on-hold | deployed | completed | abandoned` (required)
- `deployed` is software-specific and additionally requires `## Version Control`,
  `## Backup Concept`, and `## Cron Jobs` sections

---

## Required section template (LINT-enforced)

Every project page must contain these sections, in this order:

1. `## Summary` — 2–4 sentences
   - `## Links` — optional, may follow Summary: external URLs relevant to the project
2. `## Use Cases` — concrete capabilities with example actions and data sources; note priority
   order
3. `## Hard- and Software` — options table (model/version, cost, pros/cons) plus a "Selected"
   subsection (TBD until decided); supporting infrastructure as relative links to entity pages
4. `## Plan / Phases` — implementation phases; **GATED: stub only until the plan is manually
   approved.** Must carry a prominent notice: *"Deferred — awaiting manual plan approval."*
5. `## Open Questions` — unresolved decisions blocking progress
6. `## Log` — chronological notes, append-only

The `## Hard- and Software` options table is quietly the highest-value section in the system.
It's where *"why not the obvious alternative?"* gets answered permanently, at the moment you
actually know the answer.

---

## The plan approval gate

**While a project is in `planned` status, `## Plan / Phases` contains only a high-level phase
list marked as deferred. The agent must not begin any implementation work — writing code,
creating files, calling APIs — until the human explicitly says "approve the plan" or
equivalent. On approval, status moves to `active` and the plan is fleshed out in full.**

This is the strongest human-in-the-loop rule in the contract. The problem it solves is
specific to agentic tools: you describe an idea, and forty seconds later there are eleven
files. They're plausible, some are even good, and you never made the architectural decisions —
they were made for you, at speed, and now they're load-bearing.

The gate costs one round trip. It is worth it every time.

---

## Status lifecycle

```
planned → active → deployed / completed
   ↓         ↓
on-hold   abandoned
```

**`on-hold` and `abandoned` require a recorded reason.** Git shows no commits since a date; it
cannot tell you whether that means finished, blocked, abandoned, or waiting on a decision —
and those demand entirely different responses when you return. One line saves an hour of
archaeology.

**Nothing is deleted.** An abandoned project keeps its full plan, including phases never built.
Projects get revived.

---

## Final-step rule — deployed-state entity

If a project's completion produces an **owned, running system** — a deployed service, a
hardware build with firmware, a tool complex enough to need its own reference — as opposed to
a buying decision, an audit, or a one-off change, then its `## Plan / Phases` **must end with
a final step**: create (or confirm an existing) operational entity page documenting the
deployed state, per the Entity Placement Rule.

The entity page is the *living* doc going forward (`type: entity`, `change_history: true`).
The project page becomes the historical build record and moves to `completed/`.

**Check for existing coverage first.** A roster page or a project-adjacent entity may already
document the deployed state; note which one in the project's `## Log` rather than creating a
duplicate.

---

## Dispatch flow

**P1.** Determine new vs existing project. If existing → update; if new → create.

**P2.** Confirm `status:`.

**P3.** Write or update `wiki/projects/<slug>.md` with the required section template. **On
status transition** to `completed` or `deployed`, move the file to `wiki/projects/completed/`;
to `abandoned`, move it to `wiki/projects/abandoned/`. Update relative links elsewhere in the
wiki that point at this page — its path just changed. For `deployed`, ensure the three extra
sections exist (stub if needed). If the project produces an owned running system, confirm the
final-step entity exists or is explicitly noted as satisfied before the move.

**P4.** Link any sources consumed via `sources:` frontmatter.

**P5.** Link related entities via relative markdown links under `## Hard- and Software`.

---

## Auto-append on cross-domain touches

When the agent updates a project page during **another domain's ingest** — an article that
affects a build decision, say — it appends a one-line dated entry to that project's `## Log`.

This is how a project page stays current without anyone deliberately maintaining it.

---

## Checklist

- [ ] New vs existing checked
- [ ] `status:` confirmed
- [ ] Required sections present, in order
- [ ] Plan gated if `planned` — no implementation work started
- [ ] On status transition: file moved, inbound links updated
- [ ] Entities linked under Hard- and Software
- [ ] If it deploys an owned running system: final-step entity confirmed
- [ ] `on-hold` / `abandoned` carry a recorded reason
- [ ] `index-projects.md` updated
