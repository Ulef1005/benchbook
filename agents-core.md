# benchbook — Agent Contract

Operating contract for the agent that maintains this wiki: the single source of truth for
structure, conventions, and workflows. Co-owned — the agent proposes changes, the human
approves. Detail lives in satellite files (`agents-page-conventions.md`,
`agents-domain-*.md`), loaded on demand rather than restated here.

**Owner:** *(your name)* · **Dates:** `YYYY-MM-DD`

> **Working style (applies to everything below).** Never assume — ask when anything is
> unclear; state how many questions, present them one at a time with options and a
> recommendation, and ask before starting a task. Don't just agree: push back on legitimate
> concerns, but don't be nit-picky.

---

## 1. Session Start

1. Read this file (`agents-core.md`).
2. Greet the owner and confirm the contract loaded.

Index files load lazily (QUERY reads them at its step 1; INGEST touches the domain index in
post-flight) — **don't preload them.**

---

## 2. Hard Rules (non-negotiable)

1. **Read `agents-core.md` at session start.**
2. **Read `wiki/index.md` + the relevant `wiki/index-<domain>.md`** before answering
   questions — they are your map of what exists.
3. **Never modify `raw/`** — immutable sources. LINT may *move* files to `raw/_archived/`
   after 14 days; never delete.
4. **Always use relative markdown links** (`[text](relative/path.md)`) between wiki pages.
5. **Always include YAML frontmatter** on new pages, `publish: false` by default.
6. **Update the relevant `wiki/index-<domain>.md`** when creating or significantly updating a
   page.
7. **Append to `wiki/log/log.md`** only for *wiki-structural* events — `ingest`, `create`,
   `lint`, `query`, `skill` — in **1–3 lines**. **Not** `update`: project progress belongs in
   that project's `## Log`, and entity state changes belong in that entity's
   `## Change History`. See § 6 Log for the rule and why.
8. **Flag contradictions explicitly** — never silently overwrite conflicting information.
9. **Ask before creating pages** during interactive ingest — discuss with the human first.
10. **Keep pages concise** — split rather than bloat (past ~500 words, **~1,000 for `entity`
    pages**, consider splitting). **Measured excluding append-only sections** (`## Log`,
    `## Change History`) — a project's build history growing is not bloat — and **`project`
    and `source` pages are exempt**: the first because its template mandates six sections, the
    second because a source page transcribes external material and its length is inherent.
    The **`entity` limit is higher** because operational hub pages are dense on purpose, and
    splitting one lookup into three is a downgrade. LINT warns on the rest.
11. **Propose changes to this file** — don't modify the schema silently.
12. **Deployed-code commit rule.** If any code in this repo (or a linked infrastructure repo)
    is a *live checkout* running on a machine, it MUST be committed and pushed before the
    session ends — a live checkout is not an auto-committing daemon, so an uncommitted fix
    silently rots. Never in-place-edit a symlinked live-checkout path; it replaces the symlink
    with a plain file.
13. **No-Deletion Rule.** Before deleting a file or omitting content, stop and ask: *"About to
    delete / not carry over [X], which contains [summary] — does it belong somewhere else, or
    is it safe to discard?"* Applies to migration deletes, content that doesn't fit the target
    page, removed or collapsed sections, and links that would break. Never silently discard;
    when in doubt, ask.
14. **Never link to a `raw/` path from a page body.** Body links are online URLs
    (`source_url`) only; raw paths live in frontmatter (`raw_file:`).

---

## 3. Operations

### INGEST

**Pre-flight** (universal): (1) read the raw file; (2) propose `domain` (+`subdomain`) — human
confirms before any page is created; (3) read `agents-domain-<name>.md`; (4) extract
`source_url` from the raw if obvious, else leave empty and set `raw_file`; (5) discuss key
takeaways; (6) read `agents-page-conventions.md` before writing.
*Chat-dictation domains (projects) skip steps 1 & 4.*

**Dispatch** (domain-specific) — run the ordered steps in `agents-domain-<name>.md`:

| Domain | Flow |
|---|---|
| knowledge | source → entities (Entity Placement Rule) → 3-source channel trigger → reference only if 4+ entities |
| projects | new vs existing → confirm status → write/update project page |

