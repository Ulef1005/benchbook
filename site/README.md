# benchbook — site

The worked example from [15 — Publishing](../docs/15-publishing.md): an Astro site that reads
the repo's own `wiki/`, `docs/`, `agents-*.md`, and `domains/*/README.md` directly and renders
them. Design comes from the `benchbook-design` skill (`.claude/skills/benchbook-design/` —
palette, type, the Ordnance Survey mark, layout and copy rules).

## How it reads the repo

Everything is an [Astro content collection](../src/content.config.ts) pointed at the real
files — nothing is copied into `site/`:

| Collection | Source | Schema enforces |
|---|---|---|
| `wiki` | `../wiki/**/*.md` (minus `DEMO.md`, which has no frontmatter and isn't a page) | The full frontmatter contract — `title`, `type`, `created`, `domain`, `publish`, etc. A page that doesn't match fails the build, same spirit as `scripts/lint.py` |
| `docs` | `../docs/**/*.md` | — |
| `contract` | `../AGENTS.md`, `../agents-*.md` | — |
| `domains` | `../domains/*/README.md` | — |

`plugins/remark-wiki-links.mjs` rewrites `[text](relative/path.md)` links to site routes at
parse time. A link that resolves inside the repo but outside a rendered collection (a skill
file, the root `README.md`) points at its GitHub blob instead of failing — a link is only
treated as broken, and only then fails the build, if it doesn't resolve to a real file at all.

## `publish: false` is a hard gate, not a suggestion

`src/lib/wiki.ts`'s `publishedWiki()` is the only way any page reads the `wiki` collection, and
it filters to `publish: true` unconditionally. `scripts/check-privacy.mjs` re-asserts this
after every build by scanning `dist/` for any `publish: false` page's title — belt and braces,
because a privacy filter that lives in exactly one place is one refactor away from silently not
running.

The demo content ships with `publish: true` set deliberately on the 14 actual demo pages —
that's a real per-page decision, not a bypass. A fork bringing real wiki content starts every
new page at the schema's own default (`publish: false`) and makes that same call per page.

## Commands

Run from this directory (`site/`):

| Command | Action |
|---|---|
| `npm install` | Install dependencies |
| `npm run dev` | Dev server at `localhost:4321` |
| `npm run build` | Build to `./dist/`, then the Pagefind search index, then the privacy check — this is what CI runs |
| `npm run check:privacy` | Just the privacy assertion, against an existing `dist/` |
| `npm run preview` | Preview the production build locally |

## Deployment

`.github/workflows/deploy.yml` (repo root) builds on every push to `main` and deploys via
`withastro/action` + `actions/deploy-pages`. Repo → Settings → Pages → Source must be set to
**GitHub Actions** once (not a per-push step). See
[15 — Publishing](../docs/15-publishing.md) for why GitHub Pages is the default recommendation
over self-hosting, and what changes if a custom domain lands later (drop `base` in
`astro.config.mjs`, update `site`).
