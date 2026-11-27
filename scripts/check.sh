#!/usr/bin/env bash
# GATE TABLE: the gate of benchbook (group: github-public, minimal; ai-wiki Test Standard § Gates, Repo Gates).
# A change to this table or to this file needs Ulf's yes: the commit carries `Gate-Approved: <date> "<his words>"`.
# Tiers: commit = scripts/pre-commit.sh (lint errors, private names on the staged files);
#        land = this script on the Mac; ci = this script in .github/workflows/check.yml (GITHUB_ACTIONS set).
# benchbook is dormant and lands by direct push to main (Ulf, 2026-11-26: "Minimal gate").
#
# id             tier          trigger   catches
# lint           land, ci      always    wiki lint errors (frontmatter, links, folders)
# private-names  commit, land  always    the maintainer's private names (patterns file outside the repo, never in CI)
# secrets        land          always    secrets in the history (CI: the workflow's gitleaks action, with its marker)
#
# Every step runs, so one failure cannot hide another; the failed steps are listed at the end.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

failed=()
step() {
  local name=$1
  shift
  echo "== $name"
  "$@" || failed+=("$name")
}

secrets() {
  if [[ -n ${GITHUB_ACTIONS:-} ]]; then
    # the step after the gitleaks action sets the marker only when the scan step succeeded
    if [[ ${GATE_SECRET_SCAN:-} == "done" ]]; then
      echo "Secret scan: the workflow's gitleaks action is this run's one scan (Repo Gates)."
      return 0
    fi
    echo "ERROR: on GitHub the secret scan is the workflow's gitleaks step, and it did not run or did not pass (no GATE_SECRET_SCAN marker)"
    return 1
  fi
  if ! command -v gitleaks >/dev/null 2>&1; then
    echo "ERROR: gitleaks is not installed (brew install gitleaks): the public repo's secret scan cannot run"
    return 1
  fi
  gitleaks detect --no-banner
}

step lint python3 scripts/lint.py --quiet
step private-names python3 scripts/check_private_names.py
step secrets secrets

if ((${#failed[@]})); then
  printf 'FAILED: %s\n' "${failed[*]}"
  exit 1
fi
echo 'All checks passed'
