# Handoff: benchbook brand assets

## Overview
Visual identity for **benchbook**, an open-source system for a personal wiki that an AI agent
maintains under a written contract. The whole surface is a GitHub repository, so the identity
is: a primary mark, a wordmark lockup, a social preview card, a README banner, and a favicon
set. There is no app UI in this handoff.

## About the Design Files
The files in this bundle are **design references created in HTML** — prototypes showing the
intended look, not production code to copy. The exported SVG/PNG assets in `design/` ARE
production-ready and can be committed as-is. If any of this is later rebuilt in a docs site or
app, recreate the HTML references using that codebase's existing patterns rather than pasting
the prototype markup.

## Fidelity
**High-fidelity.** Final colours, type, sizes, and proportions. Treat measurements as exact.

## The mark
The Ordnance Survey **benchmark** symbol: a horizontal bar with an arrow pointing up into it.
A permanent reference point of known elevation — it doesn't move, you come back to it. Worth
one line in the README; the reference rewards anyone who looks it up.

Geometry, `viewBox="0 0 100 100"`, exactly two shapes, transparent background:
- `<rect x="18" y="24" width="64" height="11"/>`
- `<polygon points="50,35 27,76 73,76"/>`

Both filled with the same single colour (`currentColor` in the inline variant). No strokes, no
container, no rounding. Tested legible at 16 px.

## Design tokens

### Colour
| Token | Hex | Use |
|---|---|---|
| Graphite | `#21201C` | Text, dark grounds, monochrome/print mark. |
| Paper | `#F5F1E8` | Light ground. Mark on dark grounds. |
| Neon | `#FF3DBE` | **Default mark colour** on every shipped asset. Also single-element highlights. Never body text. |
| Hairline on dark | `rgba(245,241,232,.14)` | 1 px rules on graphite |
| Ruled line on paper | `rgba(33,32,28,.05)`, 34 px pitch | README banner texture |
| Muted copy on dark | `rgba(245,241,232,.66)` | Social-card slogan |

No gradients. One accent, used once.

### Type
- **IBM Plex Mono** — wordmark (500) and supporting copy (400). SIL OFL, freely embeddable.
- Wordmark always lowercase `benchbook`, `letter-spacing: -0.01em`, `line-height: 1`.
- Lockup: mark left, wordmark right. Gap ≈ 0.38× mark height. Mark height ≈ 1.25× wordmark
  font-size, optically aligned to the ascender of the "b" (not to the font's line box — set
  `line-height: 1` on the wordmark or the centring drifts low).

## Assets / views

### 1. Primary mark
Transparent SVG, square, 512 px nominal. `mark-neon.svg` is the default and holds on both
light and dark grounds, so the mark needs no theme swap. `mark-graphite.svg` /
`mark-paper.svg` are the monochrome pair (print, stamps, single-colour contexts) — swap those
two via `<picture>` + `prefers-color-scheme` if used. `mark-currentcolor.svg` for inline HTML.

### 2. Wordmark lockup
Mark + `benchbook` in IBM Plex Mono 500. Reference sizes: 34 px mark / 24 px type in
documentation contexts; 72 px mark / 58 px type in the banner; 140 px mark / 84 px type on the
social card.

### 3. Social preview card — `design/social-preview.png`
- **1280 × 640**, flat graphite `#21201C`. GitHub → Settings → Social preview.
- Content centred as a column: lockup (140 px neon mark, gap 26 px, `benchbook` in Plex Mono
  500 / 84 px / paper), then the slogan 18 px below.
- Slogan: **"Your AI keeps the wiki. You keep the rules."** — Plex Mono 400 / 28 px / line-height 1.5 /
  `letter-spacing: .01em` / `rgba(245,241,232,.66)`, centred, max-width 840 px.
- Two 1 px hairlines inset 36 px from top and bottom edges, full width minus 36 px each side.
- Nothing else. No badges, no screenshots, no feature list. Must stay legible at ~400 px wide.

### 4. README banner — `design/readme-banner.png`
- **1280 × 280**, paper `#F5F1E8` with a ruled-page texture:
  `repeating-linear-gradient(180deg, transparent 0, transparent 33px, rgba(33,32,28,.05) 34px)`.
- Centred lockup: 72 px neon mark, 22 px gap, `benchbook` in Plex Mono 500 / 58 px / graphite.
- **Two variants, required.** A 1280 px `#F5F1E8` slab at the top of a dark-theme GitHub page
  reads as a bright slab, so ship the inverted version too:
  `readme-banner-dark.png` — graphite `#21201C` ground, ruled texture at
  `rgba(245,241,232,.07)` (same 34 px pitch), paper `#F5F1E8` wordmark, neon mark unchanged.
- Serve them theme-aware in the README:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="design/readme-banner-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="design/readme-banner-light.png">
  <img alt="benchbook" src="design/readme-banner-light.png" width="1280">
</picture>
```

  The social card stays single-variant — GitHub accepts one social preview image and the
  graphite ground already works in light and dark chat clients.

### 5. Favicon set — `design/favicon/`
`favicon.svg` plus `favicon-16/32/180/512.png`. Neon mark on a full-bleed graphite tile so it
holds on light and dark browser chrome. 180 is the Apple touch icon.

## Rules (do not break)
- Mark ships with a transparent background — never bake in a white square.
- Two shapes only; no outlining, rotating, rounding, or wrapping in a container.
- No text inside the mark; the wordmark is a separate lockup.
- Clear space ≥ 25% of the mark's height on all sides.
- Minimum mark size 16 px.
- Must survive pure monochrome — check black-on-white before adding colour.
- Anti-brief: no brains, neural graphs, connected dots, orbs, sparkles, robot faces,
  lightbulbs, or purple-to-blue gradients.

## Interactions & Behavior
Static brand assets — no interactive states. The only conditional behaviour is theme swapping
in the README via `<picture>` + `prefers-color-scheme`.

## Files in this bundle
| File | What it is |
|---|---|
| `benchbook-brand.html` | Design reference: brand sheet (mark swatches, 16 px legibility test, wordmark lockups, palette) plus a repo-page mockup in light and dark |
| `benchbook-social-card.html` | Design reference: the 1280 × 640 social preview |
| `benchbook-readme-banner.html` | Design reference: the 1280 × 280 README banner, light |
| `benchbook-readme-banner-dark.html` | Design reference: the same banner, dark theme |
| `design/` | Production assets: mark SVGs, PNG exports, favicons, and the asset README |

## Suggested repo placement
```
design/
  README.md                 palette, type, usage rules
  mark/                     mark-graphite.svg, mark-paper.svg, mark-neon.svg, mark-currentcolor.svg
  favicon/                  favicon.svg, favicon-16.png, favicon-32.png, favicon-180.png, favicon-512.png
  social-preview.png        upload via repo Settings, not referenced from the README
  readme-banner-light.png   referenced at the top of README.md (light theme)
  readme-banner-dark.png    same, dark theme, via <picture> + prefers-color-scheme
```

## Screenshots

`screenshots/mark-and-wordmark-options.png` — the brand sheet
`screenshots/repo-page-mockup-light-dark.png` — the mark in context: repo page, light and dark (generic code-host layout, not GitHub's own chrome)
`screenshots/social-preview-1280x640.png` — the social card as exported
`screenshots/readme-banner-1280x280.png` — the light README banner as exported
`screenshots/readme-banner-dark-1280x280.png` — the dark variant
