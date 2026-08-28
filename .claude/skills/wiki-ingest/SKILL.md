---
name: wiki-ingest
description: "Process a source — a file, a URL, a video, or dictation in chat — into structured wiki pages. Use when the user says 'ingest [file/url]', 'process this', 'let's ingest [subject]', or drops a file in raw/ and wants it turned into wiki pages. Also triggers when the user pastes a URL, PDF path, or image path directly. Orchestrates the full INGEST workflow: detect input, extract content, propose domain, load domain rules, discuss takeaways, run domain dispatch, then update index, overview and log. If no source is given, offers a chat-dictation source page instead."
license: MIT
metadata:
  version: 1.0.0
  category: wiki
---

# Wiki Ingest

## Purpose

Thin orchestrator for the INGEST operation defined in `agents-core.md § 3`. Adds trigger
phrases and progressive disclosure. **Does not duplicate domain logic** — dispatch is delegated
to `domains/<name>/agents-domain-<name>.md`.

---

## Step 1 — Detect input type and extract content

| Input | Detection | Action |
|---|---|---|
| Video URL | a video host in the argument | Transcribe with whatever capability your tool has. Capture the channel/author name — it drives the 3-source entity trigger |
| Other web URL | `http://` or `https://` | Fetch and convert to readable text |
| File path | `.pdf`, `.jpg`, `.png`, `.md`, `.txt`, audio | Read it. Images are read visually |
| Path in `raw/` | text content on disk | Read it |
| Nothing | no argument given | Ask: *"No source found — create a source page from chat dictation instead?"* If yes, skip to Step 5 and take content from the conversation |

**If extraction yields under ~100 words**, don't write pages from nothing. Say what you found
and stop. A thin result usually means the source is visual or the fetch was blocked — if your
tool can extract frames or screenshots, try that first and note in `## Sources` that
lower-fidelity extraction was used.

### Step 1b — Re-ingest guard

Once you know the `source_url`, check whether it's already been ingested:

```bash
grep -rl "source_url: \"<url>\"" wiki/sources/
```

If a match exists: report the existing page path and its `created:` date, then **stop**. The
user must explicitly pass `--force` to overwrite.

---

## Step 2 — Propose domain, and wait

Propose `domain` (and `subdomain` where the domain defines them). **Do not create any page
before the human confirms.**

This is the highest-leverage checkpoint in the whole workflow — nearly every downstream filing
mistake traces back to a wrong call here.

Default proposal for general or cross-cutting material is `knowledge`. For something the user
owns and operates, propose `home`.

Only installed domains are valid — see the dispatch table in `agents-core.md § 3`. If the
material clearly belongs to an uninstalled pack, say so and offer to install it.

---

## Step 3 — Load domain rules

Read `domains/<confirmed-domain>/agents-domain-<confirmed-domain>.md`. It holds the dispatch
flow and every convention for this domain.

---

## Step 4 — Extract `source_url`

- URL inputs: the URL itself.
- Raw files: scan for a primary URL (clipper metadata, first line). If absent, leave it empty —
  `raw_file:` is the provenance pointer. **Do not web-search for one; do not ask.**
- Never use a local file path as `source_url`.

---

## Step 5 — Discuss key takeaways, before writing anything

Summarise what the source actually says, and ask what to emphasise.

| Depth | Takeaways | Extras |
|---|---|---|
| `--depth deep` *(default)* | 8–12 | timestamps, counterarguments |
| `--depth standard` | 5–7 | — |
| `--depth light` | 3–5 | — |

Nothing is on disk yet. This is where a human corrects a misreading cheaply.

---

## Step 5a — Load page conventions

Read `agents-page-conventions.md` before writing a single page. It carries the frontmatter
tables and the per-page-type section templates.

---

## Step 6 — Domain dispatch

Run the ordered steps from the domain rules file. Universally:

- **Propose entity pages; don't create them.** Get approval for each.
- **Apply the Entity Placement Rule** per entity — humans to `people/`, owned instances to
  `home/entities/` (or a better-fitting domain), general things to `knowledge/entities/`.
- **Two-way link** — the entity's `sources:` frontmatter gets the source slug; the source body
  links to the entity.
- **A reference page needs 4+ compared entities and human approval.** For 1–3, use entity pages
  with `## Compared To` cross-links.
- **Channel trigger:** at the third source from one origin, propose a channel entity.
  ```bash
  grep -h "^channel:" wiki/sources/*.md | sort | uniq -c
  ```

---

## Step 7 — Post-flight

1. **Flag contradictions** with existing content — never silently overwrite.
2. **Update `wiki/index-<domain>.md`.** The master `index.md` changes only if a domain or meta
   page appeared. Write the one-line summary properly: say what the page is *for*, not what
   it's called — that line is the retrieval signal.
3. **Update `wiki/overview.md`** only if the big picture actually shifted. Usually it hasn't.
4. **Append to `wiki/log/log.md`** — `## [YYYY-MM-DD] ingest | <Subject>` plus 1–3 lines,
   ~40 words. Only if a page was created.
5. **Report:** created, updated, contradictions flagged, open questions.

---

## Flags

- `--depth deep` (default) · `--depth standard` · `--depth light`
- `--force` — overwrite an existing source page, bypassing the re-ingest guard

## Error handling

- **Under ~100 words extracted:** say what was found and stop. Never write pages from nothing.
- **Existing source page, no `--force`:** report the path and date; stop.
- **Raw file not found:** report the exact path checked; offer chat dictation.
- **Domain not confirmed:** do not proceed past Step 2.
- **Domain rules file missing:** name the missing file and stop.
- **Contradiction found:** surface it explicitly. Never resolve it silently.
