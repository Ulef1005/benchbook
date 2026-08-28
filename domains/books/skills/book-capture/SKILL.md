---
name: book-capture
description: "Capture a book recommendation into the wiki as a ranked to-read candidate. Use when the user pastes a link or screenshot text recommending a book, or says 'add this book', 'someone recommended X', 'add X to my to-read', 'should I read X', 'have I read X', or 'do I already have X'. Always checks the existing library across every shelf first — a recommendation for something already read or abandoned is reported as a collision, not filed as new. Fetches a real blurb and writes the candidate page, author-table row and series page per the books-domain flow. Never invents a plot summary."
license: MIT
metadata:
  version: 1.0.0
  category: books
---

# Book Capture

## Purpose

Turn a recommendation from anywhere into a properly filed candidate — **or** tell the user they
already read it in 2019 and gave it three stars.

The collision check is not a nicety. It's the most-used feature of this skill.

---

## Step 1 — Identify the book

From a link, a screenshot, a quote, or just a title. Establish **title + author** — a title
alone is ambiguous more often than you'd expect.

If the source is a post or article, note what was actually *said* about it. That quote goes on
the page verbatim later; a paraphrase loses the reason it appealed.

---

## Step 2 — Collision check, before anything else

Search **every shelf**:

```bash
grep -ril "<title>" wiki/books/authors/ wiki/books/series/ wiki/books/candidates/
```

Then check the author page's `## Books` table directly — a read book has no page of its own,
only a row.

| Found where | Report as |
|---|---|
| `read` | **Already read.** Give the rating and date. Stop |
| `abandoned` | **Already abandoned.** Say so plainly — this is the most useful collision of all |
| `reading` | **Currently reading** |
| existing candidate | **Already on the to-read list**, with when and from where |
| not found | Proceed to Step 3 |

**A collision is a successful outcome, not a failure.** Report it and stop; don't file a
duplicate. Someone enthusiastically recommending a book you bounced off is exactly the moment
this wiki earns its keep.

---

## Step 3 — Fetch a real blurb

Get an actual description from a real source — a book database, the publisher, the author's
site.

> **Never invent a plot summary.** If you can't fetch one, write a stub saying so and note why.
> A fabricated blurb is indistinguishable from a real one six months later, and it will inform
> a purchase.

Blurb language follows the **book's own** original language — don't translate.

---

## Step 4 — Check the series

If the book belongs to a series, check whether a series page should exist per
`domains/books/agents-domain-books.md`:

**2+ published volumes AND your entry point is `to-read`, `reading`, or `read` rated 4+.**

Match on the **normalized** series name — case-insensitive, leading "The " stripped. Sources
tag the same series inconsistently ("Expanse" / "The Expanse"), which silently splits one
series into two pages.

---

## Step 5 — Write the pages

Three writes, and **the second is the one that gets forgotten**:

**5a. Candidate page** — `wiki/books/candidates/<book-slug>.md`

`type: candidate`, `author`, `year`, `status: to-read`, `source`. Sections: `## Summary` (the
blurb), `## Source` (**quote what was actually said**, not a paraphrase),
`## Why You'll Like It` (a stub — see Step 6).

**5b. Author page row** — find or create `wiki/books/authors/<author-slug>.md`, add a `to-read`
row to `## Books`, and put the blurb in `## Standalone Blurbs` (or on the series page if one
qualifies).

> **This is the easiest step in the domain to miss.** A to-read book not in a qualifying series
> needs its blurb written in **two** places. In the wiki this came from, an enrichment pass
> skipped the author-page write for to-read books and silently left **45 books** showing
> "*Blurb pending.*" on the author page while the candidate page had the real text.

No `## Summary` on a new author page while they have only one book — and **never a
placeholder.** Real content or no section.

**5c. Series page** — only if Step 4's condition holds. Blurbs **move** there; they're never
copied. Verify the author page no longer carries it.

---

## Step 6 — Leave the ranking alone

`## Why You'll Like It` stays a stub unless you have an actual ranking mechanism — a taste
profile, a scoring model, something with a basis.

**Don't hand-write a rationale ahead of one.** An invented justification reads exactly like a
computed one and will be trusted the same way.

---

## Step 7 — Post-flight

1. Update the books indexes — authors, series, candidates.
2. Append to `wiki/log/log.md` **only if a genuinely new author, series or candidate page was
   created**. An added row on an existing author page is not a wiki-structural event.

---

## Reporting

State plainly: collision or new; which pages were created versus updated; whether the blurb was
fetched or stubbed, and from where.
