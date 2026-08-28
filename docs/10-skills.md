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

"Core" means **domain-independent** — these six are used in every wiki regardless of what it's
about. Everything else belongs to a domain and ships with its pack.

### Where they fire

The loop from [A Day in the Life](day-in-the-life.md), with the skills placed on it:

```
CAPTURE          DECIDE                    EXECUTE            CLOSE
   │                │                         │                 │
wiki-ingest    wiki-project-start      wiki-project-open   wiki-session-close
               wiki-project-review                          (every session)
                                                           wiki-lint
                                                           (every few weeks)
```

Two fire constantly (`wiki-ingest`, `wiki-session-close`). Three fire around projects. One is
periodic maintenance.

---

### `wiki-ingest`

**When:** something arrived and should be in the wiki — a URL, a video, a PDF, a photo, or a
decision you just made out loud in chat.

**Why it's a skill:** it's the operation you run most often, which makes it the one where drift
is most expensive. The flow has seven steps and three of them are *gates* that get skipped
when you're moving fast:

- **Domain confirmation** before any page is written. Nearly every misfiled page traces back to
  a wrong call here, and a wrong domain is expensive to fix later because links and indexes
  have already formed around it.
- **Discussing takeaways before writing.** The cheapest moment to correct a misreading is
  while nothing is on disk.
- **The re-ingest guard.** Without it you silently create a second source page for a URL you
  already ingested, and now two pages disagree about the same material.

You *can* do all this by describing it each time. It works, and it varies slightly every time —
and that variance is exactly what makes a wiki inconsistent after six months.

→ [`.claude/skills/wiki-ingest/`](../.claude/skills/wiki-ingest/SKILL.md)

---

### `wiki-project-start`

**When:** you're about to build something. *Before* you build any of it.

**Why it's a skill:** two reasons, and the second is the real one.

First, the six-section template. Write a project page freehand and you'll produce a summary
and a plan and skip the options table — which is the highest-value section in the entire
system, because it's where "why not the obvious alternative?" gets answered while you still
know the answer.

Second: **this skill's most important behaviour is refusing to build anything.** With an
agentic tool, "let's start a project" otherwise produces eleven files in forty seconds. They're
plausible. Some are good. But the architectural decisions were made at speed on your behalf,
they're now load-bearing, and you're reviewing them backwards. The skill writes a *gated plan
stub* and stops.

→ [`.claude/skills/wiki-project-start/`](../.claude/skills/wiki-project-start/SKILL.md)

---

### `wiki-project-open`

**When:** resuming anything after more than a day away.

**Why it's a skill:** the honest answer is you could read the page instead — and you won't. You
will ask "where were we?", get a reasonable-sounding summary, and start work.

The failure that causes is silent and specific: **you resume a project whose plan was never
approved**, or one that was deliberately paused for a reason nobody restated. The skill forces
a fixed brief — status, last activity, open questions, current phase — and surfaces the gated
or on-hold state *loudly*, because that state is precisely what should change what you do next.

A fixed shape also means the same four facts appear every time, rather than whichever ones the
agent found interesting today.

→ [`.claude/skills/wiki-project-open/`](../.claude/skills/wiki-project-open/SKILL.md)

---

### `wiki-project-review`

**When:** in the window between the plan existing and you approving it. That window only exists
because of the plan gate — which is the point.

**Why it's a skill:** the gate creates a moment where the plan is written and nothing has been
built. Without something to *do* in that moment, the gate degrades into "please read the plan
carefully," which is exactly what everyone already fails to do.

This skill is adversarial on purpose. It doesn't help you write the plan; it attacks it —
hunting unstated assumptions, unjustified selections, hidden dependencies, and steps ordered so
the expensive irreversible one comes before the cheap thing that would have invalidated it.

And it asks **one question per message**, deliberately. A human handed six questions answers
the first and waves at the rest.

The best outcome is sometimes "don't build this." A project abandoned at the plan stage costs
an hour; the same project abandoned in phase four costs a month.

→ [`.claude/skills/wiki-project-review/`](../.claude/skills/wiki-project-review/SKILL.md)

---

### `wiki-lint`

**When:** every few weeks. Always before sharing anything.

