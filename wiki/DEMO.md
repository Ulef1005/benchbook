# Demo content

The pages listed below are **synthetic examples**, not real notes. They exist so you can see a
populated wiki before you have one — how a source becomes entities, where the Entity Placement
Rule sends things, what a gated plan looks like, and how a finished project forks into a living
entity page.

Every demo **wiki page** carries `demo` in its `tags:`. The two `raw/` files have no
frontmatter — raw files aren't wiki pages — so they're removed by name.

From the repo root:

```bash
grep -rl "demo\]" wiki/ --include="*.md" | xargs rm
rm -rf wiki/DEMO.md raw/esphome-eink-walkthrough.md raw/_archived/knowledge
```

Then clear the demo entries out of `wiki/index*.md`, `wiki/overview.md` and `wiki/log/log.md`
— they're all marked *(demo)*.

Easiest route: **ask your agent to "remove the demo content"**. It'll do the files and the
index entries together, which is the bit that's tedious by hand.

## What's here, and what each page demonstrates

**There is one demo file in every folder**, so no directory is a mystery.

| Page | Demonstrates |
|---|---|
| `raw/esphome-eink-walkthrough.md` | The **immutable layer** — source material as it arrived, no frontmatter, not a wiki page |
| `raw/_archived/knowledge/older-eink-panel-notes.md` | What LINT's 14-day archival produces. It **moves**, never deletes — and it's why page bodies must never link a `raw/` path |
| `sources/esphome-eink-dashboard-walkthrough.md` | A source page with embedded `## Content`, `channel:`, `raw_file:`, and two-way links to the entities it produced |
| `knowledge/entities/esphome.md` | A general **tool** entity — a thing that exists in the world |
| `knowledge/entities/esp32-c6.md` | A general **product** entity, with a `## Relations` table using the controlled predicate vocabulary |
| `knowledge/references/low-power-esp32-boards.md` | A **reference** page — and why the 4+ rule exists, plus the cost: it's a snapshot while entities accumulate |
| `home/entities/hallway-display.md` | An **owned instance** with `change_history: true` — `## Current State` overwritten in place, `## Change History` append-only |
| `home/references/battery-build-checklist.md` | A `guide`-shaped reference; the two items learned the expensive way are marked as such |
| `projects/completed/hallway-display-build.md` | A finished project: options table with rejected alternatives, and the fork to a living entity page |
| `projects/office-air-quality-sensor.md` | A `planned` project with a **gated** plan stub — the rule that stops an agent building eleven files before you've decided anything |
| `projects/abandoned/kitchen-tablet-dashboard.md` | **Recording why work stopped.** Three dated reasons and the generalisable mistake — nothing is deleted, and this page is why the e-ink build exists |
| `projects/references/build-decision-log.md` | Decisions binding **more than one** project, which is what `projects/references/` is for |
| `people/alex-demo.md` | A person page — humans only, no `status:`, `domain: null` |
| `log/log-archive/2026-07.md` | What log archival produces once the live log passes 500 lines |

## Two things worth noticing

**The Entity Placement Rule, in the shape you'll meet it.** `esp32-c6` and `esphome` are in
`knowledge/` because they're things that exist in the world. `hallway-display` is in `home/`
because it's a specific thing that was built and is running. They link to each other. That call
is the one you'll make most often, and the one that's most expensive to get wrong.

**The pages form one story, and the abandoned one carries it.** A tablet was tried first and
abandoned for three specific reasons; those three reasons became the requirements that selected
e-ink; the build then hit a firmware regression that forced a version pin. Read in order —
`kitchen-tablet-dashboard` → `hallway-display-build` → `hallway-display` — you can see the
reasoning survive across a failure, a build, and an operational surprise.

That's the whole point of the system, and it's why the abandoned project is not deleted.
