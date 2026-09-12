# scripts/ — code store

Code that is **not** a live deployed service:

- Wiki tooling, loose at the root
- Per-project build recipes or firmware source whose deployed form is a separate artifact,
  each in `scripts/<slug>/` with its own `README.md` linking back to the wiki page

## What ships here

| Script | What it does |
|---|---|
| `lint.py` | Every mechanical LINT check. `python3 scripts/lint.py` for the full report, `--quiet` for errors only. Exit 1 = at least one error. Pure stdlib — no install step, no dependencies, runs in any clone |
| `pre-commit.sh` | Git hook wrapper around `lint.py --quiet`. Blocks a commit on **errors only**. Install with `ln -s ../../scripts/pre-commit.sh .git/hooks/pre-commit`; bypass with `git commit --no-verify` |
| `relations.py` | Neighbourhood lookup over the `## Relations` graph. `./scripts/relations.py <page-slug>` reports a page's inbound **and** outbound edges, because each edge is stored exactly once and a page's own table therefore shows only half of them. `--depth N` walks further (capped at 4), `--orphans` lists pages with no edges either way |

**Why these are scripts and not model instructions.** A mechanical check has exactly one correct
answer, so paying a model to compute it is slow, expensive, and non-repeatable — and worse, a
model's answer varies run to run, which is the one thing a check must not do. The judgement
checks (does this page contradict that one? is this entity in the right place?) stay with the
agent, where variance is the point. The split is described in `agents-lint-checks.md`.

This distinction was learned the expensive way: for the first weeks of this repo's life
`lint.py` did not exist, and every LINT run re-derived the mechanical checks by hand at model
cost. The report was fine. It was just needlessly expensive and slightly different each time.

Continuously-running deployed services belong in their own infrastructure repo, where the
on-host path **is** the git working tree. A repo that is a *copy* of what's running on a
server rots: someone applies a fix in the field at 11pm, it works, and the repo silently stops
describing reality.

## Conventions

1. **Faithful backup.** Byte-for-byte copies of the on-disk originals — no added headers, no
   helpful reformatting. The moment a stored copy differs cosmetically, diffing it against the
   original stops being useful. Re-copy after any edit.
2. **No secrets.** Only environment variables, secret references, or vault indirection. This
   matters more here than in a normal repo, because the wiki's whole purpose is to be
   comprehensive — and comprehensiveness is exactly the instinct that leads to pasting a
   working config with a real token in it. LINT scans this folder and treats a hardcoded
   credential as an error.
3. **Two-way link.** The wiki page links to the files; the subfolder README links back.
4. **Not a wiki page.** No frontmatter, not indexed.
