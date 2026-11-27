#!/usr/bin/env python3
"""Private names must never reach this public repository (Repo Gates, 2026-11-26).

    python3 scripts/check_private_names.py            # every file of HEAD, as it lands (scripts/check.sh)
    python3 scripts/check_private_names.py --staged   # the staged content (the commit hook)

File names are checked as well as file content; text that is not UTF-8 is read with replacement characters, so a
name in Latin-1 text is still found. A git error fails the check.

The patterns are the maintainer's own, one regular expression per line, `#` starts a comment, matched case-insensitively.
They live outside the repository and never go to CI: BENCHBOOK_PRIVATE_PATTERNS_FILE, else the shared file in ai-wiki
(~/Workspace/ai-wiki/scripts/brick-work-private-patterns.txt; Ulf, 2026-11-26: "Reuse brick-work's file"). A missing file
fails the check on the Mac; on GitHub Actions the check says it cannot run there and passes. A hit prints the path and
line number only, never the matched text, because this output can land in a public log.

Exit 0 clean, 1 a private name found or the patterns file missing, 2 usage."""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = Path.home() / "Workspace" / "ai-wiki" / "scripts" / "brick-work-private-patterns.txt"
SELF = "scripts/check_private_names.py"


def patterns(path):
    lines = [ln.strip() for ln in path.read_text().splitlines()]
    expr = [ln for ln in lines if ln and not ln.startswith("#")]
    if not expr:
        raise SystemExit(f"private names: FAILED, {path} holds no patterns")
    try:   # each line its own group, so one line's alternation cannot swallow another's
        return re.compile("|".join(f"(?:{e})" for e in expr), re.IGNORECASE)
    except re.error as e:
        raise SystemExit(f"private names: FAILED, a pattern in {path} is not a valid regex ({e})") from None


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), "-c", "core.quotePath=false", *args],
                          capture_output=True, check=True).stdout


def main(argv):
    if argv not in ([], ["--staged"]):
        print(__doc__.split("\n\n")[1], file=sys.stderr)
        return 2
    staged = argv == ["--staged"]
    if os.environ.get("GITHUB_ACTIONS"):
        print("private names: not checked on GitHub (the patterns file never leaves the Mac)")
        return 0
    path = Path(os.environ.get("BENCHBOOK_PRIVATE_PATTERNS_FILE", DEFAULT)).expanduser()
    if not path.is_file():
        print(f"private names: FAILED, no patterns file at {path} (set BENCHBOOK_PRIVATE_PATTERNS_FILE)", file=sys.stderr)
        return 1
    rx = patterns(path)
    try:
        if staged:
            names = [n for n in git("diff", "--cached", "--name-only", "-z", "--diff-filter=ACMRT").decode().split("\0") if n]
        else:
            names = [n for n in git("ls-tree", "-r", "-z", "--name-only", "HEAD").decode().split("\0") if n]
        hits = []
        for name in names:
            if rx.search(name):
                hits.append(f"{name} (the file name)")
            if name == SELF:
                continue
            data = git("show", f":{name}" if staged else f"HEAD:{name}")
            if b"\0" in data[:8000]:
                continue   # binary: gitleaks covers secrets, names live in text
            text = data.decode("utf-8", errors="replace")
            hits += [f"{name}:{n}" for n, line in enumerate(text.splitlines(), 1) if rx.search(line)]
    except subprocess.CalledProcessError as e:
        print(f"private names: FAILED, git {' '.join(e.cmd[3:5])} did not answer: the check cannot run", file=sys.stderr)
        return 1
    if hits:
        print(f"private names: FAILED, {len(hits)} line(s) match the maintainer's patterns:", file=sys.stderr)
        for h in hits[:40]:
            print(f"  {h}", file=sys.stderr)
        return 1
    print(f"private names: clean ({len(names)} {'staged ' if staged else ''}file(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
