---
name: wiki-lint
description: "Run a full LINT check on the wiki. Use when the user says 'lint the wiki', 'run lint', or '/lint'. Runs the mechanical checker, adds the judgement checks on top, writes a dated report, and syncs todo.md. Report-only for wiki content — never edits page bodies or frontmatter. Offers opt-in archival for stale raw files and log overflow, and never moves anything without confirmation."
license: MIT
metadata:
  version: 1.0.0
  category: wiki
---

# Wiki Lint

## Purpose

Thin orchestrator for the LINT operation in `agents-core.md § 3`. Runs the deterministic
checker for mechanical checks, adds the judgement checks, writes a report, and handles the two
write operations with explicit opt-in.

> **Report-only.** LINT never edits page bodies or frontmatter. Its only write permissions are
> two file-*moving* operations that never delete. An auto-fixing linter over natural-language
> content is a machine for introducing unreviewed changes across hundreds of files at once.

---

## Step 1 — Mechanical checks

```bash
python3 scripts/lint.py
```

Implements the mechanical half of `agents-lint-checks.md` — read that file before running LINT.
**Exit code 1 means "findings exist", not "the script failed."** Capture the output; it becomes
the body of the report.

If `scripts/lint.py` doesn't exist yet, do the mechanical checks by hand from
`agents-lint-checks.md` and tell the user the script is worth writing — these checks are
deterministic and shouldn't cost model tokens every run.

**When the schema changes, update `scripts/lint.py` in the same session.** A checker that
mirrors an older schema produces confident wrong answers.

---

## Step 2 — Judgement checks

The checks a script can't do. **Surface findings; change nothing.**

1. **Entity placement audit** — `people/` humans only; owned instances in a domain's
   `entities/`; general things in `knowledge/entities/`. Flag suspected misplacements. Never
   auto-move.
2. **Contradictions** — spot-check recently touched pages against what they supersede. *Two
   pages that quietly stopped agreeing is the single most valuable thing LINT finds.*
3. **Staleness** — does a page describe a state of the world that later pages have overtaken?
4. **Orphan / thin triage** — of the script's warnings, which are genuine problems versus pages
   that are simply short and fine? Report only the real ones.
5. **Inline-artifact triage** — fenced code blocks that are standalone artifacts (full configs
   or scripts) rather than illustrative snippets. Flag as `scripts/` migration candidates.

---

## Step 3 — Sync `wiki/todo.md`

**Never rewrite the whole file** — `## Wiki Meta` is hand-authored and has no source page.

1. **Closed items:** for each `[x]` on a project or entity page, remove the matching `[ ]` from
   todo.
2. **New items:** add `[ ]` items that aren't there yet, under the right heading.
3. **Findings:** replace `## LINT Findings` with this run's summary, or `No findings.`

Remember todo is **pointer-only for projects** — link the page, don't mirror its items. Mirrored
state drifts; in the wiki this came from, 60 of ~76 mirrored items had diverged from their
sources before that rule changed.

---

## Step 4 — Write the report

Write `wiki/log/lint-YYYY-MM-DD.md` (overwrite on a same-day re-run): script output, then
`## Judgement Checks`, then a summary of todo changes.

Print an inline summary to chat: error count, warning count, top three issues.

---

## Step 5 — Raw-file archival (opt-in)

Candidates are pages whose `raw_file:` exists in `raw/` with mtime older than 14 days.

Show the list. Ask: *"Archive these? (`raw/` → `raw/_archived/<domain>/`)"* **Only proceed on
confirmation.** Never delete — archival is reversible.

---

## Step 6 — Log archival (opt-in)

If `wiki/log/log.md` exceeds 500 lines, identify the oldest entries needed to bring it back to
≤350. Show them. Ask before moving them to `wiki/log/log-archive/YYYY-MM.md`.

**Before writing any archive file, check you're appending and not replacing.** Overwriting an
archive destroys history that exists nowhere else.

---

## Step 7 — Log the run

```
## [YYYY-MM-DD] lint | LINT run — <N> errors, <N> warnings. Report: wiki/log/lint-YYYY-MM-DD.md
```

---

## A note on thresholds

If a check fires on more than a few percent of pages, **the check is usually wrong, not the
content.** In the original wiki the page-length rule flagged 27% of pages — a rule that flags a
quarter of your content steers nothing, because you stop reading its output within two runs.

When you notice that happening, propose fixing the threshold rather than the pages.

## Error handling

- **Script crashes** (traceback, not exit 1): report it, fall back to manual checks.
- **Exit code 1:** findings exist. Proceed normally.
- **File read error:** note the path in the report; don't stop the run.
