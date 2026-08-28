---
name: deploy-runbook
description: "Create an install/deploy runbook for a new self-hosted service. Use when the user says 'create a deploy runbook for X', 'write an install runbook for X', 'we need to deploy X', 'runbook for [service]', or is about to plan a new self-hosted service. Scaffolds the full page — prerequisites, stack files, admin account, service-specific phases — plus a pre-filled Fleet Integration phase, so the boring integration steps never get re-derived, re-typed, or silently skipped."
license: MIT
metadata:
  version: 1.0.0
  category: home
---

# Deploy Runbook

## Purpose

After you deploy the third service you notice every runbook ends with the same boring steps —
and that skipping any one of them is invisible until something breaks at 3am.

**The value here isn't saved typing. It's that the boring steps stop being optional**, because
they arrive pre-written and unticked. A checklist you have to remember to write is a checklist
you'll eventually skip.

---

## Step 1 — Establish what's being deployed

Ask, one at a time:

1. **Service name and what it does**
2. **Where it runs** — which machine, from your `home` entities
3. **How it's packaged** — container, package, binary
4. **Does it need persistent storage?** Where, and how much
5. **Does it need to be reachable from outside?** This decides the proxy and DNS steps

---

## Step 2 — Check for an existing entity

```bash
ls wiki/home/entities/ | grep -i <service>
```

If the service already has an entity page, this is a re-deploy or an upgrade — read that page
first. Its `## Change History` may already record why the last attempt went the way it did.

---

## Step 3 — Create the project page

A deployment is a project. Use `/wiki-project-start`, which gives you the six required sections
and — importantly — **gates the plan until approved.**

`## Hard- and Software` should record the alternatives you considered and why this one won.
Six months on, "why not the other one?" is the question you'll actually have.

---

## Step 4 — Write the runbook phases

Into `## Plan / Phases`. The first phases are service-specific; the last one never is.

**Phase 1 — Prerequisites.** Host has capacity (disk, RAM, ports free). Storage path exists.
Any upstream account or API key obtained — recorded in your secret store, **never on the page**.

**Phase 2 — Stack files.** Compose file or unit file, config, environment. Committed to your
infrastructure repo, **not pasted into the wiki page**. The page links to the files; the files'
README links back.

> **No credentials, ever.** Environment variables, secret references, or vault lookups only.
> The comprehensiveness instinct — *"let me include the working config so the page is
> complete"* — is exactly what leaks tokens into a wiki you later want to share.

**Phase 3 — First run and admin account.** Bring it up, create the admin user, disable open
signup if the service allows it, verify you can log in.

**Phase 4+ — Service-specific.** Whatever this particular service needs: import, migration,
library scan, integration with something else. Ask the user; don't invent phases.

---

## Step 5 — The Fleet Integration phase — pre-filled, unticked

This is the point of the skill. Write it **verbatim**, every time, with nothing pre-checked:

```markdown
### Phase N — Fleet Integration

- [ ] **Reverse proxy** — add the route; confirm TLS
- [ ] **DNS** — add the record; confirm it resolves from a client
- [ ] **Backup** — add to the backup set; **run one backup and verify it restores**
- [ ] **Monitoring** — add an uptime check and an alert destination
- [ ] **Release tracking** — set `repo_url:` on the entity page so upgrades get noticed
- [ ] **Dashboard** — add a tile or link wherever you keep them
- [ ] **Documentation** — create the operational entity page (see Step 6)
```

**Adapt this list once, to your own fleet, then stop editing it.** Its value comes from being
identical across every service.

Two notes worth keeping:

- **"Run one backup and verify it restores"** — a backup job that has never been restored from
  is not a backup. This is the step most often marked done without being done.
- **Release tracking is cheap now and expensive later.** Setting `repo_url:` at deploy time
  costs nothing; discovering two years of missed security releases costs a weekend.

---

## Step 6 — The final step: the operational entity page

Per the final-step rule in `domains/projects/agents-domain-projects.md`, a deployment that
produces a running system **must** end by creating (or confirming) an entity page at
`wiki/home/entities/<service>.md` with `change_history: true`.

It carries:

- `## Current State` near the top — version, host, storage path, backup target, monitoring
  check. **Overwritten in place** when things change
- `## Installation`, `## Configuration`, `## Operations` — see the software entity template in
  `domains/home/agents-domain-home.md`
- `## Change History` at the bottom — append-only, newest first

**Check for existing coverage first.** A roster page may already track this; note that in the
project's `## Log` instead of creating a duplicate.

Then the record forks: the **project page** freezes and moves to `wiki/projects/completed/`
as the build history; the **entity page** becomes the living document.

---

## Step 7 — `deployed` status requires three extra sections

Before moving the project to `completed/`, ensure the page has `## Version Control`,
`## Backup Concept` and `## Cron Jobs`.

These exist because they're precisely what you fail to record and desperately need eighteen
months later, at which point recovering them is a forensic exercise.

---

## Error handling

- **User wants to skip fleet integration steps:** write them unticked anyway. An unticked box is
  a decision the user can make later; an absent box is one they'll never know they missed.
- **A step doesn't apply** (no external access, so no DNS): leave it in and strike it through
  with a one-line reason. Silence reads as an oversight.
- **Credentials appear in a config you're asked to record:** stop, and replace with an env var
  or vault reference before writing anything.
