# Pack: homelab

Hardware and self-hosted software you **own and operate** — servers, single-board computers,
network gear, appliances, and the services running on them.

## What it adds

| | |
|---|---|
| **Rules** | `agents-domain-homelab.md` — the owned/considered/referenced checkpoint, software entity template, capture-at-touch rule |
| **Skills** | `deploy-runbook` — scaffolds an install runbook with your fleet's integration steps pre-filled |
| **Folders** | `wiki/homelab/entities/`, `wiki/homelab/references/` |
| **Index** | `wiki/index-homelab.md` |
| **Schema** | No new page types |
| **Subdomains** | `computing`, `appliances` |

## Install

1. Add to `agents-core.md` § 3 dispatch table:
   `| homelab | source → entity (owned/considered checkpoint) → references only if 4+ |`
   pointing at `domains/homelab/agents-domain-homelab.md`
2. Add `homelab` to the domain list in `agents-core.md` § 4
3. `mkdir -p wiki/homelab/entities wiki/homelab/references`
4. Create `wiki/index-homelab.md` from the pattern in `wiki/index-knowledge.md`
5. Copy `skills/deploy-runbook/` into your tool's skills location

Or just ask your agent: *"install the homelab domain pack."*

## Why you probably want it

If you run anything — a Pi, a NAS, a VPS, a few containers — this is where the *"how is this
actually wired and why did I do it that way"* problem lives most acutely. It pairs directly
with the ESP32 and Telegram-bot walkthroughs in
[A Day in the Life](../../docs/day-in-the-life.md).

Two rules in this pack earn their place:

**The owned/considered/referenced checkpoint** stops the most common failure in this domain —
an entity page for every product mentioned in every review, none of which you own, all
indistinguishable from the things you do.

**Capture-at-touch** says: ingest a project's documentation at install, at a troubleshooting
session, or at a breaking upgrade — never speculatively. Docs you ingest "to have them" are
stale before you need them; those three moments are exactly when you've read them properly and
know which part mattered.

## About `deploy-runbook`

The shipped version is genericized. Its seven fleet-integration steps — reverse proxy, DNS,
backup job, monitoring check, release tracking, dashboard tile, documentation pages — are the
shape of the original, not a prescription.

**Replace them with your own fleet's steps.** The value isn't the specific list, it's that the
boring steps arrive pre-written and unticked, so they stop being optional. A checklist you have
to remember to write is a checklist you'll eventually skip.
