# Architecture

Three layers, plus a code store. The layering exists to answer one question at all times:
**who is allowed to write here?**

```
raw/                    ← you write. The agent reads and never modifies.
wiki/                   ← the agent writes. You read (and correct).
scripts/                ← code that isn't a deployed service.
agents-core.md          ← co-owned. Agent proposes, human commits.
```

Get that ownership map wrong and the system fails in a specific way: you stop trusting the
wiki, because you can no longer tell which parts you asserted and which parts the agent
inferred.

---

## `raw/` — the immutable layer

Source material as it arrived. Articles, transcripts, PDFs, images, exports.

**The agent never modifies anything here.** This is a hard rule, and it's the reason you can
always re-derive the wiki if you decide the schema was wrong. If the agent could edit sources,
an error introduced during ingestion would be indistinguishable from the source itself, and
your ground truth would quietly become a copy of the agent's understanding.

There is one exception, and it's mechanical rather than editorial: the lint pass may **move**
raw files older than 14 days into an archive folder. Nothing is ever deleted.

Two related rules that look fussy and aren't:

- **Page bodies never link to a raw path.** Body links point at the original online URL. The
  local path lives in frontmatter only. Because raw files get archived, a body link to one is
  a link that will break — and a page full of dead links trains you to stop clicking links.
- **Sources embed their content.** A source page carries the full transcript or text inline,
  not just a link. The wiki stays readable when the original URL rots, which it will.

---

## `wiki/` — the agent-owned layer

Generated markdown. Summaries, entity pages, projects, indexes, logs. The agent creates and
maintains all of it; you read it, correct it, and approve what gets created.

The important property is that this layer is **derived but authoritative**. Derived, because
everything in it traces back to a source or a conversation. Authoritative, because it's what
you and the agent actually consult — nobody re-reads the raw material once it's been ingested.

That's the compounding artifact, and it's the whole point: the synthesis is done once and kept
current, rather than re-derived on every question.

---

## The schema layer

`agents-core.md` plus its satellites. Covered in full in
[02 — The Contract](02-the-contract.md). Structurally, the thing to note is that it's the only
**co-owned** layer: the agent proposes changes, a human commits them.

That makes it the one place where the system's own rules have a version history, which turns
out to matter more than expected. "Why is this rule here?" is answered by the commit that
introduced it and the mess that prompted it.

---

## `scripts/` — the code store

A split by *what the code is*, which is less obvious than it sounds and worth copying.

**Code that is not a running service** lives in the wiki repo: lint tooling, git hooks,
per-project build recipes, firmware source whose deployed form is a separate artifact. Each
project's subfolder carries a README linking back to its wiki page, and the wiki page links
forward to the files. Two-way, always.

**Code that is a continuously-running deployed service** lives in a separate infrastructure
repo, where the on-host path *is* the git working tree. This is the important half. If your
repo is a *copy* of what's running on a server, the copy rots — someone applies a fix in the
field at 11pm, it works, and the repo silently no longer describes reality. Making the
deployed path a live checkout means a field hotfix is a real commit rather than a divergence
waiting to be discovered.

The corresponding hard rule: **deployed code must be committed before the session ends.** A
live checkout is not an auto-committing daemon.

Two conventions on the code store that prevent predictable pain:

- **Faithful copies only.** Byte-for-byte, no added headers or helpful reformatting. The
  moment a stored copy differs cosmetically from the original, diffing them stops being
  useful.
- **No secrets.** Only indirection — environment variables, secret references, a vault
  lookup. This matters more in a wiki than a normal repo, because the wiki's whole purpose is
  to be comprehensive, and comprehensiveness is exactly the instinct that leads to pasting a
  working config with a token in it.

---

## Why git, specifically

The wiki is a git repo of markdown files, which buys several things for free:

- **History of the content**, so you can see when a page's claim changed
- **History of the rules**, which is half their value
- **Diff review** — you can read what the agent changed before you accept it
- **Sync and backup** with no bespoke machinery
- **Recovery** when the agent does something wrong at scale, which it eventually will

That last one is the real argument. Every safeguard in this system assumes the agent will
occasionally be confidently wrong across many files at once. Git is what makes that
recoverable rather than catastrophic, and it's why "just use a database" is the wrong trade
here.

---

**Next:** [04 — Domains](04-domains.md).
