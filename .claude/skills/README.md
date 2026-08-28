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

## Skills ship in a later phase

This starter's skill set is not yet populated. See [10 — Skills](../../docs/10-skills.md) for
what's planned and, more usefully, for **when to write one of your own**:

> When you've performed the same multi-step sequence for the third time, write a skill.

Third time, not first. The first time you don't know which parts are essential; the second
you're guessing; by the third you know what the steps actually are and which ones you skipped
without consequence.
