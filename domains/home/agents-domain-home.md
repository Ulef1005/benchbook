# benchbook — Domain Rules: Home

> Loaded during INGEST for the home domain. Read alongside `agents-core.md`.
> The shared source-style dispatch flow is in `agents-core.md § 7 Domain Rules`.

---

## What belongs here

**Everything you own and operate.** Servers, single-board computers, network gear,
peripherals, appliances, devices, tools — and the software running on them.

This domain is the counterpart to `knowledge`, and together they resolve the Entity Placement
Rule's central question:

| | |
|---|---|
| **knowledge** | what exists *in the world* — the general product, tool or concept |
| **home** | what *you have* — the specific instance you own and run |

So a container runtime is a knowledge entity; the particular machine you run it on is a home
entity. A camera model is knowledge; *your* camera is home. Both exist, and they link to each
other.

Without this domain installed, the Entity Placement Rule has nowhere to send an owned thing —
which is why it ships installed by default.

**Self-hosted infrastructure is the heaviest use** of this domain for most people, and the
rules below lean that way. They apply equally to a coffee machine.

**Default subdomain assignment:**

| Subdomain | What goes there |
|---|---|
| `computing` | Servers, laptops, SBCs, peripherals, displays, and the software running on them |
| `appliances` | Smart-home devices, kitchen and household appliances, anything with a plug and an opinion |
| *(cross-subdomain)* | Ask the human |

References live flat in `wiki/home/references/`.

**Page types this domain produces:**

- **Source** — one per product spec, manual, review, or setup guide
- **Entity** — a specific product owned or seriously considered
- **Reference** — buying guides, setup guides, comparisons (4+ entities only)

---

## Domain checkpoint — REQUIRED, blocks until answered

At shared-flow step 2, ask:

> **"Is this product *owned*, *seriously considered*, or *just referenced*?"**

- **Owned or considered** → create an entity page with the matching `status:`
- **Just referenced** → source page only, no entity

This one question prevents the most common failure in this domain: an entity page for every
product mentioned in every review, none of which you own, all of which look identical to the
things you do.

If the entity is a **software tool with a public repo**, also ask whether it is *installed and
running*. If yes, set `repo_url:` in frontmatter — that's what enables release tracking later.

---

## Frontmatter conventions

- `subdomain:` always set
- `status:` required — `owned | considered | retired | reference-only`
- Owned products include `purchase_price:` and `purchase_date:` where known
- Software entities you actually run: set `repo_url:` and propose `change_history: true`

---

## Software / tool entity template

For software you run (`computing` subdomain). All sections optional — include only what's
relevant:

| Section | Purpose |
|---|---|
| `## Installation` | Binary location, install command, config file paths |
| `## Configuration` | Key settings actually used — **not** a full config dump |
| `## Operations` | Start/stop/restart, common commands, plugin management |
| `## Troubleshooting` | Solved issues — root cause plus fix; link to source pages for detail |
| `## Open Issues` | Current unresolved issues |

Plus the two sections that come with `change_history: true` — `## Current State` near the top
(overwritten in place) and `## Change History` at the bottom (append-only, newest first). See
`agents-page-conventions.md § Change History Conventions`.

**Never paste a working config containing real credentials.** Environment variables, secret
references, or vault indirection only. The comprehensiveness instinct — *"let me include the
whole config so the page is complete"* — is exactly what leaks tokens.

---

## Capture-at-touch rule

Ingest a source page from a project's own documentation at the moment of:

1. **install**, 2. **a troubleshooting session**, or 3. **a breaking upgrade**

— and not proactively. Note the version captured.

Documentation you ingest speculatively is documentation that's stale before you need it. The
moments above are exactly when you've read the docs properly and know which part mattered.

---

## Checklist

- [ ] Domain checkpoint answered (owned / considered / referenced)
- [ ] `subdomain:` set
- [ ] `status:` set on any entity page
- [ ] Software entity: `repo_url:` set, `change_history: true` proposed
- [ ] No credentials in any pasted config
- [ ] Two-way links between source and entities
- [ ] `index-home.md` updated
