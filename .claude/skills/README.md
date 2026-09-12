# Skills

A skill is a packaged, named procedure the agent can invoke — instructions for a recurring
multi-step task, triggered by a command or by recognising the situation.

The contract (`agents-core.md`) defines *what the wiki is*. Skills define *how specific jobs
get done in it*.

## The one tool-specific part

Everything else in benchbook is plain markdown that any agentic tool can read. Skills are the
exception: **where they live and how they're invoked differs per tool.**

| Tool | Location |
|---|---|
| Claude Code | `.claude/skills/<name>/SKILL.md`, invoked as `/<name>` |
| Codex and other `AGENTS.md`-based tools | prompt files, or procedures described in `AGENTS.md` |
| Cursor | `.cursor/rules/`, or custom commands |
| Anything else | wherever that tool keeps reusable prompts |

This folder uses the Claude Code layout because that's where the system was built. If you're
on a different tool, **the procedures port fine — only the packaging changes.** Each skill is
an ordered list of steps in plain language; move it to your tool's equivalent location and it
works.

You can also skip skills entirely at first. The contract alone is enough to run INGEST, QUERY
and LINT — you just describe what you want instead of typing a command.

## What's here

**This table is a *view* over the directories next to it, not a second source of truth.**
`scripts/lint.py` errors if the two disagree in either direction — a directory with no row, or
a row with no directory. That check exists because this exact table was wrong the day it was
written: `benchbook-design` shipped in this folder and was never listed here, and nobody
noticed for two weeks.

The **core six** — domain-independent, used in every wiki regardless of subject:

| Skill | Maturity | What it does |
|---|---|---|
| `wiki-ingest` | `tested` | The full ingest workflow — detect, extract, propose domain, dispatch, post-flight |
| `wiki-project-start` | `tested` | Create a project page with all required sections and a **gated** plan stub |
| `wiki-project-open` | `tested` | Orient to an existing project — status, relations, last activity, open questions |
| `wiki-project-review` | `tested` | Attack a plan one question at a time, before anything is built |
| `wiki-lint` | `tested` | Full maintenance pass — mechanical script, judgement checks, dated report |
| `wiki-session-close` | `tested` | Verify, log, gate-check, commit, push |

Plus one that is not a wiki operation at all:

| Skill | Maturity | What it does |
|---|---|---|
| `benchbook-design` | `tested` | The visual language for the published site — palette, type, mark, layout, copy rules |

**Domain skills live with their domain**, not here — see `domains/<name>/skills/`. Installing a
pack copies its skills into this folder. Available: `research` (knowledge), `deploy-runbook`
(home), `book-capture` (books), `recipe-capture` (cooking), `game-capture` + `game-drop`
(gaming). All are `maturity: draft` **in this repo** — they run in the wiki they came from, but
nothing here has exercised them, and "works elsewhere" is not the same claim as "works here".

## Two frontmatter fields worth understanding

Every SKILL.md here carries `maturity:` and, where it writes pages, `outputs:`.

```yaml
maturity: draft | tested | hardened
outputs: wiki/projects/*.md
```

**`maturity:` separates "no invocations because it is new" from "no invocations because it is
dead".** Those look identical from usage data alone, and the ambiguity is what lets a broken
skill sit unnoticed — you assume the silence means nobody needed it. One human-set line
resolves it. `draft` = written, not yet proven. `tested` = run end to end at least once.
`hardened` = run repeatedly, failure modes known.

**`outputs:` is a glob naming the page shape a skill produces.** It sounds like documentation
and is actually the machinery: it turns "is this recurring work covered by a skill?" from a
judgement call into a comparison. Look at the pages created over the last N sessions, match
them against every declared `outputs:` glob, and what's left over is the honest answer to
*what am I doing by hand, repeatedly, that nothing covers*.

The same comparison run backwards is just as useful: a skill that *declares* a shape which keeps
getting created while that skill is never invoked is being **bypassed** — usually because its
trigger wording doesn't match how you actually ask for it.

## Writing your own

See [10 — Skills](../../docs/10-skills.md) for the full guidance. The trigger:

> When you've performed the same multi-step sequence for the third time, write a skill.

Third time, not first. The first time you don't know which parts are essential; the second
you're guessing; by the third you know what the steps actually are and which ones you skipped
without consequence.

When you add one: create the directory, set `maturity: draft` and an `outputs:` glob if it
creates pages, then add a row to the table above. Run `python3 scripts/lint.py` — it fails
until the folder and the table agree, which is the point.
