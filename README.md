<p align="center">
  <img src="assets/readme-banner-light.png" alt="benchbook" width="100%">
</p>

<p align="center"><strong>Your AI keeps the wiki. You keep the rules.</strong></p>

*TL;DR: benchbook is a plain-markdown wiki, versioned in git, that an AI agent reads and
writes under a written contract — what it may create, what it must ask about, what it can
never touch. Works with any agentic tool that can read and write files in a repo, not just
one assistant.*

You build something with an LLM on a Tuesday. It works. Three months later you open the
folder and have no idea why you chose that library, what the two rejected approaches were,
or which of the four config files is the live one. The code survived. The reasoning didn't.

benchbook is the system I use to fix that: a plain markdown wiki, in git, maintained by an AI
agent under a written contract — a file the model reads at the start of every session that
tells it what it may create, what it must ask about, and what it is never allowed to touch.

It is not tied to any one assistant. Any agentic tool that can read and write files in a repo
can run it.

No app. No database. No embeddings. Just files an agent is disciplined about.

---

## See it work

The fastest way to understand this is to watch it handle three ordinary tasks. Each one is
walked step by step in [**A Day in the Life**](docs/day-in-the-life.md):

> **🔧 You saw a funky ESP32 project on YouTube and want to build it.**
> The video becomes a source page with the transcript embedded. The *build* becomes a separate
> project page — and nothing gets written until you've approved a plan. Eight months later,
> when the display goes blank, the pinned library version and the reason it's pinned are one
> click away.

> **🤖 You want a self-hosted Telegram bot, but don't know which repo to use.**
> Research four candidates, record why the most popular one lost, then deploy with the seven
> boring integration steps pre-filled and unticked so none of them get skipped. The bot token
> never touches the wiki. When the framework ships a major version, release tracking tells you.

> **🚁 You want to learn to fly FPV drones.**
> Not software at all. A learning path with gates between phases, a price baseline before you
> shop, and — the valuable part — every gear option you *rejected*, with your reasoning, dated.
> So when someone enthusiastically recommends the goggles you already ruled out, you know why.

Each example names the command that runs, what you decide versus what the agent does, and
exactly what ends up written down.

---

## The problem it actually solves

Building with an LLM is fast, and that speed is the trap. You produce more decisions per week
than you can remember, and none of them write themselves down. Six months of that leaves you
with a homelab, a pile of scripts, and a strong suspicion that past-you had reasons.

What you want to recover later is rarely the code — it's:

- **How** was this built (which stack, which wiring, which files are live)
- **When** was it built, and what has changed since
- **Why** was it built that way — including the options that were considered and dropped

A README in each project captures the first. Git captures the second. Almost nothing captures
the third, and the third is the one you actually miss.

benchbook captures all three as a side effect of working, because the agent that helps you
build is the same agent that files the record.

---

## Lineage