**Post-flight** (universal): flag contradictions; update `index-<domain>.md` (master
`index.md` changes only when a domain or meta page is added); update `overview.md` if the big
picture shifted; append to `log.md` **only if a page was created or a source ingested** (1–3
lines — see § 6 Log); report what was created, updated, and flagged.

### QUERY

Read `wiki/index.md`, then the relevant `index-<domain>.md`, then the pages themselves →
synthesize with markdown-link citations. Offer to file substantial, reusable answers. If the
wiki is insufficient, fall back to `raw/` then general knowledge — **always disclose non-wiki
sources**. Append to `log.md` if significant (1–3 lines) — a `query` op is one of the few
things git history can't capture, so it genuinely belongs there.

### LINT

Manual trigger only. **Report-only** for wiki content — never edits page bodies or
frontmatter; writes a full report to `wiki/log/lint-YYYY-MM-DD.md`, prints an inline summary,
and appends one line to `log.md`. Write-capable only for two mechanical operations:

- **Raw-file archival:** for each page with a `raw_file:`, if that file exists in `raw/` and
  `mtime < now−14 days`, `mv` it to `raw/_archived/<domain>/`. Never delete.
- **Log archival:** when `log.md` exceeds 500 lines, move the oldest entries to
  `wiki/log/log-archive/YYYY-MM.md` until ≤350 lines remain.

Mechanical checks belong in `scripts/lint.py` (`python3 scripts/lint.py`; exit 1 = findings).
The LLM-judgment checks — entity placement, contradictions, staleness — live in
`agents-lint-checks.md`; read it before running LINT.

---

## 4. Architecture & Structure

**Layers:** `raw/` (immutable drop zone, read-only to the agent) → `wiki/` (agent-owned pages)
→ `scripts/` (code store) → `agents-core.md` (co-owned schema).

**Folders:**

- **Domains:** `knowledge`, `projects`. *(Add your own — see "Adding a domain" below.)*
- **Globals:** `sources/` (all source pages, flat, regardless of domain), `people/` (humans
  only).
- **Domain-local:** `<domain>/entities/` + `<domain>/references/`. Subdomain distinctions live
  in `subdomain:` frontmatter, not folders.
- **Meta:** `index.md`, `index-<domain>.md`, `overview.md`, `todo.md`, `log/log.md` (overflow
  → `log/log-archive/YYYY-MM.md`; LINT reports → `log/lint-YYYY-MM-DD.md`).

**Entity Placement Rule** — decided at first ingest by what the entity *is* (not how many
domains reference it); existing entities are reviewed only when next touched:

| Entity | Folder |
|---|---|
| Concrete humans | `wiki/people/` |
| Owned/specific instances (your particular server, your specific device) | `wiki/<domain>/entities/` |
| General concepts / products / tools | `wiki/knowledge/entities/` |

Cross-folder relations are first-class and expected.

**Adding a domain.** Start with two. Add a third only when an existing domain genuinely can't
hold something. Each new domain needs: a folder with `entities/` and `references/`, an
`index-<domain>.md`, an `agents-domain-<name>.md` satellite, a row in the INGEST dispatch
table above, and a pointer from `index.md`. Domains are cheap to add and expensive to abandon
half-populated.

### `scripts/` — Code Store

Holds code that is **not** a live deployed service: wiki tooling (`lint.py` and friends, loose
at root) and per-project build recipes or firmware source whose deployed form is a separate
artifact (`scripts/<slug>/`, each with a `README.md` linking back to its wiki page).

Continuously-running deployed services belong in their own infrastructure repo, where the
on-host path **is** the git working tree — so a field hotfix is a real commit rather than a
copy that rots.

Conventions: (1) **faithful backup** — byte-for-byte copies, no added headers; re-copy after
any edit. (2) **No secrets** — only environment variables, secret references, or vault
indirection. (3) **Two-way link** — the page links to the files, the subfolder README links
back; never paste standalone code into a page body. (4) **Not a wiki page** — no frontmatter,
not indexed.

---

## 5. Page Conventions

Full frontmatter field tables and per-page-type templates are in
**`agents-page-conventions.md`** — read it before creating or editing a page. Core rules:

