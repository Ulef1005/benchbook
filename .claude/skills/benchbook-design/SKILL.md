---
name: benchbook-design
description: The benchbook visual language — palette, type, mark, layout and copy rules. Use whenever building or changing anything visible: the wiki site, README assets, social cards, diagrams, slides.
---

# benchbook design

A field survey instrument, not a SaaS product. Restrained, monospaced, paper-and-graphite, with
exactly one hot accent. If a change makes it look friendlier, it is probably wrong.

## The mark

The Ordnance Survey benchmark symbol: a horizontal bar with an arrow pointing up into it. A fixed
reference point of known elevation — it doesn't move; you come back to it.

```svg
<svg viewBox="0 0 100 100"><rect x="18" y="24" width="64" height="11" fill="currentColor"/><polygon points="50,35 27,76 73,76" fill="currentColor"/></svg>
```

- Two shapes only. Never outline, round, rotate, or put it in a container.
- Never place text inside it; the wordmark is a separate lockup.
- Clear space ≥ 25% of its height on all sides. Minimum size 16px.
- Ships transparent — never bake in a white square.
- `assets/mark/mark-neon.svg` is the default and holds on both grounds; graphite/paper variants
  are for monochrome, print and stamp use.

## Palette — three colours, no fourth

| Token | Hex | Use |
|---|---|---|
| Graphite | `#21201C` | Text, dark grounds, monochrome/print mark |
| Paper | `#F5F1E8` | Light ground |
| Neon | `#FF3DBE` | Default mark colour; **one accent per surface** |

Derived neutrals (site only, all in `src/styles/global.css`): `--bg-sunk`, `--bg-raised`,
`--fg-muted`, `--fg-faint`, `--rule`, `--code-bg`. Need a new tone? Derive it from graphite or
paper in `oklch` — never introduce a new hue. Neon is never body text, never a gradient, never a
large fill: badges, one rule, one word, the mark.

## Type

- **IBM Plex Mono** (500) — wordmark, all headings, metadata, eyebrows, code, nav, buttons.
  Wordmark is always lowercase `benchbook`, letter-spacing `-0.01em`.
- **IBM Plex Sans** (400/600) — body copy and list items. Mono at 16px over fourteen reference
  docs reads badly; this split is a deliberate extension of the brand sheet, not a drift.
- Headings: `letter-spacing: -0.02em`, `line-height: 1.2`. Eyebrows: 11px, `0.12em` tracking,
  uppercase, `--fg-faint`.
- Reading measure `74ch`. `text-wrap: pretty` on prose, `balance` on display headings.
- Never below 12px on screen, never below 24px on a 1920-wide slide.

## Layout

- Radius `2px` on controls and chips, `3px` on cards and panels. Nothing rounder.
- 1px `--rule` borders do the separating. One shadow style only, and only on floating things:
  `0 24px 50px -30px rgba(33,32,28,0.9)`.
- Docs shell: `236px` sidebar · fluid column · `200px` TOC. Wiki shell swaps the TOC for a
  `268px` metadata/backlinks rail.
- Active nav item = 2px neon left border + raised background. That is the only "selected" pattern.
- Flex/grid with `gap` for every sibling group.
- Dark mode is a token swap on `:root[data-theme]`, applied before first paint. Both themes ship.

## Wiki pages look different from docs pages

Docs are prose. Wiki pages are records, and should read as such: type badge in neon, frontmatter
chips, a metadata rail with frontmatter / sources / linked-from, and `h2`s demoted to small
uppercase section labels. Never hide frontmatter — it is the interesting part.

## Copy

- The slogan, unchanged: **Your AI keeps the wiki. You keep the rules.**
- Plain, specific, slightly dry. Concrete nouns. No marketing adjectives, no exclamation marks,
  no emoji (the README's three are the documented exception).
- Prefer the honest negative: "No app. No database. No embeddings."
- **Never quote the private wiki's numbers** (page counts, domain counts) in public-facing
  surfaces. Claims must be verifiable from this repo.
- Lead with the question the user actually has: "Why did I pick that library three months ago?"

## Don't

Gradients · a second accent · emoji as icons · drop shadows on static cards · illustration or
mascots · a rounded container with a left accent bar as a callout (use a bare 2px neon rule) ·
Inter/Roboto anywhere · full-width neon fills · pill buttons.
