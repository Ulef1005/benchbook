# benchbook — design assets

The mark is the Ordnance Survey benchmark symbol: a horizontal bar with an arrow pointing up
into it. A fixed reference point of known elevation. It doesn't move; you come back to it.

## Palette

| Role | Hex | Use |
|---|---|---|
| Graphite | `#21201C` | Primary. Mark on light grounds, all body text, dark backgrounds. |
| Paper | `#F5F1E8` | Light ground. Mark on dark grounds. |
| Neon | `#FF3DBE` | Accent only. The mark in colour contexts, single-element highlights. Never for body text. |

## Type

- **Wordmark and supporting copy:** IBM Plex Mono, weight 500 (wordmark) / 400 (copy). SIL Open Font License.
- **Wordmark is always lowercase:** `benchbook`. Letter-spacing `-0.01em`, line-height 1.
- Lockup: mark left, wordmark right, gap ≈ 0.38× the mark height; mark height ≈ 1.25× the wordmark font size.

## Assets

| File | Size | Where it's used |
|---|---|---|
| `mark/mark-graphite.svg` | vector, transparent | Mark on light grounds |
| `mark/mark-paper.svg` | vector, transparent | Mark on dark grounds |
| `mark/mark-neon.svg` | vector, transparent | Accent contexts |
| `mark/mark-currentcolor.svg` | vector, inherits `color` | Inline in HTML/docs, monochrome/stamp use |
| `social-preview.png` | 1280×640 | GitHub → Settings → Social preview |
| `readme-banner.png` | 1280×280 | Top of the root `README.md` |
| `favicon/favicon.svg` + `favicon-{16,32,180,512}.png` | — | Future docs site; 180 is the Apple touch icon |

## Rules

- The mark ships with a **transparent background**. Never bake in a white square.
- Two shapes only. Don't outline, round, rotate, or add a container to it.
- Never place text inside the mark; the wordmark is a separate lockup.
- Clear space around the mark: ≥ 25% of its height on all sides.
- Minimum mark size: 16 px. It is tested at that size and holds.
- Works in pure monochrome — check black-on-white before adding colour.
- One accent, used once per surface. No gradients.

## Slogan

> The agentic workbench for builders.
