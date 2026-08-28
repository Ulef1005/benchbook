# Pack: home

**Installed by default.**

Everything you own and operate — servers, single-board computers, network gear, peripherals,
appliances, devices, and the software running on them.

## Why this one is core

`home` is the counterpart to `knowledge`, and the two together resolve the Entity Placement
Rule:

| | |
|---|---|
| **knowledge** | what exists *in the world* — the general product, tool or concept |
| **home** | what *you have* — the specific instance you own and run |

Without it, the rule's middle branch has nowhere to send an owned thing. A container runtime
belongs in `knowledge/entities/`; the machine you run it on has to go *somewhere*, and
`projects` is wrong — a project is something you're building, not something you have.

That's why the default install is three domains rather than two:

- **knowledge** — what exists in the world
- **home** — what you own and operate
- **projects** — what you're building

Drop any one and something has no correct destination.

## What it adds

| | |
|---|---|
| **Rules** | `agents-domain-home.md` — the owned/considered/referenced checkpoint, software entity template, capture-at-touch rule |
| **Skills** | `deploy-runbook` — scaffolds an install runbook with your fleet's integration steps pre-filled |
| **Folders** | `wiki/home/entities/`, `wiki/home/references/` |
| **Index** | `wiki/index-home.md` |
| **Schema** | No new page types |
| **Subdomains** | `computing`, `appliances` |

## Two rules that earn their place

**The owned/considered/referenced checkpoint** blocks the ingest until answered, and it stops
the most common failure in this domain: an entity page for every product mentioned in every
review, none of which you own, all indistinguishable from the things you do.

**Capture-at-touch** says ingest a project's documentation at install, at a troubleshooting
session, or at a breaking upgrade — never speculatively. Docs you ingest "to have them" are
stale before you need them. Those three moments are exactly when you've read them properly and
know which part mattered.

## About `deploy-runbook`

Self-hosted infrastructure is the heaviest use of this domain, and this skill serves it. The
shipped version is genericized — its seven integration steps (reverse proxy, DNS, backup job,
monitoring check, release tracking, dashboard tile, documentation pages) are the *shape* of the
original, not a prescription.

**Replace them with your own fleet's steps.** The value isn't the list, it's that the boring
steps arrive pre-written and unticked, so they stop being optional. A checklist you have to
remember to write is one you'll eventually skip.

If you don't self-host anything, skip the skill and keep the domain — the entity conventions
work just as well for a bike, a camera, or a coffee machine.
