# raw/ — immutable source material

Drop source material here: saved articles, transcripts, PDFs, images, exports.

**The agent reads from this folder and never modifies it.** That's Hard Rule 3, and it's what
lets you re-derive the wiki if you later decide the schema was wrong. If the agent could edit
sources, an error introduced during ingestion would be indistinguishable from the source
itself — and your ground truth would quietly become a copy of the agent's understanding.

## The one exception

LINT may **move** files older than 14 days into `_archived/<domain>/`. It never deletes them.

That archival is why two related rules exist:

- **Page bodies never link to a `raw/` path.** Body links point at the original online URL;
  the local path lives in frontmatter as `raw_file:`. A body link to an archived file is a
  link that will break, and a page full of dead links teaches you to stop clicking links.
- **Source pages embed their content.** A source page carries the full transcript or text
  inline, so the wiki stays readable when the original URL rots — which it eventually will.

## You don't always need this folder

Plenty of ingests start from a URL or from a conversation, with nothing ever landing here.
`raw/` is for material you want a durable local copy of.
