# Domain Packs

A domain pack is everything one subject area needs, in one folder:

```
domains/<name>/
  README.md                      what this pack adds, and how to install it
  agents-domain-<name>.md        the dispatch flow and conventions
  skills/                        skills that belong to this domain (may be empty)
```

Packs exist because domains aren't just folders — each one carries its own ingest flow, its
own conventions, sometimes its own page types, and usually its own skills. Bundling them means
adopting a subject area is one decision instead of six.

---

## Available packs

| Pack | What it's for | Skills | Extends the schema? |
|---|---|---|---|
| [knowledge](knowledge/) | What exists in the world — general concepts, tools, products, techniques | `research` | no |
| [home](home/) | What you own and operate — hardware, devices, self-hosted services | `deploy-runbook` | no |
| [projects](projects/) | What you're building, planning, or tracking | — (core skills cover it) | no |
| [books](books/) | Reading — what you've read, what you might read, and why | `book-capture` | **yes** — adds author, series, candidate page types |
| [cooking](cooking/) | Recipes and meal planning | `recipe-capture` | **yes** — adds the recipe page type |
| [gaming](gaming/) | Computer and console games — played, playing, backlog, dropped | `game-capture`, `game-drop` | **yes** — adds game and franchise page types |

**knowledge**, **home** and **projects** are installed by default. The rest are available and
inert until you install them.

Those three aren't an arbitrary starter set — they're the minimum that makes the **Entity
Placement Rule** satisfiable. That rule sends humans to `people/`, general things to
`knowledge/entities/`, and *owned* things to a domain's own `entities/`. Without `home`, that
last branch has no destination: `projects` is wrong, because a project is something you're
building rather than something you have. Drop any of the three and something has nowhere to go.

---

## Then stop for a while.

The temptation is to install everything on day one. Don't.

Nine domains in the wiki this came from accumulated over months, each added when an existing
domain genuinely couldn't hold something. Installing all of them upfront gets you empty
folders, an index full of headings with nothing under them, and an agent making placement
decisions between categories that have no content to compare against.

**Domains are cheap to add later and expensive to abandon half-populated.** Live on the three
installed ones for a while. Add a fourth when you actually reach for it and it isn't there —
not because a pack looks interesting.

---

## Installing a pack

There's no installer, and you don't need one. **Ask your agent:**

> "Install the books domain pack."

It reads that pack's README and does the five steps. If you'd rather do it by hand, they are:

1. **Add a dispatch row** in `agents-core.md` § 3 INGEST → Dispatch, pointing at
   `domains/<name>/agents-domain-<name>.md`
2. **Add the domain** to the folder list in `agents-core.md` § 4
3. **Create the folders** — `wiki/<name>/entities/` and `wiki/<name>/references/`
   (some packs vary; the pack README says)
4. **Create `wiki/index-<name>.md`** from the pattern in an existing index
5. **Copy the pack's skills** into your tool's skills location — `.claude/skills/` for Claude
   Code, elsewhere for other tools (see [10 — Skills](../docs/10-skills.md))

Uninstalling is the same list in reverse. Nothing is entangled: a pack that isn't in the
dispatch table is simply never loaded.

---

## Writing your own

A pack is worth creating when a subject area has conventions that don't fit any existing
domain — not merely when you have a lot of pages about something.

The test: **would the ingest flow differ?** If filing a recipe genuinely needs different steps
than filing an article, that's a domain. If it's the same flow with different subject matter,
it's a `subdomain:` field on an existing domain.

Copy the shape of `domains/knowledge/` — it's the simplest complete example. The pack README
should state what the pack adds, what folders it needs, and whether it extends the page-type
schema, so the agent can install it without you explaining anything.

Pull requests adding packs are welcome.
