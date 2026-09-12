# Pack: knowledge

**Installed by default.**

General concepts, tools, products, frameworks, techniques — things that exist in the world
independently of you. The default home for anything you've *learned about* rather than *own*.

## What it adds

| | |
|---|---|
| **Rules** | [agents-domain-knowledge.md](agents-domain-knowledge.md) — dispatch flow, the 36-predicate controlled vocabulary, channel/author entity trigger |
| **Skills** | `research` — multi-source research → synthesis → offer to file |
| **Folders** | `wiki/knowledge/entities/`, `wiki/knowledge/references/` |
| **Index** | `wiki/index-knowledge.md` |
| **Schema** | No new page types. Uses source / entity / reference. |
| **Subdomains** | None |

## Why you probably want it

It's the domain that absorbs everything not covered by a more specific one. Without it, every
article you read has nowhere obvious to go.

The controlled predicate vocabulary is the part worth reading — see
[agents-domain-knowledge.md](agents-domain-knowledge.md) § Predicate Vocabulary. A free-text
relation field becomes unqueryable within months; that list is what stops it.

It ships in three blocks: **18 core** predicates that apply to any wiki, **8** for provenance and
ownership, and **10 operations** ones (`backed_up_by`, `fronts`, `monitors`, `secures`,
`stores_data_on` and their inverses) that only matter if you run services — skip that block
entirely if you don't, it costs nothing. Queried with `./scripts/relations.py <page>`, which
reads a page's inbound *and* outbound edges, because each fact is stored exactly once and a
page's own table therefore shows only half of them.
