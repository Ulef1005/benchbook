---
name: wiki-project-start
description: "Create a new project page in the wiki. Use when the user says 'start a project', 'let's track a new project', 'create project [name]', 'new wiki project', 'I want to begin tracking X', or expresses intent to start, plan or track something new — even if they don't say 'wiki'. Asks for the name and goal, creates the page with all required sections and a GATED plan stub, updates the index, and appends to the log. Never begins implementation work."
license: MIT
metadata:
  version: 1.0.0
  category: wiki
---

# Wiki Project Start

## Purpose

Create a project page per `domains/projects/agents-domain-projects.md`, with the plan
deliberately left unwritten until a human approves it.

> **The single most important thing this skill does is not build anything.** See Step 5.

---

## Step 1 — Check new vs existing

```bash
ls wiki/projects/ wiki/projects/completed/ wiki/projects/abandoned/
```

If something similar exists, ask whether to update it instead. Reviving an abandoned project is
common and preferable to starting a near-duplicate.

---

## Step 2 — Gather the essentials

Ask, one at a time, with a recommendation where you have one:

1. **Name** — derive a lowercase-hyphenated slug and confirm it
2. **Goal** — what does "done" look like?
3. **Status** — `planned` for anything not yet approved (the default and usually correct)

Don't ask for the plan yet. That's Step 5's whole point.

---

## Step 3 — Read the conventions

Read `domains/projects/agents-domain-projects.md` and `agents-page-conventions.md` before
writing.

---

## Step 4 — Write the page

`wiki/projects/<slug>.md`, with frontmatter (`type: project`, `domain: projects`,
`subdomain: null`, `status:`, `publish: false`) and **all six required sections in order**:

| Section | What goes in it now |
|---|---|
| `## Summary` | 2–4 sentences |
| `## Use Cases` | What it must actually do, concretely |
| `## Hard- and Software` | Options table — the alternatives and their trade-offs — plus a "Selected" subsection marked TBD until decided |
| `## Plan / Phases` | **Stub only.** See Step 5 |
| `## Open Questions` | Everything genuinely undecided |
| `## Log` | One entry: `### [YYYY-MM-DD] Project created` |

The **options table is the highest-value section in the system**. It's where "why not the
obvious alternative?" gets answered permanently, at the moment you actually know the answer.
Fill it in even when the choice feels obvious — especially then.

---

## Step 5 — Gate the plan

`## Plan / Phases` gets a high-level phase list and this notice, prominently:

> **Deferred — awaiting manual plan approval.**

**Then stop. Write no code, create no files, call no APIs.**

The problem this solves is specific to agentic tools: the user describes an idea, and forty
seconds later there are eleven files. They're plausible. Some are even good. But the
architectural decisions were made at speed by the agent, they're now load-bearing, and the
human is reviewing them backwards.

Tell the user the plan is gated, and offer `/wiki-project-review` to stress-test it before
approving.

On explicit approval — *"approve the plan"* or equivalent — move `status:` to `active` and
write the plan out in full.

---

## Step 6 — Post-flight

1. Add an entry to `wiki/index-projects.md` under the right status heading, with a one-line
   summary saying what the project is *for*.
2. Append to `wiki/log/log.md`:
   `## [YYYY-MM-DD] create | <Project Name>` plus 1–3 lines.
3. Report what was created and confirm the plan is gated.

---

## Error handling

- **A similar project exists:** surface it and ask before creating a second.
- **The user asks you to start building immediately:** explain the gate, offer to write the plan
  for approval in the same breath. Don't just refuse — produce the thing they need to approve.
- **Status unclear:** default to `planned`. It's the safe direction.
