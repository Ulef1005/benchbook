---
title: "Review Queue"
type: overview
created: 2026-09-12
domain: null
subdomain: null
publish: false
tags: [meta]
sources: []
---

# Review Queue

**Contradictions and conflicts that need a human decision.** LINT writes here when it finds two
pages that disagree, or a page that disagrees with itself; LINT **drains this file before it
looks for new work**, so nothing sits here unexamined across runs.

This is the only standing list in the wiki, and it exists because it holds exactly one kind of
item — a decision only the owner can make. It is not a todo list: there is no todo file, and
open work lives on the page the work belongs to (`agents-core.md` § 6).

Each entry: what disagrees, where, and what the options are. Delete the entry when the human
decides — the decision itself gets written onto the page, not kept here.

---

## Open

### `office-air-quality-sensor.md` — internal contradiction *(demo)*

`## Hard- and Software` reads *"Selected: TBD — pending the open question below"*, but the open
question it points at was closed on 2026-08-29 with **NDIR selected**. The two sections
disagree, and the `## Hard- and Software` one is the stale copy.

**Options:** (a) update the Selected line to NDIR, (b) reopen the question if the decision is
not in fact settled.

*Planted deliberately as a validation test of the contradiction check — it is a real
contradiction, just an intentional one. Left here as the worked example of what this file holds.*

## Resolved

*(Entries are deleted on resolution, not archived here. The decision lives on the page it was
made about; git history holds the rest.)*
