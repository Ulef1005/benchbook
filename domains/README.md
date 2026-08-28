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
| [knowledge](knowledge/) | General concepts, tools, products, techniques — things that exist independently of you | `research` | no |
| [projects](projects/) | Things you're building, planning, or tracking | — (core skills cover it) | no |
| [homelab](homelab/) | Self-hosted services and hardware you own and operate | `deploy-runbook` | no |
| [books](books/) | Reading — what you've read, what you might read, and why | `book-capture` | **yes** — adds author, series, candidate page types |
| [cooking](cooking/) | Recipes and meal planning | `recipe-capture` | **yes** — adds the recipe page type |

**knowledge** and **projects** are installed by default in a fresh clone. The rest are
available and inert until you install them.

---

## Install two. Not five.

The temptation is to install everything on day one. Don't.

Nine domains in the wiki this came from accumulated over months, each added when an existing
domain genuinely couldn't hold something. Installing all of them upfront gets you empty
folders, an index full of headings with nothing under them, and an agent making placement
decisions between categories that have no content to compare against.

**Domains are cheap to add later and expensive to abandon half-populated.** Start with the two
that are already installed, or swap one out for a pack that fits you better. Add a third when
you actually reach for it and it isn't there.

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
