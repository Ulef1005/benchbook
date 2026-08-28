# benchbook — Domain Rules: Books

> Loaded during INGEST for the books domain. Read alongside `agents-core.md`.

---

## What belongs here

Reading — what you've read, what you're reading, what you abandoned, and what you might read
next.

**Default subdomain:** none. All books-domain pages land directly under `wiki/books/`.

This pack **extends the page-type schema**. It's the clearest demonstration in benchbook that
a domain may add types when the core four genuinely can't hold something — a series is not an
entity, an author needs a table of works rather than prose, and a book you *might* read is a
different kind of thing from one you have read.

---

## Page types

### Author page — `wiki/books/authors/<author-slug>.md`

**The backbone.** Every book by that author, on any shelf, lives here as a table row. No book
is ever reachable only through some other page.

`type: author`. Table columns: Title / Series / Year / Status / Rating / Read.

> **`## Summary` is required only for authors with 2+ books in the library.** For a
> single-book author the blurb already carries everything worth saying. **Never write a
> placeholder** — either a real, sourced bio or no section at all.
>
> This rule exists because the original didn't have it: after a bulk import, **169 of 208
> author pages (81%) rendered a literal "*To be filled in.*"** A placeholder that appears on
> four-fifths of your pages isn't a prompt to fill it in, it's just noise you learn to skip.

### Series page — `wiki/books/series/<series-slug>.md`

`type: series`. Holds the series' blurbs in reading order, plus a `## Volumes` table.
Volumes you don't own are listed with status `–`.

**Create one when** the series has **2+ published volumes** *and* your entry point into it is
`to-read`, `reading`, or `read` rated 4+.

**Skip it when** your entry point is `abandoned`, or `read` and rated ≤3.

> **Where that condition came from.** The rule was first written as simply "2+ published
> volumes," which generated a 51-page backlog. Measuring that backlog showed the rule
> over-generated — every one of the 51 had exactly one book in the library, and the page's
> value depended entirely on that book's shelf status:
>
> | Entry point | Worth a page? | In the backlog |
> |---|---|---|
> | `to-read` | **Yes** — reading order is directly actionable | 18 built |
> | `read`, rated 4+ | **Yes** — continuing is a live question | 4 built |
> | `read`, rated ≤3 | No — "what's book 2" isn't a question being asked | 16 skipped |
> | `abandoned` | **No** — a page listing five more volumes is noise, and actively misleading in a to-read context | 10 skipped |
>
> Two-thirds of what the naive rule would have generated was worthless. Revisit if a skipped
> book's status ever changes.

**Group by a normalized series name** — case-insensitive, leading "The " stripped. Library
exports tag the same series inconsistently ("Expanse" on one book, "The Expanse" on another),
which silently splits one series into two pages if you group on the raw string.

### Candidate page — `wiki/books/candidates/<book-slug>.md`

`type: candidate`. **Only for to-read books.** The sole page type carrying `source:`,
`rank_score:`, and `## Why You'll Like It`.

Required frontmatter: `author` (slug), `year`, `status: to-read`, `source` (origin URL or
capture context). Optional: `series`, `source_url`, `rank_score`.

Promotion to read happens by **deleting the candidate page** and adding the row to the author
table — not by changing `status:`.

### No individual page for a read, abandoned, or currently-reading book

That history is a row in the author's table, plus a blurb on the series page if it has one.

This is deliberate anti-bloat. A page per read book would have added ~390 pages to a 781-page
wiki — half the wiki, carrying almost no information that the table row doesn't.

---

## Index shape — a books-specific deviation

The domain index is **split by page type**: a small `wiki/index-books.md` master pointing at
`index-books-authors.md`, `index-books-series.md`, and `index-books-candidates.md`.

This deviates from the one-index-per-domain shape in `agents-core.md § 6`. It happened because
a single file reached 357 lines and grew ~12 per ingest, and because a query almost never needs
all three catalogues at once.

