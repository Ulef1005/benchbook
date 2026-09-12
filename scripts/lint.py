#!/usr/bin/env python3
"""Mechanical LINT checks for a benchbook wiki.

    python3 scripts/lint.py            # full run, human-readable
    python3 scripts/lint.py --quiet    # errors only (what the pre-commit hook uses)

Exit code: 0 = no errors, 1 = at least one error. Warnings never affect the exit code,
because warnings gate nothing -- see agents-lint-checks.md.

Everything in here is deterministic. If a check needs reading comprehension, it does not
belong in this file; it belongs in agents-lint-checks.md as a judgement check, run by the
agent during a LINT operation. That split is the whole design: a model is expensive and
non-repeatable, so it should spend its attention on contradictions and placement calls, not
on whether a required frontmatter field is present.

This script is deliberately not auto-fixing. It reports; a human or an agent decides.
"""
import argparse
import os
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
SKILLS_DIR = ROOT / ".claude" / "skills"

# ---------------------------------------------------------------- constants

# Domains are *derived from the folder tree*, not hardcoded -- installing a domain pack
# creates its folder, and a constant here would silently go stale the day you do that.
GLOBAL_FOLDERS = {"sources", "people", "log"}

# Page types. Extend this when you install a pack that adds types (books adds author/
# series/candidate; cooking adds recipe) -- the pack's README says so.
TYPES = {"source", "entity", "reference", "overview", "project"}
PACK_TYPES = {"book", "author", "series", "candidate", "recipe", "trip"}

ENTITY_STATUS = {"owned", "considered", "retired", "reference-only"}
PROJECT_STATUS = {"planned", "active", "on-hold", "deployed", "completed", "abandoned"}
OPEN_PROJECT_STATUS = {"active", "planned"}

UNIVERSAL_REQUIRED = ["title", "type", "created", "domain", "publish", "sources"]

SHAPE_TAGS = {"concept", "comparison", "ranking", "buying-guide", "guide"}

# The controlled predicate vocabulary -- agents-domain-knowledge.md is the rule source.
# 18 core + 8 provenance/ownership + 10 operations. If you dropped the operations block
# because you don't run services, drop it here too; the check only fires on predicates
# you actually use.
PREDICATES = {
    # core
    "is_a", "made_by", "makes", "includes", "part_of", "uses", "used_by", "runs",
    "runs_on", "integrates_with", "competes_with", "replaces", "requires", "supports",
    "enables", "evaluates", "evaluated_for", "compared_to",
    # provenance and ownership
    "built_by", "builds", "owns", "owned_by", "feeds", "fed_by", "triggered_by", "triggers",
    # operations
    "backed_up_by", "backs_up", "secures", "secured_by", "monitors", "monitored_by",
    "fronts", "fronted_by", "stores_data_on", "stores_data_for",
}

PROJECT_SECTIONS = ["## Summary", "## Use Cases", "## Hard- and Software",
                    "## Plan / Phases", "## Open Questions", "## Log"]
DEPLOYED_SECTIONS = ["## Version Control", "## Backup Concept", "## Cron Jobs"]

BLOAT_WORDS = 500
BLOAT_WORDS_BY_TYPE = {"entity": 3000}      # hubs are dense on purpose
BLOAT_EXEMPT_TYPES = {"project", "source", "reference", "trip"}
BLOAT_SHOW = 10                              # the rest is a standing backlog, not a list
THIN_WORDS = 60

INDEX_ENTRY_WORDS = 30                       # per-entry cap in index files
INDEX_ENTRY_SHOW = 10

RAW_ARCHIVE_DAYS = 14
LOG_MAX_LINES = 500
LOG_VALID_OPS = {"ingest", "create", "lint", "query", "skill"}  # `update` deliberately absent
LOG_ENTRY_MAX_WORDS = 40
LOG_RECENT_ENTRIES = 40                      # older entries predate the rule; not retroactive

