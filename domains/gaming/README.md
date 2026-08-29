# Pack: gaming

Computer and console games — what you've played, what you're playing, what you own and haven't
touched, and what you deliberately stopped playing.

## What it adds

| | |
|---|---|
| **Rules** | `agents-domain-gaming.md` — status vocabulary, franchise threshold, the stop-reason and time-estimate rules |
| **Skills** | `game-capture` (file a game, ownership-collision-checked) and `game-drop` (capture *why* you stopped, while you still remember) |
| **Folders** | `wiki/gaming/games/`, `wiki/gaming/franchises/`, `wiki/gaming/entities/`, `wiki/gaming/references/` |
| **Index** | `wiki/index-gaming.md` |
| **Schema** | **Yes — adds `game` and `franchise` page types** |
| **Subdomains** | None — platform is a field, not a folder |

## Install

1. Add a dispatch row in `agents-core.md` § 3 pointing at
   `domains/gaming/agents-domain-gaming.md`
2. Add `gaming` to the domain list in `agents-core.md` § 4
3. Add `game` and `franchise` to the `type:` enum in `agents-page-conventions.md`
4. `mkdir -p wiki/gaming/{games,franchises,entities,references}`
5. Create `wiki/index-gaming.md`
6. Copy `skills/game-capture/` and `skills/game-drop/` into your tool's skills location

Or ask your agent: *"install the gaming domain pack."*

## The hardware isn't in this domain

Your PS5, Steam Deck and gaming PC are things you **own and operate** → `home/entities/`. This
pack covers the software and the playing of it. Game pages link to platform pages; they're
different kinds of thing, and the Entity Placement Rule already says which goes where.

## Why it isn't a reskin of the books pack

The obvious move is to copy books — author→studio, series→franchise, candidate→wishlist. Three
places this pack deliberately doesn't:

**Games get a page each; books don't.** Books has *no* page per read book, because 350 books ×
one page each is bloat carrying nothing a table row wouldn't. Games are fewer and have more to
say — playtime, platform, why you stopped, what build you ran. The asymmetry is the point:
copy the *reasoning*, not the structure.

**No candidate type.** Books needs one because a read book has no page to promote into. A game
always has a page, so wanting it is `status: wishlist` and owning it unplayed is
`status: backlog`. **Don't add a type where a field will do.**

**Studio pages are earned at the third game**, not created automatically — the same trigger
shape as the knowledge pack's channel entity. Below three you have an impression, not a
pattern.

## Three rules worth stealing even if you don't game

**A wishlist entry requires a time estimate.** A game's price is advertised; its real cost is
not. Wishlisting a 90-hour RPG and a 5-hour indie are different decisions, and the storefront
shows you only the number that's the same. Recording `time_to_beat` up front is what makes
*"I have four hours this weekend"* a question the wiki can answer.

**Stopping requires a reason and an hour count.** `dropped` and `shelved` are different — one
is a verdict, one is a pause — and both demand the reason plus `playtime_hours`. *"Dropped at
4h, the crafting loop is the whole game and I don't like crafting"* is worth more than any
review, because it's about you. The hour count calibrates it: dropped at 40 minutes and
dropped at 30 hours are entirely different judgements.

**Playtime is evidence; rating is opinion.** Record both, never derive one from the other. A
4/5 with 6 hours and a 4/5 with 200 hours are different claims.

## About `game-drop`

Most systems capture things when you acquire them. This one captures the moment you *stop* —
which is the higher-value moment and the one nobody ever writes up, because quitting a game
doesn't feel like an event worth recording.

It is. Six months later, when the sequel is on sale and someone tells you the series is
brilliant, the page tells you in one line why you already know otherwise.
