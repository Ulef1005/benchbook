---
name: wiki-project-review
description: "Stress-test an existing project's plan through a one-question-at-a-time interview before anything gets built. Use when the user says 'review this project', 'stress-test [project]', 'interview me about [project]', \"let's think through [project]\", 'poke holes in this plan', or wants to challenge a plan rather than just orient to it (that's wiki-project-open). Pairs with the plan approval gate — this is the skill that uses the moment where the plan exists and nothing has been built."
license: MIT
metadata:
  version: 1.0.0
  category: wiki
---

# Wiki Project Review

## Purpose

Attack a plan while changing it is still free.

This is the counterpart to the plan approval gate in
`domains/projects/agents-domain-projects.md`. The gate creates a moment where the plan exists
and no code does. **This skill is what makes that moment useful** — without it, the gate is
just "please read the plan carefully," which is exactly what everyone already fails to do.

Your job here is **not** to help write the plan. It's to find what's wrong with it.

---

## Step 1 — Read everything first

Read the project page in full, plus every entity page it links under
`## Hard- and Software`. Do not start asking questions until you've read the lot — half the
weaknesses are visible on the page and asking about them wastes the user's attention.

---

## Step 2 — Find the real weak points

Before asking anything, privately identify the 3–6 places this plan is most likely to fail.
Look for:

| Weakness | What it looks like |
|---|---|
| **Unstated assumption** | A phase that only works if something unverified is true |
| **Unjustified selection** | `## Hard- and Software` picks an option with no recorded reason, or with no alternatives listed at all |
| **Hidden dependency** | Phase 3 needs something no phase produces |
| **Undefined done** | No phase says how you'd know it worked |
| **Ordering risk** | The expensive, irreversible step comes before the cheap thing that would invalidate it |
| **Unpriced cost** | Money, time or ongoing maintenance nobody has estimated |
| **Silent scope** | The plan quietly grew past what `## Summary` claims |
| **Missing exit** | No stated condition under which you'd stop |

Rank them. Lead with the one most likely to sink the project.

---

## Step 3 — Interview, one question at a time

**One question per message. Always.** A numbered list of six questions gets one answer to the
first and a vague gesture at the rest.

For each:

1. Ask the question plainly
2. Say **why it matters** in one line — what breaks if the answer is bad
3. Offer 2–3 concrete options where they exist, with a recommendation
4. State how many questions remain

Push back on weak answers. A reflexive "yeah that'll be fine" on a load-bearing assumption is
the exact thing this skill exists to catch. Ask once more, concretely: *"what specifically
makes you confident about that?"*

Don't be nit-picky. If a concern is genuinely minor, note it and move on — burning the user's
patience on trivia means the important question lands on someone who's stopped reading.

---

## Step 4 — Record the outcome on the page

The interview is worthless if it evaporates into chat.

- **Answers that resolve something** → add to `## Open Questions` as `[x]` with the decision,
  or into the `## Hard- and Software` "Selected" reasoning
- **New problems found** → add as `[ ]` open questions
- **Plan changes agreed** → edit `## Plan / Phases`
- **Always** → append a `## Log` entry: what was reviewed, what changed, what's still open

Write the *reasoning*, not just the conclusion. "Chose B" is worth little in eight months;
"chose B because A needs a static IP we don't have" is worth an afternoon.

---

## Step 5 — Give a verdict

State plainly which of these applies:

- **Ready to approve** — remaining questions don't block starting
- **Not ready** — name the specific unresolved thing that blocks it
- **Should be reconsidered** — the review surfaced something that undermines the goal itself

That third outcome is a success, not a failure. A project abandoned at the plan stage costs an
hour. The same project abandoned in phase four costs a month — and the page will record why,
so it doesn't get re-proposed next year.
