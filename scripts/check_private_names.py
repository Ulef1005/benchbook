#!/usr/bin/env python3
"""Private names must never reach this public repository (Repo Gates, 2026-11-26).

    python3 scripts/check_private_names.py            # every tracked file (the land tier, scripts/check.sh)
    python3 scripts/check_private_names.py --staged   # the staged content (the commit hook)

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
        raise SystemExit(f"private names: {path} holds no patterns")
    return re.compile("|".join(expr), re.IGNORECASE)


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
    if staged:
        names = [n for n in git("diff", "--cached", "--name-only", "-z", "--diff-filter=ACMR").decode().split("\0") if n]
    else:
        names = [n for n in git("ls-files", "-z").decode().split("\0") if n]
    hits = []
    for name in names:
        if name == SELF:
            continue
        try:
            data = git("show", f":{name}") if staged else (ROOT / name).read_bytes()
            text = data.decode("utf-8")
        except (UnicodeDecodeError, OSError, subprocess.CalledProcessError):
            continue   # binary or unreadable: gitleaks covers secrets, names live in text
        hits += [f"{name}:{n}" for n, line in enumerate(text.splitlines(), 1) if rx.search(line)]
    if hits:
        print(f"private names: FAILED, {len(hits)} line(s) match the maintainer's patterns:", file=sys.stderr)
        for h in hits[:40]:
            print(f"  {h}", file=sys.stderr)
        return 1
    print(f"private names: clean ({len(names)} {'staged ' if staged else ''}file(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