CHANNEL_TRIGGER = 3

SKILL_MATURITY = {"draft", "tested", "hardened"}
SKILL_DESC_MAX = 1024                        # the documented description limit

SCRIPTS_SECRET_EXTS = {".yaml", ".yml", ".json"}
SECRET_KEY_RE = re.compile(
    r"^\s*[\"']?(password|passwd|api_key|apikey|secret|token|access_key)[\"']?\s*[:=]\s*(.+)$",
    re.I)
SAFE_VALUE_RE = re.compile(
    r"^[\"']?(\$\{?[A-Z_]|!secret\b|<[^>]+>|\{\{|op://|env\.|null|~|\"\"|''|changeme|your[-_])",
    re.I)

MD_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")

# ---------------------------------------------------------------- helpers


def resolve_md_link(linkpath, source_file):
    """Resolve a markdown link relative to the file it appears in.

    Returns None for external or non-.md links -- there is nothing local to check.
    """
    path = linkpath.split("#", 1)[0]
    if not path or path.startswith(("http://", "https://", "mailto:")):
        return None
    if not path.endswith(".md"):
        return None
    return (source_file.parent / path).resolve()


def parse_frontmatter(text):
    """Minimal YAML-subset parser: scalars, inline lists, block lists.

    Deliberately not a YAML library: this needs to run with no dependencies, in any
    clone, with no install step. It handles the subset the page conventions actually
    use, and a page that needs more than this subset is a page that has outgrown the
    convention.
    """
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text
    fm, i, key = {}, 1, None
    while i < len(lines):
        line = lines[i]
        if line.strip() == "---":
            return fm, "\n".join(lines[i + 1:])
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val == "":
                fm[key] = []
            elif val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                items = [x.strip().strip("\"'") for x in inner.split(",")] if inner else []
                fm[key] = [x for x in items if x]
            else:
                fm[key] = val.strip("\"'")
        elif key is not None and re.match(r"^\s+-\s+", line):
            fm[key] = fm[key] if isinstance(fm[key], list) else []
            fm[key].append(re.sub(r"^\s+-\s+", "", line).strip().strip("\"'"))
        i += 1
    return fm, ""


