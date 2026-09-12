# LINT Checks — Detail

> Loaded on-demand: read this file only when actually running the LINT operation. Not loaded
> at session start — see `agents-core.md § 3 Operations § LINT` for the cadence, posture,
> report format, and archival procedures, which stay in core.

**Posture reminder:** LINT is **report-only** for wiki content. It never edits page bodies or
frontmatter. Its only write permissions are two file-moving operations that never delete —
raw-file archival and log archival.

**One exception, and it is narrow: the error-class mechanical checks gate commits.**
`scripts/pre-commit.sh` runs `scripts/lint.py` and blocks the commit on any **error**. Warnings
never block, and the judgement checks below are not involved at all — they need a model, and a
commit hook that needs a model is a commit hook people disable. Bypass deliberately with
`git commit --no-verify`; install with `ln -s ../../scripts/pre-commit.sh .git/hooks/pre-commit`.

The distinction that makes this safe: *reporting* stays advisory because it involves judgement,
while *gating* is restricted to checks with exactly one correct answer — a missing required
field, a link that doesn't resolve, a file in the wrong folder for its declared type. Nothing
that gates a commit requires an opinion.

---

## Mechanical checks

These are deterministic. They belong in `scripts/lint.py`, not in model judgement — cheaper,
repeatable, and runnable on every commit.

| Check | Rule source | Notes |
|---|---|---|
| Frontmatter — required fields, enums, tag vocabulary | `agents-page-conventions.md § YAML Frontmatter` | tag vocabulary enforced on `reference` pages only |
| Domain ↔ folder consistency | `agents-core.md § 4 Architecture` | `wiki/sources/` and `wiki/people/` are global — any domain allowed there; elsewhere a mismatch is an error |
| Source page sections | `agents-page-conventions.md § Source Page Conventions` | missing `## Summary` / `## Sources` = error; missing `## Content` with a fetchable `source_url` = warning, unless `content-exempt` tagged |
| Project section template | `agents-domain-projects.md` | including the three extra sections required by `deployed` status |
| Skill roster vs disk | `agents-core.md § skills` | a skill directory with no roster entry, or a roster entry with no directory = error; missing/invalid SKILL.md frontmatter, `name:` ≠ directory name, `maturity:` outside `draft\|tested\|hardened` = error. **Disk is the source of truth; the roster page is a view over it** |
| Predicate vocabulary | `agents-domain-knowledge.md` | out-of-vocabulary predicate = warning; fix at next touch — most belong in `## Key Facts`. Scans **every** page carrying a `## Relations` table, not just knowledge entities, and matches the heading **exactly** — `## Relationship to X` is prose, not a triplet table |
| Project relations | `agents-page-conventions.md § Project Relations` | `## Relations` missing on an `active`/`planned` project, or not positioned directly after `## Summary` = error. Closed projects are out of scope |
| Reference page audit | `agents-page-conventions.md § Reference Page Conventions` | fewer than 4 compared entities = conversion candidate; no enforcement |
| Index coverage + orphans | `agents-core.md § 6 Index` | page missing from all index files = warning; dead index link = error; zero inbound links = warning, unless `standalone-reference` tagged |
| Page length | `agents-core.md` Hard Rule 10 | measured **excluding** append-only sections; `project` and `source` exempt; `entity` threshold higher. Report the worst offenders and a total count, not every breach |
| Broken relative links | Hard Rule 4 | any `](path.md)` that doesn't resolve = error |
| Raw path in page body | Hard Rule 14 | a body link to a `raw/` path = error |
| Duplicate files | — | `* 2.md` / `*conflicted copy*` under `wiki/` = error (sync-tool artifact); delete manually after confirming the original |
| Scripts store — README + links | `agents-core.md § scripts/` | subfolder missing `README.md` = warning; a wiki page linking a `scripts/…` path that doesn't exist = error; subfolder with no inbound link from any wiki page = warning |
| Scripts store — secret scan | `agents-core.md § scripts/` | `scripts/**/*.{yaml,yml,json}` scanned for hardcoded `password` / `api_key` / `secret` / `token` literals not using env-var, vault, or placeholder syntax = **error** |
| Publish audit | — | counts per domain only, no enforcement |
| Channel trigger | `agents-domain-knowledge.md` | an origin with ≥3 sources and no channel entity → note proposing one |

---

## Judgement checks

These need reading comprehension and are where a linting agent adds something a script can't.
All of them **surface findings; none of them act.**

| Check | Rule source | Notes |
|---|---|---|
| Entity placement audit | `agents-core.md § Entity Placement Rule` | `people/` is humans only; flag suspected misplacements between `<domain>/entities/` and `knowledge/entities/` — surface, never auto-move |
| Contradictions | — | spot-check recent pages against what they supersede. Two pages that quietly stopped agreeing is the single most valuable thing LINT finds |
| Staleness | — | does this page describe a state of the world that later pages have superseded? |
| Thin pages | — | triage the script's orphan and thin-page warnings for genuine problems vs. pages that are simply short and fine |
| Inline-artifact triage | `agents-core.md § scripts/` | spot fenced code blocks in page bodies that are standalone artifacts (full configs or scripts) rather than illustrative snippets; flag as `scripts/` migration candidates |

---

## A note on threshold design

When a check fires on more than a few percent of your content, **the check is usually wrong,
not the content.**

In the original wiki, the page-length rule flagged 27% of all pages. A rule that flags a
quarter of your content steers nothing — you stop reading its output within two runs. The fix
was to make the measurement honest (exclude append-only sections, exempt page types whose
length is inherent, raise the threshold for deliberately dense pages) and to report only the
worst offenders plus a backlog count.

Before adding a check, estimate what fraction of pages it will fire on. If the answer is
"lots", fix the threshold first.

## A note on check *scope*

A second failure mode, subtler than a bad threshold: **a check that is right about the region it
inspects is not the same thing as a check that is right.**

The predicate-vocabulary check above was originally scoped to knowledge entity pages, because
that is where `## Relations` tables started. It reported clean for months. When the graph was
finally measured end to end, 709 triples existed — **185 of them outside the check's scope,
carrying 124 off-vocabulary predicates**. Inside the scope, 0 of 524 rows were bad. The check
had a perfect record and a blind spot, and the perfect record is what stopped anyone looking.

So when you write a rule and a check for it, write down both scopes and compare them. If the
rule says "every page that has this section" and the check says "pages in this one folder", the
gap between them is invisible by construction — the check cannot report on what it does not
read.

Same class of bug, different shape: matching a heading by prefix rather than exactly. `## Relations`
and `## Relationship to the old system` both start with `## Relation`, and only one of them is a
triplet table.
