---
name: wiki-session-close
description: "Close the current wiki work session: verify what changed, log new pages, run verification gates, commit and push. Use when the user says 'close the session', \"we're done\", 'wrap up', \"that's all for today\", 'end session', or signals they're finished. Run this at the end of any session that produced changes."
license: MIT
metadata:
  version: 1.0.0
  category: wiki
---

# Wiki Session Close

## Purpose

The last five minutes are where discipline dies. The work is done, the interesting part is
over, and committing feels like paperwork.

Making it one command is the difference between a repo that's current and one that isn't.

---

## Step 1 — Ground-truth what changed

```bash
git status --short
git diff --name-only
git ls-files --others --exclude-standard
```

If nothing changed, say so and stop.

For each changed file note: path, whether it was **created** or **updated**, and a one-line
description. Work from the diff — not from memory of what you think you did.

---

## Step 2 — Verify frontmatter on created pages

For anything created this session, check `created:` is today's date. Fix if not.

---

## Step 3 — Log new pages only

Append to `wiki/log/log.md` for **newly created pages only**. Skip updates entirely — project
progress belongs in that project's `## Log`, entity state in that entity's `## Change History`.

```
## [YYYY-MM-DD] <op> | <Subject>

<1–3 lines, ~40 words max>
```

Valid ops: `ingest`, `create`, `lint`, `query`, `skill`. **Never `update`.**

De-duplicate before appending:

```bash
grep "^## \[$(date +%Y-%m-%d)\]" wiki/log/log.md
```

If an entry wants to be longer than three lines, that's the signal it belongs on a page — with
at most a one-line pointer here.

Skip this step entirely if no new pages were created.

---

## Step 4 — Lint quick-check

```bash
python3 scripts/lint.py
```

- **Errors introduced this session** (in Step 1's files): fix before committing.
- **Pre-existing errors:** don't block. Mention them in the close report.
- **Warnings:** ignore here. The full `/wiki-lint` run triages those.

---

## Step 5 — Verification gate

Run against **this session's files only** — not the whole wiki. This is a hard gate: fix and
re-check until every item passes.

1. **Line-break check.** Look for a non-blank line ending mid-sentence — no trailing
   punctuation, list marker, or two trailing spaces — followed immediately by another non-blank
   line. Markdown collapses that into a run-on on render.

2. **Table arithmetic.** For any table with a numeric column and a Total/Subtotal row,
   recompute from the other rows. Flag mismatches rather than guessing which figure is right.

3. **Link resolution.** Extract every relative `](path.md)` from changed files and confirm each
   resolves. For broken ones, ask whether the target should be a stub or the link is a typo.
   **Never leave one broken silently.**

4. **Commit message accuracy.** After drafting the message (Step 6), diff it against
   `git diff --stat`. Everything named in the message must be in the diff, and nothing
   significant in the diff should go unmentioned. Rewrite if it drifted.

5. **Destructive-overwrite check.** For any changed file matching a log or archive shape
   (`log.md`, `log-archive/**`, `**/_archived/**`):

   ```bash
   git diff --numstat <file>
   ```

   **If deletions exceed insertions, stop and show the human the diff before proceeding.** This
   is the exact failure mode — a write clobbering history instead of appending — that has
   destroyed archive content before.

---

## Step 6 — Commit and push

```bash
git add -A && git commit -m "<message>" && git push
```

Message format: `<op>: <subject> — <what changed>`, e.g.
`create: esp32-display project page`, `ingest: guide to structured logging`.

Review what's staged before committing (`git status` after a broad `git add`). If anything
looks like it might carry a secret — even with an innocuous filename — check the contents
before pushing.

Run automatically once Step 5 is green. No confirmation needed.

---

## Step 7 — Report

State plainly: what was created, what was updated, what the lint found, what you fixed in the
gate, and anything left open. If tests or checks failed, say so with the output — don't round
up to "done".