def parse_skill_fm(text):
    """SKILL.md frontmatter -- top-level scalars plus one level of nesting, dot-flattened."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fm, parent = {}, None
    for line in text[4:end].split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if m:
            k, v = m.group(1), m.group(2).strip().strip("\"'")
            fm[k] = v
            parent = k if v == "" else None
            continue
        m = re.match(r"^\s+([A-Za-z][\w-]*):\s*(.*)$", line)
        if m and parent:
            fm[f"{parent}.{m.group(1)}"] = m.group(2).strip().strip("\"'")
    return fm


def strip_code(body):
    """Drop fenced and inline code before scanning for real links.

    Template and runbook pages legitimately *show* example markdown whose links are
    written from the perspective of the page being templated, not from the current
    file's location. Those are documentation, not navigation, and link-checking them
    produces confident false positives.
    """
    body = re.sub(r"^```.*?^```", " ", body, flags=re.S | re.M)
    return re.sub(r"`[^`\n]*`", " ", body)


def body_without_append_only(body):
    """Body minus the sections that are supposed to grow forever.

    `## Log`, `## Change History` and `## Modifications` are append-only by convention,
    so counting them toward a "keep pages concise" guideline penalises exactly the
    behaviour the wiki wants.
    """
    return re.sub(r"\n## (?:Log|Change History|Modifications)\b.*?(?=\n## [A-Z]|\Z)",
                  "\n", body, flags=re.S)


def words_in_body(body):
    return len(re.findall(r"\w+", re.sub(r"```.*?```", " ", body, flags=re.S)))


def relations_block(body):
    """The one `## Relations` section, matched **exactly**.

    Prefix matching would also scan `## Relationship to the old system`, which is prose.
    Returns (text, start_index) or (None, -1).
    """
    m = re.search(r"^## Relations\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
    return (m.group(1), m.start()) if m else (None, -1)


def rel(p):
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


class Report:
    def __init__(self):
        self.errors = defaultdict(list)
        self.warnings = defaultdict(list)
        self.info = defaultdict(list)

    def err(self, check, msg):
        self.errors[check].append(msg)

    def warn(self, check, msg):
        self.warnings[check].append(msg)

    def note(self, check, msg):
        self.info[check].append(msg)

    def n_err(self):
        return sum(len(v) for v in self.errors.values())

    def n_warn(self):
        return sum(len(v) for v in self.warnings.values())


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quiet", action="store_true",
                    help="print errors only (used by the pre-commit hook)")
    args = ap.parse_args()

    rep = Report()
    if not WIKI.is_dir():
        print(f"no wiki/ folder at {WIKI}", file=sys.stderr)
        return 2

    domains = sorted(d.name for d in WIKI.iterdir()
                     if d.is_dir() and d.name not in GLOBAL_FOLDERS)
    all_types = TYPES | PACK_TYPES

    pages = {}          # Path -> (frontmatter, body)
    for path in sorted(WIKI.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if fm is None:
            # DEMO.md documents the demo content and is not itself a page.
            if path.name != "DEMO.md":
                rep.err("Frontmatter", f"{rel(path)}: no YAML frontmatter")
            continue
        pages[path] = (fm, body)

    # ---- Frontmatter: required fields, enums, tag vocabulary
    for path, (fm, body) in pages.items():
        for field in UNIVERSAL_REQUIRED:
            if field not in fm or (fm[field] == "" and field != "sources"):
                rep.err("Frontmatter", f"{rel(path)}: missing `{field}:`")
        ptype = fm.get("type", "")
        if ptype and ptype not in all_types:
            rep.err("Frontmatter", f"{rel(path)}: unknown type `{ptype}`")
        dom = fm.get("domain", "")
        if dom and dom != "null" and dom not in domains:
            rep.err("Frontmatter", f"{rel(path)}: domain `{dom}` has no folder in wiki/")
        if str(fm.get("publish", "")).lower() not in ("true", "false"):
            rep.err("Frontmatter", f"{rel(path)}: `publish:` must be true or false")

        status = fm.get("status", "")
        is_person = path.parent.name == "people"
        if ptype == "entity" and not is_person:
            if not status:
                rep.err("Frontmatter", f"{rel(path)}: entity page needs `status:`")
            elif status not in ENTITY_STATUS:
                rep.err("Frontmatter",
                        f"{rel(path)}: entity status `{status}` not in {sorted(ENTITY_STATUS)}")
        if ptype == "project":
            if not status:
                rep.err("Frontmatter", f"{rel(path)}: project page needs `status:`")
            elif status not in PROJECT_STATUS:
                rep.err("Frontmatter",
                        f"{rel(path)}: project status `{status}` not in {sorted(PROJECT_STATUS)}")
        if ptype == "reference":
            tags = fm.get("tags", [])
            tags = tags if isinstance(tags, list) else [tags]
            if not SHAPE_TAGS & set(tags):
                rep.err("Frontmatter",
                        f"{rel(path)}: reference page needs one shape tag {sorted(SHAPE_TAGS)}")
        created = fm.get("created", "")
        if created and not re.match(r"^\d{4}-\d{2}-\d{2}$", str(created)):
            rep.err("Frontmatter", f"{rel(path)}: `created: {created}` is not YYYY-MM-DD")

    # ---- Domain <-> folder consistency
    for path, (fm, body) in pages.items():
        parts = path.relative_to(WIKI).parts
        if len(parts) == 1 or parts[0] in GLOBAL_FOLDERS:
            continue      # meta files at root; sources/ and people/ are global
        dom = fm.get("domain", "")
        if dom and dom != "null" and dom != parts[0]:
            rep.err("Domain/folder",
                    f"{rel(path)}: `domain: {dom}` but the file sits under wiki/{parts[0]}/")

    # ---- Source page sections
    for path, (fm, body) in pages.items():
        if fm.get("type") != "source":
            continue
        for sec in ("## Summary", "## Sources"):
            if not re.search(rf"^{re.escape(sec)}\s*$", body, re.M):
                rep.err("Source sections", f"{rel(path)}: missing `{sec}`")
        tags = fm.get("tags", [])
        tags = tags if isinstance(tags, list) else [tags]
        if (fm.get("source_url") and "content-exempt" not in tags
                and not re.search(r"^## Content\s*$", body, re.M)):
            rep.warn("Source sections",
                     f"{rel(path)}: has `source_url:` but no `## Content` "
                     f"(tag `content-exempt` if that is deliberate)")

    # ---- Project section template
    for path, (fm, body) in pages.items():
        if fm.get("type") != "project":
            continue
        found = [s for s in PROJECT_SECTIONS
                 if re.search(rf"^{re.escape(s)}\s*$", body, re.M)]
        for sec in PROJECT_SECTIONS:
            if sec not in found:
                rep.err("Project template", f"{rel(path)}: missing `{sec}`")
        order = [body.index(s) for s in found]
        if order != sorted(order):
            rep.err("Project template", f"{rel(path)}: required sections are out of order")
        if fm.get("status") == "deployed":
            for sec in DEPLOYED_SECTIONS:
                if not re.search(rf"^{re.escape(sec)}\s*$", body, re.M):
                    rep.err("Project template",
                            f"{rel(path)}: `status: deployed` also requires `{sec}`")

    # ---- Project relations: required on open projects, directly after ## Summary
    for path, (fm, body) in pages.items():
        if fm.get("type") != "project" or fm.get("status") not in OPEN_PROJECT_STATUS:
            continue
        block, start = relations_block(body)
        if block is None:
            rep.err("Project relations",
                    f"{rel(path)}: `status: {fm['status']}` requires a `## Relations` section")
            continue
        headings = [(m.start(), m.group(1))
                    for m in re.finditer(r"^## (.+?)\s*$", body, re.M)]
        names = [h[1] for h in headings]
        if "Summary" in names:
            i = names.index("Summary")
            if i + 1 >= len(names) or names[i + 1] != "Relations":
                rep.err("Project relations",
                        f"{rel(path)}: `## Relations` must come directly after `## Summary`")

    # ---- Predicate vocabulary: every page carrying the table
    for path, (fm, body) in pages.items():
        block, _ = relations_block(body)
        if not block:
            continue
        for line in block.split("\n"):
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3 or cells[0].lower() in ("subject", "subjekt"):
                continue
            if not set(cells[0]) - set("-: "):
                continue                      # separator row
            pred = re.sub(r"[`*]", "", cells[1]).strip()
            if pred and pred not in PREDICATES:
                rep.warn("Predicates",
                         f"{rel(path)}: `{pred}` is not in the controlled vocabulary "
                         f"(most such facts belong in `## Key Facts`)")

    # ---- Broken relative links + raw/ paths in bodies
    for path, (fm, body) in pages.items():
        for _, link in MD_LINK_RE.findall(strip_code(body)):
            if link.startswith("raw/") or "/raw/" in link or link.startswith("../raw/"):
                rep.err("Raw link", f"{rel(path)}: body links `{link}` "
                                    f"(raw paths belong in frontmatter, Hard Rule 14)")
            target = resolve_md_link(link, path)
            if target is not None and not target.is_file():
                rep.err("Broken links", f"{rel(path)}: `{link}` does not resolve")

    # ---- Duplicate / sync-artifact files
    for path in WIKI.rglob("*.md"):
        if re.search(r" \d+\.md$", path.name) or "conflicted copy" in path.name:
            rep.err("Duplicates", f"{rel(path)}: sync-tool artifact — confirm, then delete")

    # ---- Index coverage + orphans + entry length
    index_files = sorted(WIKI.glob("index*.md"))
    indexed, dead = set(), []
    for idx in index_files:
        text = idx.read_text(encoding="utf-8")
        _, ibody = parse_frontmatter(text)
        for line in ibody.split("\n"):
            m = re.match(r"^\s*[-*]\s*\[([^\]]+)\]\(([^)\s]+)\)\s*(.*)$", line)
            if not m:
                continue
            target = resolve_md_link(m.group(2), idx)
            if target is None:
                continue
            if target.is_file():
                indexed.add(target)
            else:
                dead.append((idx, m.group(2)))
            words = len(re.findall(r"\w+", re.sub(r"\[[^\]]*\]\([^)]*\)", "", m.group(3))))
            if words > INDEX_ENTRY_WORDS:
                rep.warn("Index entry length",
                         f"{rel(idx)}: `{m.group(1)}` — {words} words of prose "
                         f"(cap {INDEX_ENTRY_WORDS})")
    for idx, link in dead:
        rep.err("Index", f"{rel(idx)}: dead link `{link}`")

    inbound = defaultdict(int)
    for path, (fm, body) in pages.items():
        for _, link in MD_LINK_RE.findall(strip_code(body)):
            target = resolve_md_link(link, path)
            if target and target.is_file() and target != path:
                inbound[target] += 1

    for path, (fm, body) in pages.items():
        if fm.get("type") == "overview" or path.name.startswith("index"):
            continue
        tags = fm.get("tags", [])
        tags = tags if isinstance(tags, list) else [tags]
        if path not in indexed:
            rep.warn("Index coverage", f"{rel(path)}: not listed in any index file")
        if inbound[path] == 0 and "standalone-reference" not in tags:
            rep.warn("Orphans", f"{rel(path)}: no inbound links from any page")

    # ---- Page length + thin pages
    bloated = []
    for path, (fm, body) in pages.items():
        ptype = fm.get("type", "")
        # wiki/log/ holds append-only records and generated LINT reports. Their length is
        # a function of how much happened, not of editorial sprawl.
        if ptype in BLOAT_EXEMPT_TYPES or path.parent.name in ("log", "log-archive"):
            continue
        limit = BLOAT_WORDS_BY_TYPE.get(ptype, BLOAT_WORDS)
        n = words_in_body(body_without_append_only(body))
        if n > limit:
            bloated.append((n, limit, path))
        elif n < THIN_WORDS and ptype in ("entity", "reference"):
            rep.warn("Thin pages", f"{rel(path)}: {n} words — real page, or a stub?")
    for n, limit, path in sorted(bloated, reverse=True)[:BLOAT_SHOW]:
        rep.warn("Page length", f"{rel(path)}: {n} words (limit {limit}) — consider splitting")
    if len(bloated) > BLOAT_SHOW:
        rep.note("Page length",
                 f"{len(bloated) - BLOAT_SHOW} further pages over the limit — standing backlog")

    # ---- Channel trigger
    channels = defaultdict(list)
    for path, (fm, body) in pages.items():
        if fm.get("type") == "source" and fm.get("channel"):
            channels[fm["channel"]].append(path)
    existing = {p.stem for p in WIKI.rglob("entities/*.md")}
    for origin, srcs in sorted(channels.items()):
        if len(srcs) >= CHANNEL_TRIGGER and origin not in existing:
            rep.note("Channel trigger",
                     f"`{origin}` has {len(srcs)} sources and no entity page — propose one")

    # ---- Reference page audit
    for path, (fm, body) in pages.items():
        if fm.get("type") != "reference":
            continue
        compared = len(set(MD_LINK_RE.findall(strip_code(body))))
        if compared < 4:
            rep.note("Reference audit",
                     f"{rel(path)}: links {compared} pages — conversion candidate if it is a "
                     f"comparison (project-attached records are exempt by shape)")

    # ---- Log discipline
    logfile = WIKI / "log" / "log.md"
    if logfile.is_file():
        text = logfile.read_text(encoding="utf-8")
        lines = text.split("\n")
        if len(lines) > LOG_MAX_LINES:
            rep.warn("Log", f"log.md is {len(lines)} lines (>{LOG_MAX_LINES}) — archive the "
                            f"oldest entries to log/log-archive/YYYY-MM.md")
        entries = re.findall(r"^## \[(\d{4}-\d{2}-\d{2})\] (\w+) \|(.*?)(?=^## \[|\Z)",
                             text, re.M | re.S)
        for stamp, op, rest in entries[-LOG_RECENT_ENTRIES:]:
            if op not in LOG_VALID_OPS:
                rep.err("Log", f"log.md [{stamp}]: `{op}` is not a valid op "
                               f"{sorted(LOG_VALID_OPS)}")
            words = len(re.findall(r"\w+", rest.split("\n", 1)[-1]))
            if words > LOG_ENTRY_MAX_WORDS * 2:
                rep.warn("Log", f"log.md [{stamp}] {op}: {words} words — the spec is 1–3 lines; "
                                f"this probably belongs on a page")

    # ---- raw/ archival candidates
    cutoff = datetime.now() - timedelta(days=RAW_ARCHIVE_DAYS)
    for path, (fm, body) in pages.items():
        rawref = fm.get("raw_file")
        if not rawref or isinstance(rawref, list):
            continue
        rawpath = ROOT / rawref
        if rawpath.is_file() and datetime.fromtimestamp(rawpath.stat().st_mtime) < cutoff:
            rep.note("Raw archival",
                     f"{rawref} is older than {RAW_ARCHIVE_DAYS} days — "
                     f"move to raw/_archived/{fm.get('domain', 'misc')}/ (never delete)")

    # ---- scripts/ store
    scripts_dir = ROOT / "scripts"
    if scripts_dir.is_dir():
        linked = set()
        for path, (fm, body) in pages.items():
            for _, link in MD_LINK_RE.findall(strip_code(body)):
                if "scripts/" in link:
                    linked.add(link.split("scripts/", 1)[1].split("/")[0])
                    target = (ROOT / link.lstrip("./")).resolve() if link.startswith(
                        ("scripts/", "./scripts/")) else resolve_md_link(link, path)
                    if (link.startswith(("scripts/", "./scripts/"))
                            and not (ROOT / link.lstrip("./")).exists()):
                        rep.err("Scripts store",
                                f"{rel(path)}: links `{link}`, which does not exist on disk")
        for sub in sorted(p for p in scripts_dir.iterdir() if p.is_dir()):
            if not (sub / "README.md").is_file():
                rep.warn("Scripts store", f"scripts/{sub.name}/: no README.md")
            if sub.name not in linked:
                rep.warn("Scripts store",
                         f"scripts/{sub.name}/: no inbound link from any wiki page")
        for f in scripts_dir.rglob("*"):
            if f.suffix.lower() not in SCRIPTS_SECRET_EXTS or not f.is_file():
                continue
            for i, line in enumerate(f.read_text(encoding="utf-8",
                                                 errors="replace").split("\n"), 1):
                m = SECRET_KEY_RE.match(line)
                if m and not SAFE_VALUE_RE.match(m.group(2).strip()):
                    rep.err("Scripts secrets",
                            f"{rel(f)}:{i}: `{m.group(1)}` looks like a literal value")

    # ---- Skills: disk is the source of truth, the roster is a view over it
    roster = SKILLS_DIR / "README.md"
    if SKILLS_DIR.is_dir():
        on_disk = sorted(d.name for d in SKILLS_DIR.iterdir() if (d / "SKILL.md").is_file())
        for name in on_disk:
            fm = parse_skill_fm((SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8"))
            if fm is None:
                rep.err("Skills", f".claude/skills/{name}/SKILL.md: no frontmatter")
                continue
            if fm.get("name") != name:
                rep.err("Skills",
                        f".claude/skills/{name}: frontmatter `name: {fm.get('name')}` "
                        f"≠ directory name")
            if not fm.get("description"):
                rep.err("Skills", f".claude/skills/{name}: missing `description:`")
            elif len(fm["description"]) > SKILL_DESC_MAX:
                rep.err("Skills",
                        f".claude/skills/{name}: description is {len(fm['description'])} chars "
                        f"(max {SKILL_DESC_MAX})")
            mat = fm.get("maturity")
            if mat and mat not in SKILL_MATURITY:
                rep.err("Skills",
                        f".claude/skills/{name}: `maturity: {mat}` not in "
                        f"{sorted(SKILL_MATURITY)}")
            elif not mat:
                rep.warn("Skills", f".claude/skills/{name}: no `maturity:` — "
                                   f"new and dead look identical without it")
        if roster.is_file():
            rtext = roster.read_text(encoding="utf-8")
            for name in on_disk:
                if not re.search(rf"\b{re.escape(name)}\b", rtext):
                    rep.err("Skills", f".claude/skills/{name}: on disk but absent from the "
                                      f"roster in .claude/skills/README.md")
            for m in re.finditer(r"^\s*[-*|]\s*.*?`([a-z][a-z0-9-]{2,})`", rtext, re.M):
                cand = m.group(1)
                if cand not in on_disk and (SKILLS_DIR / cand).exists() is False and \
                        re.search(rf"`{re.escape(cand)}`\s*(\||—|-)", rtext):
                    rep.warn("Skills", f"roster names `{cand}`, which has no directory "
                                       f"in .claude/skills/")

    # ---- Publish audit (counts only, no enforcement)
    pub = defaultdict(lambda: [0, 0])
    for path, (fm, body) in pages.items():
        dom = fm.get("domain") or "null"
        pub[dom][0 if str(fm.get("publish")).lower() == "true" else 1] += 1

    # ---------------------------------------------------------------- output
    def emit(title, bucket, marker):
        if not bucket:
            return
        print(f"\n{marker} {title}")
        for check in sorted(bucket):
            print(f"\n  {check}")
            for msg in bucket[check]:
                print(f"    - {msg}")

    if args.quiet:
        emit("Errors", rep.errors, "✗")
        if rep.n_err():
            print(f"\n{rep.n_err()} error(s). Fix them, or commit with --no-verify.\n")
        return 1 if rep.n_err() else 0

    print(f"benchbook lint — {date.today().isoformat()}")
    print(f"{len(pages)} pages · {len(domains)} domains ({', '.join(domains)})")

    emit("Errors", rep.errors, "✗")
    emit("Warnings", rep.warnings, "⚠")
    emit("Notes", rep.info, "·")

    print("\n## Stats\n")
    print("| Domain | published | unpublished |")
    print("|---|---|---|")
    for dom in sorted(pub):
        print(f"| {dom} | {pub[dom][0]} | {pub[dom][1]} |")
    bytype = defaultdict(int)
    for path, (fm, body) in pages.items():
        bytype[fm.get("type", "?")] += 1
    print("\n| Type | count |")
    print("|---|---|")
    for t, n in sorted(bytype.items(), key=lambda kv: -kv[1]):
        print(f"| {t} | {n} |")
    if index_files:
        sizes = sorted(((f.stat().st_size, f.name) for f in index_files), reverse=True)
        print("\nindex files: " + " · ".join(f"{n}: {s // 1024 or 1} KB" for s, n in sizes))
    if logfile.is_file():
        print(f"log.md: {len(logfile.read_text(encoding='utf-8').splitlines())} lines")

    print(f"\n{rep.n_err()} error(s), {rep.n_warn()} warning(s).")
    return 1 if rep.n_err() else 0


if __name__ == "__main__":
    sys.exit(main())
