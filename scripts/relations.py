#!/usr/bin/env python3
"""Neighbourhood lookup over the wiki's ## Relations triplet graph.

    ./scripts/relations.py esphome                  # inbound + outbound, depth 1
    ./scripts/relations.py hallway-display --depth 2  # walk two hops
    ./scripts/relations.py esp32-c6 --json          # machine-readable
    ./scripts/relations.py --orphans                # pages with no edges either way

The question this answers: "what should I read before working on X?"

Every edge is stored exactly once, on whichever page reads naturally (see
agents-domain-knowledge.md: "the subject of a row does not have to be the page's own
entity"), so a page's own table shows only half its relations. This reads the whole
graph and reports both directions for one page.

Depth 1 is the usable unit. Depth 2+ answers "what is the blast radius of changing
this", which is a rarer question and a much larger answer.

Traversal deliberately excludes the three symmetric predicates. integrates_with,
competes_with and compared_to are symmetric by definition, which makes every one of
them a 2-cycle; walking them turns a neighbourhood into the whole graph. They are
still reported at depth 1, where they are useful, just never followed.
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = os.path.join(ROOT, "wiki")

# Symmetric by definition -> every instance is a 2-cycle. Reported, never followed.
SYMMETRIC = {"integrates_with", "competes_with", "compared_to"}
DEPTH_CAP = 4  # bounds cost


def slug_of(cell):
    """Return the linked page slug in a table cell, or None if the cell is prose.

    Prose objects are conventional (`is_a | single-board computer`), so a missing
    link is normal, not a defect -- such nodes are shown but never traversed.
    """
    link = re.search(r"\]\(([^)]+?\.md)[^)]*\)", cell)
    return os.path.basename(link.group(1))[:-3] if link else None


def label_of(cell):
    txt = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cell)
    return re.sub(r"\s+", " ", re.sub(r"[`*]", "", txt)).strip()


def load_edges():
    """Parse every ## Relations table into (subj, pred, obj, stored_in) tuples."""
    edges = []
    for dirpath, _, names in os.walk(WIKI):
        for name in sorted(names):
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            # Exact heading match: `## Relationship to ...` is a different section,
            # and prefix matching would scan it as if it were a relations table.
            m = re.search(r"^## Relations\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
            if not m:
                continue
            for line in m.group(1).split("\n"):
                if not line.strip().startswith("|"):
                    continue
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) < 3 or cells[0].lower() in ("subject", "subjekt"):
                    continue
                if not set(cells[0]) - set("-: "):
                    continue  # separator row
                edges.append({
                    "subject": slug_of(cells[0]) or label_of(cells[0]),
                    "subject_is_page": slug_of(cells[0]) is not None,
                    "predicate": re.sub(r"[`*]", "", cells[1]).strip(),
                    "object": slug_of(cells[2]) or label_of(cells[2]),
                    "object_is_page": slug_of(cells[2]) is not None,
                    "note": label_of(cells[2]),
                    "stored_in": os.path.relpath(path, ROOT),
                })
    return edges


def neighbourhood(edges, seed, depth):
    """Breadth-first walk from seed, returning {hop: [edge, ...]}."""
    out_by, in_by = defaultdict(list), defaultdict(list)
    for e in edges:
        out_by[e["subject"]].append(e)
        in_by[e["object"]].append(e)

    seen, frontier, hops = {seed}, [seed], {}
    for hop in range(1, min(depth, DEPTH_CAP) + 1):
        found, nxt = [], []
        for node in frontier:
            for e in out_by.get(node, []):
                found.append(("out", e))
                if e["object_is_page"] and e["predicate"] not in SYMMETRIC:
                    nxt.append(e["object"])
            for e in in_by.get(node, []):
                found.append(("in", e))
                if e["subject_is_page"] and e["predicate"] not in SYMMETRIC:
                    nxt.append(e["subject"])
        # de-duplicate: an edge can be reached from both ends within one hop
        uniq, keys = [], set()
        for direction, e in found:
            k = (e["subject"], e["predicate"], e["object"])
            if k not in keys:
                keys.add(k)
                uniq.append((direction, e))
        if not uniq:
            break
        hops[hop] = uniq
        frontier = [n for n in dict.fromkeys(nxt) if n not in seen]
        seen.update(frontier)
        if not frontier:
            break
    return hops


def main():
    ap = argparse.ArgumentParser(add_help=True, description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page", nargs="?", help="page slug, e.g. esphome")
    ap.add_argument("--depth", type=int, default=1,
                    help=f"hops to walk (default 1, capped at {DEPTH_CAP})")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--orphans", action="store_true",
                    help="list pages carrying a ## Relations table but no edges")
    args = ap.parse_args()

    edges = load_edges()

    if args.orphans:
        touched = {e["subject"] for e in edges} | {e["object"] for e in edges}
        missing = []
        for dirpath, _, names in os.walk(WIKI):
            for name in sorted(n for n in names if n.endswith(".md")):
                slug = name[:-3]
                if slug not in touched:
                    missing.append(os.path.relpath(os.path.join(dirpath, name), ROOT))
        print(f"{len(missing)} pages have no ## Relations edge in either direction:")
        for p in missing:
            print(f"  {p}")
        return 0

    if not args.page:
        ap.print_usage(sys.stderr)
        print(f"\n{len(edges)} edges loaded. Pass a page slug, or --orphans.",
              file=sys.stderr)
        return 2

    seed = args.page[:-3] if args.page.endswith(".md") else os.path.basename(args.page)
    hops = neighbourhood(edges, seed, args.depth)

    if args.json:
        print(json.dumps({"page": seed, "depth": args.depth, "hops": {
            str(h): [{"direction": d, **e} for d, e in v] for h, v in hops.items()}},
            indent=2, ensure_ascii=False))
        return 0

    if not hops:
        print(f"{seed}: no ## Relations edges in either direction.")
        print("This is a normal state, not a defect -- relations are added at next")
        print("touch rather than backfilled, and an empty graph beats an invented one.")
        return 1

    total = sum(len(v) for v in hops.values())
    print(f"{seed} -- {total} edge(s) across {len(hops)} hop(s)\n")
    for hop, items in sorted(hops.items()):
        print(f"hop {hop}:")
        for direction, e in items:
            if direction == "out":
                arrow = f"{seed}  --{e['predicate']}-->  {e['note'][:70]}"
            else:
                arrow = f"{e['subject']}  --{e['predicate']}-->  {seed}"
            flag = "" if e["object_is_page"] or direction == "in" else "   [prose]"
            print(f"  {arrow}{flag}")
            print(f"      stored in {e['stored_in']}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
