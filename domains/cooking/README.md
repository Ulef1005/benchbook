# Pack: cooking

Recipes and the reference material around them.

## What it adds

| | |
|---|---|
| **Rules** | `agents-domain-cooking.md` — the dual-file pattern, categories, derived fields, variant discipline |
| **Skills** | `recipe-capture` — turn a recipe from anywhere into a validated `.cook` + `.md` pair |
| **Folders** | `wiki/cooking/recipes/<category>/`, `wiki/cooking/references/` |
| **Index** | `wiki/index-cooking.md` |
| **Schema** | **Yes — adds the `recipe` page type** |
| **Subdomains** | None — recipes organise by category folder |

## Install

1. Add a dispatch row in `agents-core.md` § 3 pointing at
   `domains/cooking/agents-domain-cooking.md`
2. Add `cooking` to the domain list in `agents-core.md` § 4
3. Add `recipe` to the `type:` enum in `agents-page-conventions.md`
4. `mkdir -p wiki/cooking/recipes/{soups,starters,mains,desserts,condiments} wiki/cooking/references`
5. Create `wiki/index-cooking.md`
6. Copy `skills/recipe-capture/` into your tool's skills location
7. *(Optional)* Install [Cooklang](https://cooklang.org) tooling for `.cook` validation

Or ask your agent: *"install the cooking domain pack."*

## Why this pack is worth reading even if you don't cook

It's the only domain that pairs each wiki page with a **machine-readable file in an external
format** — [Cooklang](https://cooklang.org), a plain-text recipe markup where ingredients,
timers and cookware are marked inline so tools can parse quantities and scale portions.

That dual-file pattern generalises to any domain where something *other than your agent* needs
to read your data. Three rules make it work, and all three transfer:

**Name the source of truth explicitly.** The `.cook` file wins; the `.md` mirrors it. Two files
carrying the same fact *will* diverge, and when they do you need to already know which one is
right — deciding in the moment means deciding wrong half the time.

**Teach the drift check about legitimate differences.** `vegetarian:` is binary in `.cook` but
tri-state in `.md` (the extra value means "adaptable with a simple swap"). LINT knows that
pairing is expected and doesn't flag it. A drift check that cries wolf gets muted, and then it
catches nothing.

**Derived fields need explicit derivation rules.** The allergen field isn't filled in by vibes
— the domain file lists exactly which ingredients map to which allergen. Vague instructions
produce inconsistent data that looks fine until you try to filter on it.

## A note on language

The shipped rules use English throughout. The wiki this came from writes recipe *content* in
German with metric units while keeping all headings and field names in English — that split
works well. Pick a convention and hold it; a collection half in metric and half in cups is
worse than either.
