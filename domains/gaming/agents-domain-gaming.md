# benchbook — Domain Rules: Gaming

> Loaded during INGEST for the gaming domain. Read alongside `agents-core.md`.

---

## What belongs here

Computer and console games — what you've played, what you're playing, what you own and
haven't touched, and what you deliberately stopped playing.

**Default subdomain:** none. Platform is a *field*, not a folder — a game exists on several
platforms and you may own it on more than one.

**The hardware is not in this domain.** Your PS5, your Steam Deck, your gaming PC are things
you *own and operate* → `home/entities/`. This domain is the software and the playing of it.
The game links to the platform entity; they're different kinds of thing.

---

## Page types

### Game page — `wiki/gaming/games/<game-slug>.md`

`type: game`. **One page per game**, for every game in any state — played, playing, owned
unplayed, dropped, or wanted.

> **Deliberate divergence from the books pack.** Books deliberately has *no* page per read
> book — 350 books × one page each is bloat carrying nothing a table row wouldn't. Games are
> different: there are fewer of them and there's more to say about each. Playtime, platform,
> why you stopped, what build you ran, whether it's worth returning to — none of that fits a
> row. So games get pages and books don't, and that asymmetry is intentional.

### Franchise page — `wiki/gaming/franchises/<franchise-slug>.md`

`type: franchise`. Create when **2+ games in the franchise are in your library** *and* your
entry point isn't `dropped`.

If you bounced off the first one, a page listing six sequels is noise — the same reasoning as
the books pack's series threshold, which was refined after measuring showed the naive version
generated two-thirds waste.

Holds release order, which entries you've played, and — the useful part — **where a newcomer
should actually start**, which is rarely release order.

### No separate candidate or wishlist type

A game you want is a game page with `status: wishlist`. A game you own but haven't started is
`status: backlog`.

The books pack needs a distinct `candidate` type because read books have no page to promote
*into*. Games always have a page, so a status change is enough. **Don't add a type where a
field will do.**

### Studio pages are earned, not automatic

Create `wiki/gaming/entities/<studio-slug>.md` only at the **third** game from one studio —
the same trigger shape as the knowledge pack's channel entity. Below three you have an
impression, not a pattern, and the page would be a stub.

---

## Status vocabulary

| Status | Meaning |
|---|---|
| `playing` | In active rotation right now |
| `completed` | Finished the thing you set out to finish |
| `ongoing` | No end state by design — live service, roguelike, sim. Still in rotation |
| `shelved` | Started, paused, genuinely might return |
| `dropped` | Stopped, not going back |
| `backlog` | **Owned**, not started |
| `wishlist` | Not owned, want it |

**`shelved` and `dropped` are different and the distinction matters.** One is a pause, one is a
verdict. Collapsing them loses the only information that stops you re-buying something in a
sale two years from now.

---

## Frontmatter

Required beyond the universal set:

```yaml
type: game
status: playing | completed | ongoing | shelved | dropped | backlog | wishlist
platform: [pc, ps5, switch, ...]        # where you own or play it
```

Optional but load-bearing:

| Field | Why |
|---|---|
| `rating` | 1–5, one decimal allowed. Same convention as books: an imported integer and a hand-given decimal are different precision claims — never back-fill a decimal to tidy a column |
| `playtime_hours` | Actual hours in |
| `time_to_beat` | Estimated hours for the main path. **Required on `wishlist`** — see below |
| `franchise` | Slug, if part of one |
| `storefront` | Where you bought it — decides whether "do I own this?" is answerable |
| `completed_date` | |

---

## The rules that earn their place

### 1. A wishlist entry needs a time estimate

**`time_to_beat` is required on `status: wishlist`.**

A game's price is advertised; its real cost is not. Wishlisting a 90-hour RPG and a 5-hour
indie are completely different decisions, and the storefront deliberately shows you only the
number that's the same.

Recording the estimate at wishlist time is what makes the backlog answerable later: *"I have
four hours this weekend"* is a question the wiki can actually answer.

### 2. Stopping requires a reason and an hour count

**`dropped` and `shelved` both require a recorded reason and `playtime_hours`.**

*"Dropped at 4h — the crafting loop turns out to be the whole game, and I don't enjoy
crafting"* is worth more than any review, because it's about you. It's also the exact thing
you will not remember, and the exact thing that stops you buying it again on sale.

The hour count matters because it calibrates the reason. Dropped at 40 minutes and dropped at
30 hours are entirely different verdicts on the same game.

### 3. Check ownership before wishlisting

Bundles, sales and subscription services mean **you already own more than you think.** Before
filing a wishlist entry, check every status — including `backlog`, which is where forgotten
purchases live.

A collision here is the most valuable result this domain produces.

### 4. Playtime is evidence; rating is opinion

Record both, and never derive one from the other. A 4/5 with 6 hours and a 4/5 with 200 hours
are different claims, and flattening them destroys the only objective signal you have.

### 5. Log the bounce, not just the campaign

Create the page even for a game you played for twenty minutes and never opened again.

That feels like overkill and isn't: it is the cheapest possible record of a decision you would
otherwise repeat. The pages you skip writing are the ones you'll wish you had.

---

## Dispatch flow

**G1. Identify the game** — title plus platform. Titles collide across remakes and remasters;
be specific about which one.

**G2. Ownership collision check** — search every status before treating anything as new:

```bash
grep -ril "<title>" wiki/gaming/games/
```

Report a collision and stop rather than filing a duplicate.

**G3. Confirm status** — from the vocabulary above. Ask; don't infer.

**G4. Create or update the game page.** For `wishlist`, `time_to_beat` is required. For
`dropped` or `shelved`, the reason and `playtime_hours` are required.

**G5. Franchise check** — 2+ in the library and the entry point isn't `dropped` → create or
update the franchise page, including where to start.

**G6. Studio check** — third game from this studio with no studio entity → propose one.

**G7. Platform link** — link the game to the platform's entity page in `home/entities/`. If
that page doesn't exist and you own the hardware, propose it.

**G8. Post-flight** — update `wiki/index-gaming.md`; append to `log.md` only if a genuinely
new game, franchise or studio page was created.

---

## Checklist

- [ ] Ownership collision check run across **all** statuses
- [ ] Status confirmed from the vocabulary, not inferred
- [ ] `platform:` set
- [ ] `wishlist` → `time_to_beat` present
- [ ] `dropped` / `shelved` → reason **and** `playtime_hours` present
- [ ] Franchise threshold checked (2+ and entry point not `dropped`)
- [ ] Studio trigger checked (3rd game from one studio)
- [ ] Platform entity linked in `home/entities/`
- [ ] `index-gaming.md` updated
