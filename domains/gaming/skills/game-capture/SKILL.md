---
name: game-capture
description: "Capture a game into the wiki — a recommendation, a purchase, or one you just started. Use when the user says 'add this game', 'someone recommended [game]', 'I bought [game]', 'add [game] to my backlog', 'do I own [game]', 'have I played [game]', or pastes a store link. Checks ownership across every status first — bundles and sales mean you own more than you think — then files the game page with the required fields for its status."
license: MIT
metadata:
  version: 1.0.0
  category: gaming
---

# Game Capture

## Purpose

File a game — **or** tell the user it's already sitting unplayed in their backlog.

The ownership check is not a formality. Bundles, sales and subscription services mean the most
common outcome of "should I buy this?" is discovering you bought it in 2023.

---

## Step 1 — Identify the game precisely

Title **and** platform. Titles collide constantly across remakes, remasters and reboots — a
2024 remake and a 2002 original are different games with different verdicts.

If it came from a recommendation, note what was actually said. That quote goes on the page
verbatim; a paraphrase loses the reason it appealed.

---

## Step 2 — Ownership collision check, across every status

```bash
grep -ril "<title>" wiki/gaming/games/
```

Check **all** statuses, not just the played ones. `backlog` is where forgotten purchases live,
and it's the single most useful hit this skill produces.

| Found as | Report |
|---|---|
| `backlog` | **You already own this, unplayed.** Give the storefront and when it was added. Stop |
| `dropped` | **You already stopped playing this** — give the reason and the hour count. Stop |
| `shelved` | Paused, might return. Give the reason |
| `completed` / `ongoing` | Already played — give rating and playtime |
| `wishlist` | Already wanted, since when |
| not found | Proceed |

**A collision is a successful outcome.** Report it and stop — don't file a duplicate. Someone
enthusiastically recommending a game you dropped at four hours is exactly the moment this
domain earns its keep.

---

## Step 3 — Confirm the status

Ask; don't infer from context.

| Status | Meaning |
|---|---|
| `playing` | In rotation now |
| `backlog` | **Owned**, not started |
| `wishlist` | Not owned, want it |
| `completed` / `ongoing` / `shelved` / `dropped` | See the domain rules |

"I got it in a bundle" is `backlog`, not `wishlist`. The difference is whether money has
already been spent, and it changes what the page is for.

---

## Step 4 — Required fields for the status

**Always:** `platform:`, and `storefront:` for anything owned.

**`wishlist` → `time_to_beat` is required.** A game's price is advertised; its real cost is
not. Get an estimate — from a how-long-to-beat source, or the user's own guess clearly marked
as such. Don't file a wishlist entry without one; a decision missing its main cost isn't a
decision.

**`dropped` or `shelved` → reason **and** `playtime_hours` are required.** If the user is
capturing a drop, use `/game-drop` instead — it asks better questions.

---

## Step 5 — Write the page

`wiki/gaming/games/<game-slug>.md`, `type: game`.

| Section | Content |
|---|---|
| `## Summary` | What it is and what kind of game — 2–4 sentences |
| `## Why It's Here` | The recommendation quoted verbatim, or why you bought it |
| `## Verdict` | Only once played. Rating, and what actually made it good or not |
| `## Notes` | Build, settings, mods, where you got stuck — whatever future-you needs |

**Never invent a plot or a review.** If you can't fetch a real description, stub it and say so.
A fabricated summary is indistinguishable from a real one later and will inform a purchase.

---

## Step 6 — Franchise and studio checks

**Franchise:** if 2+ games in this franchise are now in the library *and* the entry point isn't
`dropped`, create or update `wiki/gaming/franchises/<slug>.md`. Include **where a newcomer
should start** — rarely release order, and the most useful thing on that page.

**Studio:** at the *third* game from one studio with no studio entity, propose one. Below three
you have an impression, not a pattern.

---

## Step 7 — Platform link

Link the game to its platform's entity page in `wiki/home/entities/`. If the user owns that
hardware and the page doesn't exist, propose it — the console is a `home` entity, not a gaming
one.

---

## Step 8 — Post-flight

Update `wiki/index-gaming.md`. Append to `log.md` **only** if a genuinely new game, franchise
or studio page was created.

---

## Reporting

State plainly: collision or new; the status filed; which required fields were captured; and
whether the description was fetched or stubbed.
