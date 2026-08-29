---
name: game-drop
description: "Capture why you stopped playing a game, while you still remember. Use when the user says 'I dropped [game]', \"I'm done with [game]\", 'stopped playing [game]', 'shelving [game]', 'bounced off [game]', or otherwise signals they've stopped. Distinguishes dropped from shelved, captures the hour count and the specific reason, and records whether anything would bring them back."
license: MIT
metadata:
  version: 1.0.0
  category: gaming
---

# Game Drop

## Purpose

Capture the moment you stop.

Most systems record acquisition — you bought it, you added it, you started it. Almost nothing
records *quitting*, because quitting doesn't feel like an event. It feels like the absence of
one.

But the drop is where the information is. Six months from now the sequel is on sale, someone
tells you the series is brilliant, and you have no idea whether you disliked it or just
drifted away. **One line written today answers that permanently.**

---

## Step 1 — Find the page

```bash
grep -ril "<title>" wiki/gaming/games/
```

If there's no page, create one — a game you played long enough to quit deserves a page
regardless of how briefly. Especially if briefly: a twenty-minute bounce is the cheapest
possible record of a decision you'd otherwise repeat.

---

## Step 2 — Dropped or shelved?

**Ask. Don't assume.** These are genuinely different and the distinction is the whole point:

| | Meaning | Test |
|---|---|---|
| `dropped` | A verdict. Not going back | *"Would you start it again from scratch?"* — no |
| `shelved` | A pause. Genuinely might return | *"Is there a version of you that picks this up again?"* — yes |

If the user hedges, ask the test question directly. "Maybe someday" is `shelved`; "I'm done"
is `dropped`. Collapsing them loses the only signal that stops a re-purchase.

---

## Step 3 — Get the hour count

`playtime_hours` is **required**. Approximate is fine; unknown is not.

The number calibrates everything else. *"Dropped at 40 minutes"* and *"dropped at 30 hours"*
are completely different judgements on the same game — the first says it never landed, the
second says it ran out of road. A reason without an hour count can't be read correctly later.

---

## Step 4 — Get the *specific* reason

This is the step that matters, and the one where a vague answer wastes the whole exercise.

**"It got boring" is not a reason.** Push once, concretely:

- *What specifically stopped being fun?*
- *Was it the core loop, the story, the difficulty, the grind, the controls, the performance?*
- *Was there a particular moment you noticed you didn't want to open it again?*
- *Would a different platform, difficulty or patch have changed it?*

Aim for something like: *"The crafting loop turns out to be the whole game — combat is a thin
layer over inventory management, and I don't enjoy inventory management."*

That sentence is worth more than any review, because it's about **you**, and it generalises:
next time a game is praised for its crafting, you already know.

**Don't be nit-picky.** If the honest answer really is "I drifted away, nothing was wrong",
record exactly that — it's true and it's useful. Just make sure it's the actual answer and not
the first thing said to end the question.

---

## Step 5 — What would bring you back?

Only for `shelved`. One line:

- A patch or expansion?
- Finishing something else first?
- Different hardware?
- A mood?

If the honest answer is "nothing specific", that's a `dropped`, not a `shelved` — go back to
Step 2.

---

## Step 6 — Rate it, if you can

Optional but valuable. A rating on a dropped game is legitimate and informative — a 4/5 you
stopped playing at 30 hours is a real and interesting verdict, not a contradiction.

Same convention as elsewhere: 1–5, one decimal allowed, and **playtime is evidence while
rating is opinion** — record both, never derive one from the other.

---

## Step 7 — Write it

Update the game page:

```yaml
status: dropped        # or shelved
playtime_hours: 4
rating: 2.5            # optional
```

Body, under `## Verdict`:

```markdown
**Dropped 2026-08-29 at ~4h.** The crafting loop turns out to be the whole
game — combat is a thin layer over inventory management. Nothing here is
badly made; it's just not a game for me.

*Would return if:* nothing specific.
```

Date it. An undated verdict can't be weighed against a patch that shipped afterwards.

---

## Step 8 — Post-flight

Update `wiki/index-gaming.md` if the status changed the grouping.

**No `log.md` entry** unless the page was newly created — a status change on an existing page
is page-local, and belongs on the page.

---

## Why this skill exists at all

Because nobody does this by hand. Quitting a game is a non-event; there's no prompt, no
receipt, no achievement. The record only exists if something asks for it at the moment the
information is still in your head.

That's the whole system in miniature: **the agent does the bookkeeping you'd never do, at the
one moment it's cheap.**
