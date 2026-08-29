# The Concept

## The actual problem

Building things with an LLM is fast. That speed is the whole point, and it's also the trap.

In a normal week you might pick a library, reject two alternatives, discover a firmware
quirk, decide a service should run on one machine rather than another, and change your mind
about a schema. Six of those decisions are load-bearing. None of them write themselves down.
The conversation where you reasoned it out scrolls away, and what survives is an artifact
that works for reasons you can no longer reconstruct.

Three months later you open the folder and you can see *what* exists. What you've lost is:

- **How** it's actually wired — which of these four config files is live, what depends on what
- **When** things changed, and what the state was before
- **Why** it's like this — the constraint that ruled out the obvious approach, the thing you
  tried first that didn't work

The third one is the expensive loss, and it's the one nothing captures by default. Git tells
you *when* and *what changed*. A README tells you *how* if you kept it current. The reasoning
lives only in a chat transcript, which is to say it may as well not exist.

The cost isn't nostalgia. It's that you re-litigate settled decisions, re-try approaches you
already rejected for good reasons, and slowly lose the confidence to change anything, because
you can't tell which parts of the design were deliberate and which were accidents.

---

## Why the obvious solutions don't hold

**"Just write it down."** Everyone knows this. Nobody sustains it. The maintenance burden of a
hand-written wiki grows faster than its value, which is why personal wikis are abandoned at a
roughly 100% rate. The bookkeeping — updating cross-references, revising a summary because a
newer source contradicts it, keeping an index current — is exactly the work humans won't do
and won't miss doing.

**Notion, Obsidian, a folder of markdown.** These are good places to *put* knowledge and do
nothing about the fact that you have to produce it. The tool was never the bottleneck.

**RAG, NotebookLM, "chat with your files."** You upload documents and the model retrieves
chunks at query time. This works, and it doesn't accumulate. Every question re-derives the
answer from raw material; nothing is ever built up. Ask something that needs five documents
synthesised and the model does that synthesis fresh, every time, and then throws it away.
Contradictions between sources are rediscovered or missed at random rather than being found
once and recorded.

**Project READMEs.** Capture *how*, sometimes. Go stale silently. Are per-project, so
anything cross-cutting — a decision affecting three projects, a piece of hardware used by two
— has no home.

**Chat history.** Contains everything and surfaces nothing. Search over transcripts returns
the moment you discussed a thing, not the conclusion you reached about it.

---

## The shape of the fix

The move, borrowed wholesale from
[Karpathy's LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f),
is to put a **persistent, compounding artifact** between you and your raw material.

When something new arrives, the agent doesn't index it for later. It reads it, extracts what
matters, and *integrates* it — updating the pages it affects, noting where it contradicts
what's already recorded, strengthening the synthesis. The work is done once and then kept
current, rather than re-derived on every question.

You rarely write the wiki. You do the parts that need a human — sourcing, judging, deciding,
asking the right question — and the agent does the bookkeeping that makes the whole thing
usable later.

Three roles, against the same structure:

| Role | What it does |
|---|---|
| **Librarian** | Files what comes in. Decides where it goes, links it up, flags what it contradicts. |
| **Advisor** | Answers from what's filed, with citations, and says clearly when the answer *isn't* from the wiki. |
| **Project Manager** | Tracks what's in flight — phases, open questions, decisions and the options they beat. |

That third role is where benchbook diverges most from the gist, whose examples are research,
reading, and team knowledge. **Tracking things you are building is a different shape** from
tracking things you are learning: it has state, it has a lifecycle, and its most valuable
content is the decision record — including the approaches that were considered and dropped,
which is precisely the thing nothing else captures.

---

## Why it's markdown in git, deliberately

No database, no app, no vector store. This is a choice, not a limitation:

- **Plain text outlives tools.** Any editor, any machine, any decade. Nothing to migrate off.
- **Git gives you history for free** — including the history of the rules themselves, which
  is half their value.
- **The agent reads and writes files**, which is the operation LLM tooling is best at. No
  integration layer to keep working.
- **You can read it without the agent.** Important on the day the agent is wrong.
- **Retrieval is an index file the model reads**, not an embedding pipeline you maintain.
  Below a certain scale this is simply better; past it, you split the index rather than
  reaching for vectors. See [06 — Indexes](06-indexes.md).

The corollary is that the interesting engineering isn't in the storage. It's entirely in the
*discipline* — the contract that governs what the agent may write, where, and when it has to
ask first. That's [02 — The Contract](02-the-contract.md), and it's the part worth stealing.

---

## Who this is for

**A good fit if** you build a lot of small things, you use an agentic coding tool daily, you
already have opinions about your own conventions, and your main frustration is losing the
reasoning behind decisions rather than losing the artifacts.

**A bad fit if** you want a turnkey app, you're not going to edit the contract (it's ~40%
personal decisions that should be replaced), or you want something that works without a human
in the loop. The approval gates are load-bearing, not training wheels — see
[11 — Keeping It Honest](11-keeping-it-honest.md).

---

**Next:** [A Day in the Life](day-in-the-life.md) — three worked examples showing all of the
above actually running. Or go straight to [02 — The Contract](02-the-contract.md) for the
mechanism.

Want the wiki itself readable somewhere other than a git client — a phone, a kitchen display?
See [15 — Publishing](15-publishing.md).