**Structure:** one H1 matching frontmatter `title`; `## Summary` (2–4 sentences) required;
`## Sources` required on source pages; relative markdown links throughout; filenames
lowercase-with-hyphens; split beyond ~500 words (see Hard Rule 10 for how that's measured);
never link a `raw/` path from the body.

**Page types & locations:**

| Type | Location |
|---|---|
| source | `wiki/sources/` (global, flat) |
| entity | `people/` (humans), `<domain>/entities/` (owned/specific), or `knowledge/entities/` (general) |
| reference | `<domain>/references/` (only when a source ranks/compares 4+ entities) |
| project | `wiki/projects/` (+ `completed/`, `abandoned/`) |
| overview | `wiki/overview.md` |

**Channel/author entity trigger** — propose at the **3rd** source from one origin, tracked via
the `channel:` frontmatter field. Template → `agents-domain-knowledge.md`.

---

## 6. Index, Log, Overview, Todo

**Index (split):** `wiki/index.md` (master, ~50 lines) = `## People` + `## Domain Indexes`
pointer list + `## Meta`; changes only when a domain or meta page is added.
`wiki/index-<domain>.md` = that domain's full catalog, `###` order Sources / Entities /
References / Projects. Each entry: `- [Title](path.md) — one-line summary`. Frontmatter:
`type: overview`, `domain: <domain>`, `tags: [meta, index]`. An empty domain has no index file
until it has content.

**Log (`wiki/log/log.md`):** chronological, append-only. Entry:
`## [YYYY-MM-DD] <op> | Subject` followed by **1–3 lines, ~40 words max**. Ops: `ingest`,
`create`, `lint`, `query`, `skill`. Never delete entries; LINT archives overflow.

**What belongs here — and what doesn't.** This log tracks **wiki-structural events**: a page
created, a source ingested, a LINT run, a significant query answered, a skill run. It is *not*
a general activity log. The two things most often mis-filed here:

| Kind of change | Belongs in | Why not log.md |
|---|---|---|
| Project progress, decisions, build narrative | that project's `## Log` | you'd look for it on the project page, not by date |
| Entity state change (versions, config, deployments) | that entity's `## Change History` | the entity page is the single source for its own state |

`update` is deliberately **not** a valid op — it was the escape hatch that made this file grow
~10× faster than intended. An audit of the original wiki found **17 of 26 recent entries were
`update`, averaging 139 words against a 1–3 line spec**, largely duplicating content already
written to a project `## Log` in the same session. If an event seems to need a long log entry,
that's the signal it belongs on a page instead — with at most a one-line pointer here.

**Overview (`wiki/overview.md`):** `## Themes` (cross-cutting synthesis) + `## By Domain` (one
paragraph each).

**Todo (`wiki/todo.md`)** — the single todo location: `## Active/Planned Projects` are
**pointer-only** lists linking to each project page. Project todos live on the page's required
`## Open Questions` section and are **not** duplicated here — in the original wiki, 60 of ~76
mirrored items had drifted from their source pages before this changed. Plus `## Wiki Meta`
(hand-curated: pending decisions, schema proposals, deferred items) and `## LINT Findings`
(rewritten by each LINT run).

---

## 7. Domain Rules

Per-domain dispatch flows and conventions live in `agents-domain-<name>.md` — load the
relevant one at INGEST pre-flight.

**Shared Flow — source-style domains:**

1. Create the source page (`wiki/sources/<slug>.md`; body `## Summary` → `## Key Takeaways` →
   `## Sources`).
2. Domain checkpoint (per that domain's file).
3. Propose entity page(s) if warranted — apply the Entity Placement Rule; create only approved
   ones; update existing entities silently and note it in the report.
4. Two-way link — entity `sources:` frontmatter (plain slug) ↔ source-body relative link to
   the entity.
5. **References — flag, don't auto-update.** A new reference needs human approval **and** 4+
   entities. If a source adds to an existing reference, never edit silently: ask to (a) update
   now, (b) record it in `todo.md § Wiki Meta`, or (c) deprecate → split into entities with
   `## Compared To` cross-links.

---

## 8. Reference

Standing facts, connection details, and environment-specific notes that don't belong anywhere
else. Keep this short — anything that grows a structure of its own belongs on a page.

*(Empty in a fresh wiki. Add yours.)*
