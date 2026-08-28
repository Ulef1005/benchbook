---
name: recipe-capture
description: "Turn a recipe from anywhere — a link, a photo, a cookbook page, or dictation in chat — into a validated Cooklang file plus its wiki companion page. Use when the user says 'add this recipe', 'capture this recipe', 'save this recipe', pastes a recipe URL, or dictates one. Confirms category and dietary status, checks for an existing recipe with the same slug, writes the .cook and .md pair, validates the Cooklang, and derives the structured fields. Never invents quantities."
license: MIT
metadata:
  version: 1.0.0
  category: cooking
---

# Recipe Capture

## Purpose

Produce the `.cook` + `.md` pair defined in `domains/cooking/agents-domain-cooking.md` — a
machine-readable recipe and its wiki page, consistent with each other, with the derived fields
actually derived rather than guessed.

---

## Step 1 — Extract the recipe

| Source | Approach |
|---|---|
| URL | Fetch and extract. Recipe sites bury the recipe under a life story — find the actual ingredient list and method |
| Photo of a page | Read it visually. Transcribe exactly |
| Chat dictation | Take it from the conversation; there's no raw file and provenance is the conversation |
| Cookbook | Ask whether the book itself should become a source page |

> **Never invent a quantity.** If the source is ambiguous or a photo is unreadable, ask. A
> plausible-looking `200 g` that was actually `2 tbsp` is indistinguishable from a correct one
> until someone cooks it.

---

## Step 2 — Domain checkpoint

Ask both, and don't guess:

1. **Category** — `soups | starters | mains | desserts | condiments`. Ask if unclear.
2. **Vegetarian** — ask if not obvious from the ingredients.

---

## Step 3 — Re-ingest check

```bash
ls wiki/cooking/recipes/*/ | grep -i <slug>
```

If a recipe with this slug exists, ask: **"Update the existing one, or create a variant?"**

Variant slug discipline:

| Axis | Pattern |
|---|---|
| Plain variant | `-v2`, `-v3` |
| Diet | `-vegetarian` |
| Source | `-<author>` |
| Other | `-<distinguishing-noun>` |

**Confirm the slug with the human before writing.**

And check it's genuinely a variant: a one-ingredient swap is **not** one. That belongs in
`## Notes` with `vegetarian: possible`.

---

## Step 4 — Write the `.cook` file

`wiki/cooking/recipes/<category>/<slug>.cook`

```cook
>> servings: 4
>> prep time: 20 min
>> cook time: 35 min
>> category: Mains
>> vegetarian: yes

Dice the @onion{1} and fry in a #pan{} for ~{5%min}.
Add @flour{200%g} and @cream cheese{50%g}.
```

- Ingredients `@name{qty%unit}` — multi-word names **require** braces
- Timers `~{10%min}` · Cookware `#pot{}` · Sections `== Name ==`
- Keep language and units consistent with the rest of the collection

---

## Step 5 — Validate

```bash
cook doctor validate wiki/cooking/recipes/<category>/<slug>.cook
```

Fix any errors before continuing.

**If the binary isn't installed, say validation was skipped.** Don't silently pass — an
unvalidated file that looks fine is how malformed syntax enters the collection.

---

## Step 6 — Write the `.md` companion

Mirror the shared metadata from `.cook` — **`.cook` is source of truth** — then derive:

| Field | How |
|---|---|
| `cuisine` | Infer from ingredients and name. **`null` if unsure** — never a catch-all bucket |
| `heat` | Check for chilli and pepper |
| `contains_meat` | `no` includes fish and seafood |
| `allergens` | Scan per the mapping in the domain rules: peanut, lactose, gluten, soy, egg, shellfish, sesame, fish. `[]` if none |
| `kid_friendly` | `no` if fundamentally adult; `adaptable` otherwise |
| `vegetarian` | `possible` if the non-vegetarian element swaps out without changing method |

**Keep allergen terms singular and spelled one way.** They're a controlled vocabulary something
will eventually filter on, and `peanut` vs `peanuts` silently splits the set.

`## Notes` — max 5 bullets, and **required** when `vegetarian: possible` (describe the swap) or
`kid_friendly: adaptable` (describe the adaptation). Otherwise omit the section entirely rather
than leaving it empty.

---

## Step 7 — Image

If there's a dish photo, save it as `<slug>.jpg` beside the pair. No frontmatter field —
**naming is the metadata**, because that's how Cooklang tools find it.

---

## Step 8 — Post-flight

1. Update `wiki/index-cooking.md` under the right category.
2. Append `## [YYYY-MM-DD] create | <Recipe Name>` to the log — new recipes only.

---

## Error handling

- **Quantities ambiguous or unreadable:** ask. Never guess.
- **Category unclear:** ask. A misfiled recipe is findable; a category that means two things
  isn't.
- **Slug exists:** stop and ask update-vs-variant before writing anything.
- **Validator missing:** proceed but state clearly that validation was skipped.
- **`.cook` and `.md` disagree after writing:** `.cook` wins. Fix the `.md`.
