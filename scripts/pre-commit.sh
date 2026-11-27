#!/usr/bin/env bash
#
# Git pre-commit hook: block a commit on error-class LINT findings.
#
# Install:
#   ln -s ../../scripts/pre-commit.sh .git/hooks/pre-commit
#
# Bypass deliberately (and it is fine to do so — sometimes you want to commit
# work in progress):
#   git commit --no-verify
#
# Only ERRORS block. Warnings never do, and the judgement checks in
# agents-lint-checks.md are not involved at all: they need a model, and a commit
# hook that needs a model is a commit hook people disable within a week.
#
# What that buys you is narrow and worth being honest about. This catches a
# missing frontmatter field, a link that doesn't resolve, a file in the wrong
# folder for its declared type — things with exactly one correct answer. It
# catches none of the failures that actually matter most: a page that quietly
# contradicts another one, an entity filed in the wrong place, a summary that
# stopped being true. Those need reading, and reading is the LINT operation's job.

set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

if ! command -v python3 >/dev/null 2>&1; then
  echo "pre-commit: python3 not found — skipping lint (commit allowed)." >&2
  exit 0
fi

if [ ! -f scripts/lint.py ]; then
  echo "pre-commit: scripts/lint.py not found — skipping lint (commit allowed)." >&2
  exit 0
fi

if ! python3 scripts/lint.py --quiet; then
  echo "pre-commit: blocked by the errors above." >&2
  echo "            Run 'python3 scripts/lint.py' for the full report." >&2
  exit 1
fi

# The maintainer's private names never reach this public repo (Repo Gates, 2026-11-26): the staged content is checked.
if ! python3 scripts/check_private_names.py --staged; then
  echo "pre-commit: blocked: a private name is staged (see above)." >&2
  exit 1
fi

exit 0
