# Skills

A skill is a packaged, named procedure the agent can invoke — a set of instructions for a
recurring multi-step task, in a file, triggered by a command or by recognising the situation.

The contract defines *what the wiki is*. Skills define *how specific jobs get done in it*.

> **Skills are the one tool-specific part of benchbook.** Everything else here is plain
> markdown any agentic tool can read. Where skills live and how you invoke them varies:
> `.claude/skills/<name>/SKILL.md` invoked as `/<name>` in Claude Code, prompt files or
> `AGENTS.md` procedures in Codex-style tools, `.cursor/rules/` in Cursor. **The procedures
> themselves port unchanged** — each is an ordered list of steps in plain language. Only the
> packaging differs.
>
> The commands written as `/name` below are Claude Code syntax. Substitute your own tool's
> invocation, or simply describe what you want — the contract alone is enough to run every
> operation without a single skill installed.

---

## The core six

These cover the everyday loop and are what this repo ships:

| Skill | What it does |
|---|---|
| `wiki-ingest` | The full ingest workflow — detect input type, fetch or transcribe, propose a domain, read the domain rules, discuss takeaways, dispatch, then update index, overview and log |
| `wiki-project-start` | Create a project page with all required sections, update the index, log it |
| `wiki-project-open` | Load an existing project and orient you — status, recent log entries, open questions — so you can decide what to do next |
| `wiki-project-review` | Stress-test a project's plan through a one-question-at-a-time interview *before* anything changes |
| `wiki-lint` | Full maintenance pass — validate, report, sync the todo list |
| `wiki-session-close` | Verify what changed, log new pages, commit, push |

Two of those deserve comment.

**`wiki-project-review` is adversarial on purpose.** It doesn't help you write the plan; it
attacks it, one question at a time, before any work starts. Pairs directly with the plan
approval gate in [09 — Projects](09-projects.md) — the gate creates a moment where the plan
exists and nothing has been built, and this is the skill that uses that moment.

**`wiki-session-close` exists because the last five minutes are where discipline dies.** The
work is done, the interesting part is over, and committing feels like paperwork. Making it a
named skill turns "I should commit this" into a single command, which is the difference
between a repo that's current and one that isn't.

---

## Two pattern examples

These ship with their domain packs (`domains/knowledge/skills/`, `domains/home/skills/`) as
demonstrations of what skills can do beyond the core loop. Both are genericized from live
versions. Two further domain skills ship with the inert packs: `book-capture` (books) and
`recipe-capture` (cooking).

### `research`

Multi-source research on a topic — pulls recent discussion from several places, synthesises
it, presents takeaways, then asks whether to ingest the result as a wiki source page.

**The pattern:** *acquire → synthesise → offer to file.* That last step is the interesting
one. Research that stays in the chat window is research you'll redo. The skill makes filing
the default path rather than an afterthought.

Its external data sources are pluggable; treat them as an example rather than a requirement.

### `deploy-runbook`

Scaffolds an install runbook for a new self-hosted service — prerequisites, stack setup,
admin account, service-specific phases, and a pre-filled block of the integration steps that
every service in your fleet needs.

**The pattern:** *scaffold-from-repeated-structure.* After you deploy the third service, you
notice every runbook has the same seven boring steps — reverse proxy entry, DNS record,
backup job, monitoring check, release tracking, dashboard tile, documentation pages — and
that skipping any one of them is invisible until something breaks at 3am.

The skill's actual value isn't saving typing. It's that **the boring steps stop being
optional**, because they arrive pre-written and unticked. A checklist you have to remember to
write is a checklist you'll eventually skip.

The shipped version is genericized. Replace the integration steps with your own fleet's.

---

## When to write a skill

The trigger is repetition, not complexity:

> **When you've performed the same multi-step sequence for the third time, write a skill.**

Third time, not first. The first time you don't know which parts are essential. The second
you're guessing. By the third you know what the steps actually are and which ones you skipped
without consequence.

Signals that something should be a skill:

- You keep re-explaining the same procedure to the agent
- The sequence has a step that's easy to skip and expensive to skip
- It spans enough steps that you'd forget one doing it by hand
- The output should be consistent across runs — a template, a scaffold, a report

Signals it shouldn't:

- It's a single action
- You've done it twice and it went differently both times
- It encodes a decision you should still be making consciously

That last one matters. A skill automates procedure, not judgement. When a skill starts making
calls you'd want to think about, it's grown past its remit — split the judgement back out into
a question it asks you.

---

## Skills vs the contract

Easy to conflate, cleanly separated in practice:

| | Contract | Skills |
|---|---|---|
| **Answers** | What the wiki *is* | How a job gets *done* |
| **Loaded** | Every session | Only when invoked |
| **Changes** | Rarely, by negotiation | Freely |
| **If wrong** | The wiki's structure is wrong | One workflow is clumsy |

Rules of thumb: anything the agent must know regardless of task belongs in the contract.
Anything only relevant while performing a specific job belongs in a skill. When a skill starts
restating conventions, those conventions belong in the contract — and the skill should point
at them instead.

---

**Next:** [11 — Keeping It Honest](11-keeping-it-honest.md).
