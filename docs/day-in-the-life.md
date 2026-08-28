# A Day in the Life

Three worked examples, start to finish. The reference docs explain the machinery; this one
shows it running.

Each follows the same four-beat loop, which is worth naming because it's the same every time:

| Beat | What happens | Typical skills |
|---|---|---|
| **Capture** | Something arrives — a video, a question, an idea | `wiki-ingest`, `research` |
| **Decide** | Options compared, one chosen, the losers recorded | `wiki-project-start`, `wiki-project-review` |
| **Execute** | You build. Progress and surprises get logged as you go | `deploy-runbook`, project `## Log` |
| **Close** | The build record freezes; a living page takes over | `wiki-session-close` |

The thing to watch for in all three: **the human makes every judgement call, and the agent
does every piece of bookkeeping.** That division is the entire system.

> **On the `/commands` below.** They're Claude Code syntax, because that's what this was built
> on. benchbook isn't tied to it — any agentic tool that reads and writes files in a repo will
> do. Substitute your tool's invocation, or just describe what you want in plain language; the
> contract is what drives the behaviour, not the command name.

---

## Example 1 — You saw an ESP32 project on YouTube and want to build it

### Capture

**1. Paste the URL.**

```
/wiki-ingest https://youtube.com/watch?v=...
```

The agent detects a video, pulls the transcript, and reads it.

**2. It proposes a domain, and waits.**

This is the highest-leverage moment in the whole workflow, and here it's genuinely ambiguous.
The *video* is reference material about a technique — that's `knowledge`. The *thing you want
to build* is a `projects` page. Those are two different pages, and conflating them is the most
common beginner mistake.

You confirm: the source goes to `knowledge`. The build comes later.

**3. It discusses the takeaways before writing anything.**

Which board, which peripherals, what the power requirements are, and — most valuably — the
gotchas the creator hit. You correct anything it misread. Nothing is on disk yet.

**4. It proposes pages.**

- A **source page** with the full transcript embedded, so the build survives the video being
  deleted
- **Entity pages** for the components: the board, the display, the sensor

You approve two and reject one, because the sensor is a detail, not a thing you'll ever look
up on its own.

The agent notices you already have an entity page for that board family — you own one — and
updates it rather than creating a duplicate, noting the new source in its `sources:` field.

### Decide

**5. Start the project.**

```
/wiki-project-start
```

You get a page with all required sections. `## Hard- and Software` gets an options table:
which board variant, which display, what each costs, what each rules out. `## Plan / Phases`
is a **stub** marked *"Deferred — awaiting manual plan approval."*

**6. Nothing gets built yet.**

This is the plan approval gate, and it's the rule most worth stealing. Without it you describe
the idea and forty seconds later there are eleven files — plausible, some of them good, and
none of the architectural decisions were yours.

Optionally, attack your own plan first:

```
/wiki-project-review
```

which interviews you one question at a time about what you haven't thought through.

**7. You approve.** Status goes `planned → active`, and the plan gets written out in full.

### Execute

**8. You build.** Each session appends to the project's `## Log` — what you did, what worked.

**9. Something breaks.** The display library needs a specific version; the newer one silently
renders nothing. That goes in the log **with the version number and the symptom**, because
that exact detail is what you will need and will not remember.

**10. Firmware source goes to `scripts/<project-slug>/`**, with a README linking back to the
project page, and the project page linking forward to the files. Two-way, always.

### Close

**11. The build produces a running thing**, so the final phase is: create an operational entity
page with `change_history: true`.

The record forks. The **project page** freezes and moves to `completed/` — how this came to
exist, what was rejected, what went wrong. The **entity page** becomes the living document —
what firmware version is on it right now, what the pinned library versions are, what changed
last month.

### What this bought you

Eight months later the display goes blank. You open the entity page's `## Current State`,
see the pinned library version and a one-line change-history entry explaining why it's
pinned, and you're done in ninety seconds instead of an evening.

And when you consider adding a second sensor, the project page's options table already tells
you which sensor you rejected and why.

---

## Example 2 — A Telegram bot, and you don't know which repo to use yet

This one starts earlier: you don't have a candidate, you have a want.

### Capture — the research phase

**1. Ask the question properly.**

```
/research self-hosted telegram bot frameworks
```

The skill pulls recent discussion from several sources, synthesises it, and presents
takeaways — which projects people actually run, which are maintained, which are abandoned but
still top of the search results.

**2. It offers to file the research.** Say yes.

This step feels skippable and isn't. In three months you will not remember why you rejected
the most popular option, and without the page you will re-research it from scratch — and
possibly reach a different conclusion for no good reason.

**3. Four candidates get compared, which crosses a threshold.**

The rule: **1–3 things compared → entity pages cross-linked with `## Compared To`. 4+ ranked
or compared → a reference page may be justified, and it needs your approval.**

You approve. You now have four entity pages plus one comparison page, and each entity carries
`repo_url:` in frontmatter — which quietly enables release tracking later.

The comparison records real, checkable things: last commit date, language, whether it supports
the one feature you actually need, deployment story, and which one won.

### Decide

**4. Start the project.** The `## Hard- and Software` table imports the comparison, then a
"Selected" subsection states the choice **and the reason**.