**It's the same split applied recursively** — split on the axis you actually query by. If a
second domain ever needs this treatment, that's the pattern.

---

## Rating convention

- Scale is **1–5**.
- **One decimal place allowed** for ratings you give directly — e.g. `4.2`.
- **Imported ratings stay integers.** They were captured at integer resolution and cannot be
  re-derived finer. Never back-fill a decimal onto an imported rating to make a column look
  tidy: a `4` from an import and a `4.0` given directly are *different claims about
  precision*, and flattening that destroys information.
- **Decimal point, never a comma.** A decimal comma breaks every downstream parser, silently.
- Averages over mixed integer and decimal ratings are fine — report to 2dp, never round the
  inputs first.

The precision matters because `rank_score` on candidate pages is 1–10 to one decimal, and
comparing a prediction against its outcome is the point of having candidates at all. Rounding
4.2 to 4 discards exactly what makes "predicted 9.5, actual 4.2" a usable calibration point.

---

## Shelf → status vocabulary

| Shelf | Status value |
|---|---|
| read | `read` |
| to-read | `to-read` |
| did-not-finish | `abandoned` |
| currently-reading | `reading` |

---

## Language convention

Section headings, table columns, and status labels are **always English**. **Only blurb content
follows the book's own original language** — a German book gets a German blurb, not a
translated one. Don't translate; write in whatever language the source material is in.

---

## Dispatch flow

### A book finished (read or abandoned)

**B1.** Find or create the author page. New author → minimal page: frontmatter plus a
`## Books` table with just this row. No `## Summary` while they have one book.

**B2.** Add the row: Title / Series (linked, if applicable) / Year / Status / Rating / Read
date.

**B3.** If it belongs to a series meeting the threshold above and no series page exists, create
one and **move** the relevant blurbs there. If one exists, add a `## Volumes` row — checking
against the *normalized* series name, not an exact string match.

**Blurbs move on creation. Never copy** — move, then verify the author page no longer carries
it.

**B4.** Fetch a blurb from a real source. Enrichment failure → stub it and note why.
**Never fabricate a plot summary.**

**B5.** If this book had a candidate page, delete it — its content is now superseded by the
author row and blurb. (The No-Deletion Rule doesn't apply to a page correctly absorbed into its
successor, but confirm the blurb carried over first.)

### A recommendation captured

**B6.** Create the candidate page. `source:` is the origin; `## Source` **quotes what was
actually said**, not a paraphrase.

**B7. Also add the book to its author's page** — find or create it, add a `to-read` row, and
put the blurb on the author page (or series page, if it qualifies) *as well as* the candidate
page.

> **This is the easiest step in the whole domain to miss.** A to-read book that isn't in a
> qualifying series needs its blurb written in **two** places. During a bulk import every
> enrichment pass initially skipped the author-page write for to-read books, silently leaving
> **45 books** stuck on "*Blurb pending.*" on the author page while the candidate page had the
> real text.

**B8. Check it against the library first.** A recommendation for something already on your
abandoned shelf should say so on the candidate page, not be presented as fresh.

**B9.** `## Why You'll Like It` stays a stub until you have an actual ranking mechanism. Don't
hand-write a rationale ahead of one.

### Post-flight

**B10.** Update the index files.

**B11.** Append to `log.md` **only** if this created a genuinely new author, series, or
candidate page. An ordinary new row on an existing author page is not a wiki-structural event.

---

## Checklist

- [ ] Author page exists before anything else
- [ ] Series page only when 2+ published volumes **and** the entry-point condition holds
- [ ] Series matched on the normalized name, not the raw string
- [ ] Candidate pages only for `to-read`
- [ ] To-read blurb written in **both** places
- [ ] Recommendation checked against the existing library before being treated as fresh
- [ ] Blurb fetched or stubbed with a reason — **never fabricated**
- [ ] Rating uses a decimal point; imported ratings left as integers
- [ ] Index files updated; `log.md` only for genuine new-page creation
