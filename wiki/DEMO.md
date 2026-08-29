# Demo content

The pages listed below are **synthetic examples**, not real notes. They exist so you can see a
populated wiki before you have one — how a source becomes entities, where the Entity Placement
Rule sends things, what a gated plan looks like, and how a finished project forks into a living
entity page.

Every demo page carries `demo` in its `tags:`. To remove all of it:

```bash
grep -rl "^  - demo$\|demo\]" wiki/ --include="*.md" | grep -v DEMO.md | xargs rm
rm wiki/DEMO.md
```

Then clear the demo entries out of `wiki/index*.md`, `wiki/overview.md` and `wiki/log/log.md`,
or just ask your agent to.

## What's here, and what each page demonstrates

| Page | Domain | Demonstrates |
|---|---|---|
| `sources/esphome-eink-dashboard-walkthrough.md` | knowledge | A source page with embedded `## Content`, a `channel:` field, and two-way links to the entities it produced |
| `knowledge/entities/esphome.md` | knowledge | A general **tool** entity — the thing that exists in the world |
| `knowledge/entities/esp32-c6.md` | knowledge | A general **product** entity, with a `## Relations` table using the controlled predicate vocabulary |
| `home/entities/hallway-display.md` | home | An **owned instance** with `change_history: true` — `## Current State` overwritten in place, `## Change History` append-only |
| `projects/completed/hallway-display-build.md` | projects | A finished project: the options table with rejected alternatives, and the fork to a living entity page |
| `projects/office-air-quality-sensor.md` | projects | A `planned` project with a **gated** plan stub — the rule that stops an agent building eleven files before you've decided anything |

## The one thing worth noticing

`esp32-c6` and `esphome` are in `knowledge/` because they're things that exist in the world.
`hallway-display` is in `home/` because it's a specific thing that was built and is running.
They link to each other.

That split is the Entity Placement Rule, and it's the call you'll make most often.
