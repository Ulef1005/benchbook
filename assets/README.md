# benchbook — design assets

The mark is the Ordnance Survey benchmark symbol: a horizontal bar with an arrow pointing up
into it. A fixed reference point of known elevation. It doesn't move; you come back to it.

## Palette

| Role | Hex | Use |
|---|---|---|
| Graphite | `#21201C` | Text, dark grounds, and the monochrome/print mark. |
| Paper | `#F5F1E8` | Light ground, and the mark where only one flat light colour is available. |
| Neon | `#FF3DBE` | **The default mark colour** — used on every shipped asset. Also single-element highlights. Never for body text. |

## Type

- **Wordmark and supporting copy:** IBM Plex Mono, weight 500 (wordmark) / 400 (copy). SIL Open Font License.
- **Wordmark is always lowercase:** `benchbook`. Letter-spacing `-0.01em`, line-height 1.
- Lockup: mark left, wordmark right, gap ≈ 0.38× the mark height; mark height ≈ 1.25× the wordmark font size.

## Assets

| File | Size | Where it's used |
|---|---|---|
| `mark/mark-neon.svg` | vector, transparent | **Default mark**, both light and dark grounds |
| `mark/mark-graphite.svg` | vector, transparent | Monochrome / print on light grounds |
| `mark/mark-paper.svg` | vector, transparent | Monochrome on dark grounds |
| `mark/mark-currentcolor.svg` | vector, inherits `color` | Inline in HTML/docs, monochrome/stamp use |
| `social-preview.png` | 1280×640 | GitHub → Settings → Social preview |
| `readme-banner-light.png` | 1280×280 | Top of the root `README.md`, GitHub light theme |
| `readme-banner-dark.png` | 1280×280 | Same, GitHub dark theme (graphite ground) |
| `favicon/favicon.svg` + `favicon-{16,32,180,512}.png` | — | Future docs site; 180 is the Apple touch icon |

## Rules

- The mark ships with a **transparent background**. Never bake in a white square.
- Two shapes only. Don't outline, round, rotate, or add a container to it.
- Never place text inside the mark; the wordmark is a separate lockup.
- Clear space around the mark: ≥ 25% of its height on all sides.
- Minimum mark size: 16 px. It is tested at that size and holds.
- Works in pure monochrome — check black-on-white before adding colour.
- The neon mark is the default; graphite/paper are for monochrome, print, and stamp contexts.
- One accent, used once per surface. No gradients.

## Slogan

> Your AI keeps the wiki. You keep the rules.

## Theme-aware banner

GitHub renders both themes. Serve both banner variants and let the browser pick:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="design/readme-banner-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="design/readme-banner-light.png">
  <img alt="benchbook" src="design/readme-banner-light.png" width="1280">
</picture>
```

The mark itself needs no theme swap — `mark/mark-neon.svg` holds on both grounds. Use the
`<picture>` swap only for the monochrome pair (`mark-graphite.svg` / `mark-paper.svg`).
The social preview card has no theme variant — GitHub accepts one image, and the graphite
ground already sits well in both light and dark chat clients.