**Why it's a skill:** drift is invisible by construction. Nothing interrupts you to say two
pages have started disagreeing, or that a page now describes a state of the world three later
pages have overtaken. Without a deliberate pass, you find out when you act on the wrong one.

Why not just run the script? Because the script is half of it. The mechanical checks — missing
frontmatter, broken links, wrong folder — are deterministic and should be cheap. The half that
needs reading comprehension is contradictions, staleness, and entity placement, and that's the
half that finds real problems.

The skill also handles the two opt-in archival operations, which need a human to confirm
because they move files.

→ [`.claude/skills/wiki-lint/`](../.claude/skills/wiki-lint/SKILL.md)

---

### `wiki-session-close`

**When:** the end of every session that changed anything.

**Why it's a skill:** because the last five minutes are where discipline dies. The work is
done, the interesting part is over, and committing feels like paperwork. An uncommitted session
is, for practical purposes, a session that didn't happen.

Making it one command turns "I should commit this" into something you actually do. But it also
runs a verification gate you'd never run by hand — link resolution, table arithmetic, commit
message accuracy against the real diff, and a **destructive-overwrite check** on log and
archive files, which exists because a write once clobbered history instead of appending to it.

The least glamorous of the six, and arguably the highest-value.

→ [`.claude/skills/wiki-session-close/`](../.claude/skills/wiki-session-close/SKILL.md)

---

### Do you actually need all six?

No, and it's worth being honest about the ordering:

| | |
|---|---|
| **Install first** | `wiki-ingest` and `wiki-session-close`. You'd miss both within a week |
| **Only if you use projects** | `wiki-project-start`, `-open`, `-review`. If you're building a research or reading wiki, skip them |
| **Add when the wiki gets big enough to drift** | `wiki-lint`. On a fifty-page wiki you can see problems yourself |

And you can run the whole system with **zero** skills installed. The contract alone defines
INGEST, QUERY and LINT — you just describe what you want instead of typing a command. Skills
buy consistency and stop you skipping the gates; they aren't a dependency.

---

## Two pattern examples

These ship with their domain packs (`domains/knowledge/skills/`, `domains/home/skills/`) as
demonstrations of what skills can do beyond the core loop. Both are genericized from live
versions. Two further domain skills ship with the inert packs: `book-capture` (books) and
`recipe-capture` (cooking).

### `research` — knowledge pack

**When:** you need to know something before deciding — which tool to use, whether a thing is
still maintained, what people who've actually run it say.

**Why it's a skill:** for the third step. Research that stays in the chat window is research
you'll redo in four months, pay for again, and possibly reach a different conclusion from for
no good reason. The skill makes *filing* the default path rather than an afterthought, and
forces two things you'd otherwise skip: varying the search angle rather than repeating one
query, and separating what's documented from what people report from what you're inferring.

**The pattern:** *acquire → synthesise → offer to file.*

Its external data sources are pluggable — treat them as an example rather than a requirement.

→ [`domains/knowledge/skills/research/`](../domains/knowledge/skills/research/SKILL.md)

### `deploy-runbook` — home pack

**When:** you're about to stand up a new self-hosted service.

**Why it's a skill:** after the third service you notice every runbook ends with the same seven
boring steps — reverse proxy, DNS, backup, monitoring, release tracking, dashboard, docs — and
that skipping any one is invisible until something breaks at 3am.

The value isn't saved typing. It's that **the boring steps stop being optional**, because they
arrive pre-written and unticked. A checklist you have to remember to write is one you'll
eventually skip. An unticked box is a decision you can defer; an absent box is one you'll never
know you missed.

**The pattern:** *scaffold-from-repeated-structure.*

The shipped version is genericized — replace the seven steps with your own fleet's, once, then
stop editing them. Their value comes from being identical across every service.

→ [`domains/home/skills/deploy-runbook/`](../domains/home/skills/deploy-runbook/SKILL.md)

### And two more, in the inert packs

`book-capture` (books) and `recipe-capture` (cooking) ship with packs that aren't installed by
default. Both are worth a skim even if you don't want the domain — `book-capture` shows a
collision check that runs *before* anything is filed, and `recipe-capture` shows a skill that
produces two co-dependent files and validates one of them against an external tool.

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
