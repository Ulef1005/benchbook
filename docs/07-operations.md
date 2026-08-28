# Operations

Three named operations cover essentially everything you do with the wiki. They're defined in
the contract as ordered steps, which matters more than it sounds: a named operation with a
fixed sequence is repeatable across sessions and across model versions, where "help me file
this" is not.

| Operation | What it's for | Trigger |
|---|---|---|
| **INGEST** | Get something *into* the wiki | a URL, a file, or a conversation |
| **QUERY** | Get something *out* of it | a question |
| **LINT** | Check the whole thing for drift | manual, periodic |

---

## INGEST

The one you'll use most. Input is anything — a YouTube video, a PDF, an article, a photo, or
just a decision you made out loud in chat. Output is one or more properly-filed pages.

It runs in three parts, and the split exists because the middle part varies by subject while
the outer two never do.

### Pre-flight (always the same)

1. **Read the source.** The actual file or URL, not a summary of it.
2. **Propose a domain.** The agent suggests where this belongs and *waits for confirmation*.
   This is the single highest-leverage checkpoint in the system — almost every later mistake
   traces back to a wrong domain call here.
3. **Read that domain's rules file.** The satellite, loaded now that it's known which one.
4. **Extract the source URL** if there is one, so the page can link to the original rather
   than to a local copy that will later be archived.
5. **Discuss the key takeaways** with you, in chat, before writing anything.
6. **Read the page-conventions satellite** before creating a single file.

Steps 2 and 5 are where a human actually earns their keep. Everything after is mechanical.

### Dispatch (varies by domain)

Each domain defines its own ordered flow. The common shape, used by most:

```
source page  →  propose entity pages  →  two-way link  →  flag reference updates
```

- The **source page** captures what the material said.
- **Entity pages** capture the things it was *about* — a tool, a product, a technique, a
  person. These are proposed, not created; you approve them.
- **Two-way linking** is enforced: the entity records the source in frontmatter, the source
  body links to the entity. One-directional links rot invisibly.
- **Comparison pages are flagged, never auto-updated.** If a new source affects an existing
  comparison, the agent tells you and offers options rather than silently editing it.

Other domains have entirely different flows — a recipe gets confirmed against a category and
written in a structured format; a book gets checked against the existing library before
anything is filed. The dispatch table in the contract routes to the right one.

### Post-flight (always the same)

1. **Flag contradictions** against anything already in the wiki.
2. **Update the domain index** — the catalogue file that makes the new page findable.
3. **Update the overview** if the big picture actually shifted (usually it hasn't).
4. **Append one short line to the log**, but only if a page was created or a source ingested.
5. **Report** what was created, what was updated, and what was flagged.

---

## QUERY

Answering a question from the wiki, with the important constraint that the agent must be
honest about where the answer came from.

The sequence:

1. **Read the master index**, then the relevant domain index. These are the map — the agent
   does not go hunting through the file tree, and it does not preload them at session start
   either. They're read at the point of use.
2. **Read the actual pages** the index points at.
3. **Synthesise, with links.** Every claim traceable to the page it came from.

Then the part that keeps it trustworthy:

> If the wiki is insufficient, fall back to the raw sources, then to general knowledge —
> **and always disclose when the answer did not come from the wiki.**

Without that rule you get a system that sounds equally confident whether it's reporting your
own recorded decision or improvising from training data. Those are very different kinds of
answer and you need to be able to tell them apart at a glance.

QUERY is also the one operation whose *occurrence* is worth logging. A question you asked and
answered is genuinely new information — git history can't reconstruct it, because nothing
changed on disk.

**Offer to file good answers.** If a query produced a substantial, reusable synthesis, it
should become a page. Otherwise you'll answer it again in four months.

---

## LINT

The maintenance pass. Manually triggered, never automatic.

It's split by what kind of judgement each check needs:

**Mechanical checks run as a plain script.** Missing or malformed frontmatter, files whose
declared type doesn't match their folder, broken relative links, template sections missing
from page types that require them, orphaned pages absent from any index. Deterministic,
fast, cheap, and runnable on every commit. No model involved.

**Judgement checks run as the model.** Is this entity in the right folder given what it
actually is? Do these two pages contradict each other? Is this page stale — does it describe
a state of the world that later pages have superseded? These genuinely need reading
comprehension, and they're where a linting agent adds something a script can't.

**The output is a dated report and nothing else.** As covered in
[11 — Keeping It Honest](11-keeping-it-honest.md), LINT does not edit page bodies or
frontmatter. Its only write permissions are two file-moving operations that never delete:
archiving old raw sources, and archiving the oldest log entries when the log gets too long.

Run it every few weeks. The interesting output is rarely the broken links — it's the
staleness and contradiction findings, which are how you discover that two parts of your wiki
have quietly stopped agreeing.

---

## What this looks like in practice

A real short session:

```
You:    ingest https://example.com/some-article
Agent:  [reads it] This looks like knowledge/tooling. Confirm?
You:    yes
Agent:  [reads domain rules] Key takeaways: ... Worth noting the third
        point contradicts what's on your existing page for X.
You:    good catch, the new one's right
Agent:  Proposing: 1 source page, 2 entity pages (A, B). A already
        exists — I'd update it and note the contradiction. Create B?
You:    yes, but B belongs under projects not knowledge
Agent:  [creates, links both ways, updates index + log]
        Created: source page, entity B. Updated: entity A (contradiction
        noted). Flagged: comparison page C may need revising.
```

That correction in the middle — *"B belongs under projects"* — is the loop that matters. If
you find yourself making the same correction twice, it belongs in the contract as a rule.
That's how the contract gets tuned to you, and it's the mechanism by which this stops being
someone else's schema.

---

**Next:** [08 — Logs](08-logs.md), or back to [02 — The Contract](02-the-contract.md).
