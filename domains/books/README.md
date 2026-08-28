# Pack: books

Reading — what you've read, what you're reading, what you abandoned, and what you might read
next.

## What it adds

| | |
|---|---|
| **Rules** | `agents-domain-books.md` — page types, the series threshold, rating precision, dispatch flow |
| **Skills** | `book-capture` — capture a recommendation, collision-check it against your library, file it as a ranked candidate |
| **Folders** | `wiki/books/authors/`, `wiki/books/series/`, `wiki/books/candidates/` |
| **Index** | `wiki/index-books.md` + three sub-indexes (authors, series, candidates) |
| **Schema** | **Yes — adds `author`, `series` and `candidate` page types** |
| **Subdomains** | None |

## Install

1. Add a dispatch row in `agents-core.md` § 3 pointing at
   `domains/books/agents-domain-books.md`
2. Add `books` to the domain list in `agents-core.md` § 4
3. Add `author`, `series`, `candidate` to the `type:` enum in `agents-page-conventions.md`
4. `mkdir -p wiki/books/authors wiki/books/series wiki/books/candidates`
5. Create `wiki/index-books.md` plus the three sub-indexes
6. Copy `skills/book-capture/` into your tool's skills location

Or ask your agent: *"install the books domain pack."*

## Why this pack is worth reading even if you don't want it

**It's the proof that domains can extend the schema.** The core four page types genuinely
couldn't hold this: a series isn't an entity, an author needs a table of works rather than
prose, and a book you *might* read is a different kind of thing from one you've read.

It also carries the clearest example in benchbook of **a rule that changed because measuring it
proved it wrong.**

The series-page rule started as "create one when the series has 2+ published volumes." That
generated a 51-page backlog. Measuring the backlog showed the rule over-generated badly — the
value of a series page depended entirely on the shelf status of your entry point into it:

| Entry point | Worth a page? | In the backlog |
|---|---|---|
| `to-read` | Yes — reading order is actionable | 18 built |
| `read`, rated 4+ | Yes — continuing is a live question | 4 built |
| `read`, rated ≤3 | No | 16 skipped |
| `abandoned` | No — and actively misleading in a to-read context | 10 skipped |

**Two-thirds of what the naive rule would have generated was worthless.** The refined rule is
in `agents-domain-books.md`, with the table.

Three other hard-won rules worth stealing regardless of domain:

- **Never write a placeholder.** After a bulk import, 169 of 208 author pages rendered a
  literal "*To be filled in.*" A placeholder on four-fifths of your pages isn't a prompt, it's
  noise you learn to skip. Either real content or no section.
- **Imported and hand-entered values are different claims about precision.** A `4` from an
  import and a `4.0` you gave directly are not the same fact. Never back-fill a decimal to
  make a column look tidy.
- **Normalize before you group.** Library exports tag the same series inconsistently
  ("Expanse" / "The Expanse"), which silently splits one series into two pages.
