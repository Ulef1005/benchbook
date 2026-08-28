# Pack: projects

**Installed by default.**

Things you're building, planning, or tracking. Not things you're learning about — that's
knowledge.

## What it adds

| | |
|---|---|
| **Rules** | `agents-domain-projects.md` — section template, plan approval gate, status lifecycle, final-step rule |
| **Skills** | None of its own — the core six already include `wiki-project-start`, `wiki-project-open` and `wiki-project-review`. |
| **Folders** | `wiki/projects/`, `wiki/projects/completed/`, `wiki/projects/abandoned/`, `wiki/projects/references/` |
| **Index** | `wiki/index-projects.md` |
| **Schema** | No new page types, but the `project` type carries a six-section required template |
| **Subdomains** | None |

## Why you probably want it

This is the pack that makes benchbook different from a general knowledge wiki. Tracking things
*you build* has state, a lifecycle, and a decision record — including the options that lost,
which is the thing nothing else captures.

It also carries the **plan approval gate**, the strongest human-in-the-loop rule in the system:
while a project is `planned`, no implementation work may begin until you approve the plan.
Pair it with the `wiki-project-review` core skill, which attacks the plan one question at a
time before anything gets built.