This is an instantiation of Andrej Karpathy's
[LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern — a
deliberately abstract "idea file" describing three layers (immutable raw sources, an
LLM-owned wiki, a co-evolved schema file) and three operations (ingest, query, lint). It
closes by saying the directory structure, schema conventions, page formats and tooling "will
depend on your domain, your preferences, and your LLM of choice," and invites you to build a
version that fits.

benchbook is what that turned into after six months of daily use. The three layers and the
three operations survived unchanged — they're right. Most of this repo is the specifics the
gist deliberately left open, plus the rules that turned out to be necessary past the scale it
scopes for.

What got added along the way:

| Addition | Why |
|---|---|
| **Domains** as a first-class concept | One flat wiki stops being navigable somewhere in the low hundreds of pages |
| **A split index** | The gist notes a single index works well at "~hundreds of pages." This one is at 1,563; the index is now one small master file plus a catalogue per domain |
| **Page types with templates** | source / entity / reference / project, each with required frontmatter and a placement rule |
| **Projects** | The gist's examples are research, reading, and business. Tracking things *you are building* — phases, rejected options, status — is a different shape and needed its own page type |
| **Human approval gates** | The gist mentions humans-in-the-loop only for the team case. In personal use they turned out to be the thing that keeps the wiki trustworthy |
| **Anti-bloat discipline** | See below — this is where experience actually contradicted the theory |

### The one place six months disagreed with the gist

The gist's argument for why this works is that humans abandon wikis because the maintenance
burden grows faster than the value, and LLMs fix that because they don't get bored and the
cost of maintenance falls to near zero.

That's true, and it creates a second problem the gist doesn't anticipate: **when maintenance
costs nothing, you get too much of it.** The failure mode in practice was never a neglected
wiki. It was a wiki growing faster than anyone could read — logs filling with narrative that
already existed on a project page, lists mirroring state that then drifted, pages accreting
past the point of usefulness. Boredom was never the enemy. Enthusiasm was.

So a real chunk of the contract exists to make the agent write *less*, in more specific
places. The numbers behind those rules are in
[11 — Keeping It Honest](docs/11-keeping-it-honest.md), and they're the part of this repo I'd
read first.

---

## What it is, concretely

Five moving parts, all of them text:

| Part | What it does |
|---|---|
| **The contract** (`agents-core.md`) | Read at every session start. Hard rules, page conventions, what needs human approval. The agent proposes changes to it; it never edits it silently. |
| **Domains** | Top-level subject areas, shipped as installable **packs** — rules, skills and page types bundled per subject. Three installed by default (`knowledge`, `home`, `projects`); `books` and `cooking` available. |
| **Page types** | `source`, `entity`, `reference`, `project` — each with a template and required frontmatter. |
| **Indexes** | Per-domain catalogue files the agent reads *before* answering. This is the retrieval layer. There is no vector store. |
| **Skills** | Packaged procedures for the recurring operations: ingest a source, start/open a project, lint the wiki, close a session. Your tool may call these skills, commands, prompts, or rules. |

The agent plays three roles against that structure — **Librarian** (files what comes in),
**Advisor** (answers from what's filed), **Project Manager** (tracks what's in flight).

---

## Rules that exist because something broke

Running since May 2026, currently **1,563 pages across 9 domains** with **16 skills** and a
log going back to the first week. The useful output of that isn't the page count — it's the
rules that are in the contract today only because the obvious version failed in practice:

- **`update` was removed as a valid log operation.** An audit found 17 of 26 recent entries
  were `update`, averaging 139 words against a 1–3 line spec, mostly duplicating text already
  written on a project page in the same session. The log was growing ~10× faster than intended.
- **The central todo file stopped mirroring project todos.** 60 of ~76 mirrored items had
  silently drifted from the pages they were copied from. It's now pointer-only.
- **The "split pages over ~500 words" rule was made measurable**, with explicit carve-outs,
  after it turned out 27% of all pages breached it — a rule that flags a quarter of your
  content steers nothing.

Anyone can write a schema. The interesting part is which parts of it survived contact with
six months of real use, and that is most of what the docs in this repo are about.

---

## Things built with it

Not demos — these run:

- **A daily two-host podcast.** Calendar, health metrics, weather and news → script → TTS →
  a private feed, generated on demand for the morning commute.
- **A used-marketplace buying assistant.** Hourly listing pickup, scored against
  project-specific criteria by an LLM, high matches pushed to Telegram with a drafted
  seller message and a price-history baseline.
- **A book recommendation pipeline.** Captures recommendations from social posts and
  screenshots, collision-checks them against a ~350-book library across four shelves,
  and ranks what's left against a taste profile.
- **A self-hosted health data store.** Wearable providers into a governed local store,
  feeding a coaching layer with weekly reports and early-warning detection.

Each one has a project page recording its phases, its rejected options, and — in two cases —
an honest post-mortem on the parts that didn't validate.

---

## Quickstart

Requires an agentic tool that can read and write files in a repository — [Claude Code](https://claude.com/claude-code),
Codex, Cursor, or similar. No install script, no dependencies.

```bash
git clone https://github.com/Ulef1005/benchbook.git my-wiki && cd my-wiki
```

Then:

1. **Read `agents-core.md`** — it's the contract. It's meant to be edited; it's yours now.
2. **Look at the demo content**, then delete it. `wiki/DEMO.md` says what each page
   demonstrates and gives you the one-line removal command. Keep the folder shape.
3. **Live on the three installed domains for a while.** `knowledge`, `home` and `projects` are
   the minimum set that makes the placement rules work. Add a fourth when you reach for it and
   it isn't there.
4. **Start your agent in the repo** and say *"read agents-core.md"*. It will greet you and
   wait. (`CLAUDE.md` and `AGENTS.md` both point at the contract, so most tools pick it up
   without being asked.)
5. **Ingest one thing** — an article, a video, a decision you already made — with
   `/wiki-ingest`. Watch where it files it and correct it. That correction is how the
   contract gets tuned to you.

Then read [**A Day in the Life**](docs/day-in-the-life.md), which walks three real tasks end
to end — it'll make the rest of the docs land faster than reading them in order.

---

## Documentation

[**A Day in the Life**](docs/day-in-the-life.md) — the three worked examples from the top of
this page, in full. Start here if you haven't already; the numbered docs below are the
reference material behind it.

| Doc | What's in it |
|---|---|
| [01 — Concept](docs/01-concept.md) | The problem in depth, the lineage, why not Notion/Obsidian/RAG |
| [02 — The Contract](docs/02-the-contract.md) | `agents-core.md`, session start, hard rules, the satellite-file pattern |
| [03 — Architecture](docs/03-architecture.md) | `raw/` → `wiki/` → `scripts/`, immutability, git as the substrate |
| [04 — Domains](docs/04-domains.md) | What a domain is, the special ones, and the nine in real use |
| [05 — Page Types](docs/05-page-types.md) | source / entity / reference / project, frontmatter, the Entity Placement Rule |
| [06 — Indexes](docs/06-indexes.md) | How retrieval works with no embeddings |
| [07 — Operations](docs/07-operations.md) | INGEST, QUERY, LINT |
| [08 — Logs](docs/08-logs.md) | How logs work and why they carry the orientation load |
| [09 — Projects](docs/09-projects.md) | The project page, its template, the status lifecycle |
| [10 — Skills](docs/10-skills.md) | The core six, plus two showing more advanced patterns |
| [11 — Keeping It Honest](docs/11-keeping-it-honest.md) | Anti-rot rules, the failure data behind them, human approval gates |
| [12 — Case Studies](docs/12-case-studies.md) | The four builds above, in detail |
| [13 — Privacy](docs/13-privacy.md) | `publish: false`, and sanitising a personal wiki before sharing |
| [14 — Limits](docs/14-limits.md) | What it's bad at, honestly |

---

## Status

Early. The system is mature; this repo's packaging of it is not. Expect the docs to land
before the demo content does.

## License

MIT.
