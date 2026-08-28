# benchbook — Domain Rules: Cooking

> Loaded during INGEST for the cooking domain. Read alongside `agents-core.md`.

---

## What belongs here

Recipes and the reference material around them — technique guides, method comparisons,
ingredient deep-dives.

**Default subdomain:** none. Recipes are organised by category folder within
`wiki/cooking/recipes/`.

This pack **extends the page-type schema** with a `recipe` type, and it's the one domain that
pairs each wiki page with a **machine-readable file in an external format**. That dual-file
pattern is the interesting part, and it generalises to any domain where something else needs
to read your data.

---

## The dual-file pattern

Every recipe is two co-located files:

```
wiki/cooking/recipes/<category>/<slug>.cook   ← Cooklang. Machine-readable. Source of truth.
wiki/cooking/recipes/<category>/<slug>.md     ← wiki companion. Frontmatter + notes.
```

[Cooklang](https://cooklang.org) is a plain-text recipe markup — ingredients, timers and
cookware are marked inline so tools can parse quantities, scale portions, and generate shopping
lists. The `.md` companion is what makes the recipe a *wiki page*: frontmatter, indexing,
links, notes.

**The `.cook` file is source of truth** for anything present in both. On edit, update `.cook`
first, then mirror to `.md`. LINT runs a drift check between them.

That rule is the whole point of naming a source of truth: two files carrying the same fact
*will* diverge, and when they do you need to already know which one wins.

**Images** co-locate by filename — `<slug>.jpg` beside the pair, and `<slug>.<step>.jpg` for
step photos. No frontmatter field: naming *is* the metadata, because that's how Cooklang tools
find them.

---

## Categories

Five, and they're a starting point rather than a rule:
`soups`, `starters`, `mains`, `desserts`, `condiments`.

**Always ask if the category is unclear.** A misfiled recipe is findable; a category that
means two different things is not.

Note one boundary that recurs: **brewing and technique content is a reference page inside
cooking; appliance manuals belong to whichever domain owns the appliance.** A coffee machine's
manual is homelab; how to dial in an espresso is cooking.

---

## Cooklang syntax quick reference

```cook
>> servings: 4
>> prep time: 20 min
>> cook time: 35 min
>> category: Mains
>> vegetarian: yes

Dice the @onion{1} and fry in a #pan{} for ~{5%min}.
Add @flour{200%g} and @cream cheese{50%g}.

== Second section ==

-- a comment
```

- **Ingredients:** `@name{quantity%unit}` — `@flour{200%g}`, `@egg{2}`, `@salt{}`
- **Multi-word ingredients require braces:** `@cream cheese{50%g}`
- **Timers:** `~{10%min}` · **Cookware:** `#pot{}` · **Sections:** `== Name ==` ·
  **Comments:** `-- text`

**Language and units are yours to choose.** Pick one and stay consistent — a recipe collection
half in metric and half in cups is worse than either. The wiki this came from writes recipes in
German with metric units while keeping all *headings and field names* in English; that split
works well and is worth copying.

---

## `.md` companion frontmatter

`type: recipe`, plus `category:`, `vegetarian:`, `servings:`, `prep_time:`, `cook_file:`.

**Derived fields**, populated by inspecting the `.cook` file:

| Field | Values | How to derive |
|---|---|---|
| `cuisine` | a controlled list, or `null` | Infer from ingredients and name. Use `null` for "unsure" — never a catch-all bucket |
| `heat` | `none \| mild \| medium \| hot` | Check for chilli and pepper ingredients |
| `contains_meat` | `yes \| no` | `no` includes fish and seafood — pair with `vegetarian:` to answer dietary questions |
| `allergens` | controlled list, `[]` if none | Scan ingredients: peanut/peanut oil → `peanut`; butter/cream/milk/cheese/yoghurt → `lactose`; wheat/flour/pasta/bread → `gluten`; soy sauce/tofu/miso → `soy`; egg → `egg`; prawns/crab/lobster → `shellfish`; sesame/tahini → `sesame`; fish/fish sauce → `fish` |
| `kid_friendly` | `yes \| no \| adaptable` | `no` if fundamentally adult (alcohol, very spicy, offal); `adaptable` otherwise |

**Keep allergen terms singular and spelled one way.** They're a controlled vocabulary that
something will eventually filter on, and `peanut` vs `peanuts` silently splits the set.

### The tri-state that lives in only one file

`vegetarian:` is **binary in `.cook`** (`yes | no`) but **tri-state in `.md`**
(`yes | no | possible`).

`possible` means the recipe as written isn't vegetarian, but a vegetarian version works with a
simple ingredient swap — no change of method. **LINT does not flag `.md: possible` against
`.cook: no`** — that pairing is expected, not drift.

This is worth noting as a pattern: when two files share a schema, the richer file may carry
*extra* states, but the drift check has to know about them or it cries wolf forever.

### `## Notes` — optional, max 5 bullets

**Required** when `vegetarian: possible` (describe the substitution) or
`kid_friendly: adaptable` (describe the adaptation). Otherwise: ingredient notes, technique
tips, origin.

Omit the section entirely if there's nothing non-obvious to say. An empty `## Notes` on every
recipe is the placeholder problem again.

---

## Variants

`variant_of:` — the slug of the base recipe. Use it **only for structural variants**: a
different cooking method, a significantly different ingredient list, or a different category.

A simple one-ingredient swap is **not** a variant. That belongs in `## Notes` with
`vegetarian: possible`.

**Slug discipline when a variant is warranted:**

| Axis | Pattern | Example |
|---|---|---|
| Plain variant | `-v2`, `-v3` | `tomato-soup-v2` |
| Diet | `-vegetarian` | `tomato-soup-vegetarian` |
| Source | `-<author>` | `tomato-soup-hazan` |
| Other | `-<distinguishing-noun>` | `tomato-soup-thai` |

Always confirm the slug with the human before writing files.

---

## Dispatch flow

**C1.** Confirm the **category** — required, ask if unclear.

**C2.** Confirm **vegetarian** — required, ask if not obvious from the ingredients.

**C3. Re-ingest check.** If a recipe with this slug already exists, ask: *"Update the existing
one, or create a variant?"* Apply the slug discipline above.

**C4.** Write the `.cook` file.

**C5. Validate it** with the Cooklang tooling (`cook doctor validate <file>`) before continuing.
Fix any errors. If the binary isn't installed, note that validation was skipped — don't
silently pass.

**C6.** Write the `.md` companion with mirrored frontmatter plus the derived fields above.

**C7.** Update the domain index.

**Chat-dictated recipes** skip pre-flight steps 1 and 4 — there's no raw file, and provenance
is the conversation.

---

## Checklist

- [ ] Category and vegetarian confirmed
- [ ] Re-ingest check performed if the slug already exists
- [ ] `.cook` validated (or skip explicitly noted)
- [ ] `.cook` and `.md` mirrored on shared metadata — `.cook` wins
- [ ] Derived fields populated: cuisine, heat, contains_meat, allergens, kid_friendly
- [ ] `## Notes` bullet present if `vegetarian: possible` or `kid_friendly: adaptable`
- [ ] Index updated
