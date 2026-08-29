# benchbook — site

The worked example from [15 — Publishing](../docs/15-publishing.md): an Astro site that reads
the repo's own `wiki/` folder directly and renders it as a website. Currently unstyled —
functional first; a real design lands via the `benchbook-design` skill (see the Phase 6 entry
on the benchbook wiki project page) once it exists.

## How it reads the wiki

`src/lib/wiki.js` walks `../wiki` at build time — no content duplication, no symlink. It:

- parses each page's frontmatter and body with `gray-matter`
- groups pages by their `domain:` frontmatter field for the domain-index routes
- renders markdown to HTML with `marked`, then rewrites `[text](relative/path.md)` links to
  site routes, resolved the same way the wiki's own convention resolves them (relative to the
  linking page's own directory — see `agents-core.md` Hard Rule 4)

If you fork this and restructure `wiki/`, `src/lib/wiki.js` is the one file that needs to
change.

## Routes

| Route | Renders |
|---|---|
| `/` | Home — every domain found, with a page count |
| `/domain/<domain>/` | Every page whose `domain:` frontmatter matches |
| `/page/<slug>` | One wiki page, `slug` = its path under `wiki/` with `.md` stripped |

Pages with `domain: null` (people, meta pages like `index.md`/`log.md`/`todo.md`) are built and
reachable by direct link, just not featured on a domain listing.

## Commands

Run from this directory (`site/`):

| Command | Action |
|---|---|
| `npm install` | Install dependencies |
| `npm run dev` | Dev server at `localhost:4321` |
| `npm run build` | Build to `./dist/` — this is what CI runs |
| `npm run preview` | Preview the production build locally |

## Deployment

`.github/workflows/deploy.yml` (repo root) builds this on every push to `wiki/` or `site/` and
deploys via `withastro/action` + `actions/deploy-pages`. **Won't serve a live URL until the
repo is public** — GitHub Pages on a private repo needs a paid plan. See
[15 — Publishing](../docs/15-publishing.md) for the full reasoning, including why GitHub Pages
is the default recommendation over self-hosting.