**5. Plan gate.** Same as before — stub, review, approve.

### Execute — deployment

**6. Scaffold the deployment.**

```
/deploy-runbook
```

This generates the install runbook with the boring integration steps **pre-filled and
unticked**: reverse proxy entry, DNS record, backup job, monitoring check, release tracking,
dashboard tile, documentation pages.

The value isn't saved typing. It's that those seven steps stop being optional. Every one of
them is invisible when skipped and expensive at 3am.

**7. The bot token does not go in the wiki.** Ever. Only an environment variable or a vault
reference. The comprehensiveness instinct — "let me paste the working config so the page is
complete" — is exactly what leaks credentials, and it's why the rule is absolute rather than
a judgement call.

**8. The code lives in the infrastructure repo as a live checkout**, not as a copy. A hotfix
applied at 11pm is a real commit, not a divergence waiting to be discovered.

**9. Because status is `deployed`**, the project page requires three extra sections:
`## Version Control`, `## Backup Concept`, `## Cron Jobs`. These exist because they are
precisely what you fail to record and desperately need eighteen months later.

### Close

**10. Operational entity page** with `## Current State` — version, host, backup target,
monitoring check — and an append-only `## Change History`. Project page moves to `completed/`.

### What this bought you

The framework ships a new major version. Release tracking flags it, because `repo_url` was set
back in step 3. You upgrade, append one line to the change history, done.

And when a friend asks "what should I use for a Telegram bot?", you have a comparison page
with dates on it rather than a vague memory.

---

## Example 3 — Learning to fly FPV drones

Not software, not a build. Skill acquisition plus a shopping decision — which is a different
shape, and the system handles it without special-casing.

### Capture

**1. Research the path, not the product.**

```
/research fpv drone getting started progression
```

What comes back is a *sequence*: simulator hours first, then a small indoor quad, then
outdoor. Plus the consensus that almost everyone buys the wrong thing first.

**2. The domain call is genuinely non-obvious.** Is this `gaming`? A new domain? Something
under `knowledge`?

The agent proposes, you decide. This is a good example of why the domain checkpoint is a
human decision — the right answer depends on how *you* think about it, and there's no way for
the agent to know that from the material.

### Decide — two tracks

**3. The learning path is a project.**

`## Use Cases` = what you actually want to be able to do. `## Plan / Phases` = the
progression, with **gates between phases**: don't buy the outdoor quad until you've flown N
hours in the simulator. Writing the gate down is what stops you skipping it.

**4. The gear is a shopping problem**, and it has a cold-start question: what is a fair price?

```
/market-baseline fpv goggles
```

This surveys current listings and new prices, computes a distribution, and drafts a
recommended buy price plus search criteria.

**5. Every candidate becomes an entity page with `status: considered`.**

Goggles, radio, quad, batteries, charger. Four goggle options compared crosses the threshold
again — comparison page, with your approval.

**6. The rejections get recorded, and this is the point.**

"Considered the higher-end goggles, didn't buy — the price difference bought two more batteries
and the feature gap doesn't matter below N hours."

Six months later someone enthusiastically recommends exactly those goggles. You already know
your own reasoning, dated, instead of re-deciding from scratch while someone is talking at you.

Research kept after a firm "not buying it" gets tagged `standalone-reference`, so the lint pass
stops flagging it as an orphan — it's terminal by decision, not by neglect. The tag requires
the page to *say* that in its own body, so the exemption can't become a rubber stamp.

### Execute

**7. Purchases flip `considered → owned`.** The entity page becomes the living record:
firmware versions, what you've broken, which spare parts fit.

**8. Progress logs to the project.** Simulator hours. First flight. First crash.

**9. The crash produces the most valuable page.** What broke, the part number, what it cost,
and what you'd do differently. That's an entity change-history entry, and it's the thing you
would absolutely not have written down without an agent doing it for you.

### Close

**10. When you can fly**, the project completes and moves to `completed/`. The gear entities
stay live, accumulating maintenance history for as long as you own them.

### What this bought you

A year in, you're deciding whether to upgrade. The wiki holds: what you bought, what you paid,
what you rejected and why, everything you've broken and what the repairs cost, and how long
each phase actually took versus what you planned.

That's a genuinely informed decision instead of a vibe.

---

## What the three have in common

Different subjects, identical structure:

1. **Capture before deciding.** The research or the source gets filed *before* the project
   exists. It's what the decision was based on, and it's worthless once reconstructed from
   memory.
2. **The plan is a reviewable artifact.** Separate from execution, gated on your approval.
3. **The rejected options are recorded as carefully as the chosen one.** This is the single
   highest-value habit here, and the one nobody sustains without help.
4. **When it's done, the record forks.** A frozen build history, and a living page for current
   state.
5. **Surprises get written down at the moment they surprise you** — with the version number,
   the part number, the error message.

None of it is clever. It's just bookkeeping that reliably happens, which is the one thing that
was never true before.

---

**Next:** [02 — The Contract](02-the-contract.md) for how the rules that enforce all this
actually work, or [11 — Keeping It Honest](11-keeping-it-honest.md) for what happens when they
don't.
