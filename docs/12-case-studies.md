# Case Studies

Four things built and tracked with this system. They're here to show what the wiki actually
*did* during the build — not to showcase the builds themselves.

Each one illustrates a different part of the system doing work: recording how something is
wired, recording a decision to stop, changing the schema to fit a new subject, and — the most
valuable one — recording a failure honestly.

---

## 1. A daily two-host podcast

**What it is.** An on-demand morning-commute podcast with two recurring hosts and an off-mic
producer. Calendar, health metrics, weather and news feeds are gathered, scripted by an LLM,
voiced with TTS, and published to a private feed. Triggered with a one-word chat command;
ready by the time you're in the car.

**What the wiki did.** This build touches six systems — an automation platform, a health data
store, a weather source, a news pipeline, a TTS provider, and a podcast feed. The failure
mode for something like this isn't building it, it's *touching it eight months later*. Which
of those six is the flaky one? Where does the script template live? Why is one voice
configured differently from the other?

The project page carries the wiring, the phases as they were completed, and the decisions —
including the TTS history, which is the part worth showing. One provider was adopted and then
replaced, because the replacement supported multi-speaker audio in a single API call and
thereby deleted an entire audio-stitching step. A second, better-known provider was evaluated
and rejected on a specific measurable ground: its dialogue mode was *more* length-constrained
than the incumbent, not less.

And then the detail that justifies this whole system. The chosen API accepts **exactly two
speakers** — three returns a hard error, verified live against two different model versions.
That constraint is why the show has two voiced hosts and a third character who is constantly
quoted but never speaks. A creative format decision, driven entirely by an API limit.

Nobody would ever reconstruct that. It looks like a writing choice. Eighteen months later,
someone — including you — will propose adding a third voice, and the page answers in one line
with the error message and the date it was verified.

**The transferable bits:** first, when a build finishes, its record should fork — a frozen
project page for how it came to be, a living entity page for what it currently is. Second, the
constraints that shaped a design are worth more than the design, because the design is visible
in the artifact and the constraints are not.

---

## 2. A used-marketplace buying assistant

**What it is.** You describe what you're hunting for. It establishes a price baseline from a
comparison site plus twelve months of its own archived observations, picks up new classifieds
listings hourly, pulls the full text, scores each against your criteria with an LLM, and
pushes anything above threshold to chat — with a why-now justification and a drafted message
to the seller.

**What the wiki did.** Two things worth reporting.

First, **it generalised a skill out of a project.** The cold-start problem — "what *is* a fair
used price for this?" — recurred across several buying projects. That got extracted into a
reusable market-survey skill that any future buying project can invoke, rather than being
re-derived by hand each time. The wiki noticing a repeated pattern and promoting it to a skill
is a recurring move; see [10 — Skills](10-skills.md).

Second, and more usefully: **it recorded a decision to stop.** V1 shipped and runs. The V2
plan — eight further phases, fully specified — was paused, because the whole concept needed
rethinking and the specifics weren't clear yet. That is written on the page, with the date and
the reason, and the eight unbuilt phases are still there.

This is the thing a git history can't give you. Git shows no commits since July. It cannot
tell you whether that's because the project is finished, abandoned, blocked, or waiting on a
decision — and those demand completely different responses when you come back to it. "Paused
2026-07-13, concept needs a refactor, specifics TBD" answers in one line what a year of
commit archaeology would not.

**The transferable bit:** record *why work stopped*, always. Silence is ambiguous and the
ambiguity is expensive.

---

## 3. A book recommendation pipeline

**What it is.** Recommendations arrive from everywhere — a social post, a screenshot, a
podcast mention, a friend. The system captures them, checks each against an existing
~350-book library across four shelves (read, reading, abandoned, to-read), and either reports
a collision ("you read this in 2019") or scores it against a taste profile and files it as a
ranked candidate. It reads book titles out of carousel images, because that's where
recommendations actually live now.

**What the wiki did.** This is the case where **the schema itself changed**. Books didn't fit
the existing page types cleanly: a series is not an entity, a book you might read is not the
same kind of thing as a book you have read, and an author needs a table of their works rather
than prose.

So the books domain got three new page types — series, author, and candidate — with the
candidate type carrying scoring fields that no other page type in the wiki has. That schema
extension was proposed by the agent, argued about, approved, and written into the contract
with its date and rationale. Then a 335-book import ran against the new schema.

The important part is that this was a *negotiated* change to a shared contract, not the agent
improvising new conventions mid-import. Without the approval gate you'd have discovered the
new page types afterwards, in whatever shape seemed reasonable at the time, applied
inconsistently across 335 files.

**The transferable bit:** the schema is allowed to grow for a subject that genuinely doesn't
fit — but through proposal and approval, not improvisation.

---

## 4. A health data store, and a model that didn't work

**What it is.** Wearable and training-platform data aggregated into a governed local store —
a custom provider for one training platform, another for a watch vendor's API, roughly 245,000
samples across a seven-year backfill, running in containers with scheduled collection jobs.
On top of it, a coaching layer producing weekly reports and early-warning detection.

**What the wiki did.** This is the best example in the repo, and it's the one where the answer
was *no*.

A companion project set out to build a personalised physiological model that would forecast
race performance from training load. It was well-specified, well-motivated, and it **did not
validate**. The fitted model explained almost none of the variance in-sample. The fatigue term
turned out to be structurally unidentifiable given the available data — the athlete only ever
races well-rested, so there is no observation of racing while fatigued for the model to learn
from. A deliberate data-densification effort, adding several hundred more runs, found the
signal was real but weak: a marginal improvement in out-of-sample skill, nowhere near enough
to justify the original claim.

All of that is on the project page. The negative result, the numbers, the specific reason the
model was unidentifiable, and the decision that followed: re-scope from *predictive* to
*descriptive*, and ship the parts that did work — the daily tracking engine and an
interpretation guide — while explicitly retiring the forecasting goal.

Two things this buys, permanently:

1. **Nobody rebuilds it.** In two years, when "I should build a model that predicts race
   performance from training load" occurs again — and it will, because it's a good idea — the
   wiki answers with the numbers, and the specific structural reason it can't work with this
   data. That's an afternoon saved every time, forever.
2. **It stays honest.** There is real pressure, when a project fails, to quietly re-describe
   what you built as what you meant to build. Writing the negative result down with its
   numbers, at the moment it happens, is the mechanism that prevents that.

**The transferable bit:** the failures are the highest-value pages in the wiki. They're also
the ones you're least inclined to write, which is exactly why the agent should be the one
writing them.

---

## The through-line

None of these are about the wiki being clever. They're about four unglamorous properties:

- The reasoning was written down **at the moment it happened**, not reconstructed later
- **Stopping** was recorded as deliberately as starting
- The schema **grew when reality demanded it**, through approval rather than drift
- **A negative result survived** in the form it actually happened in

The agent did the writing. The human made the calls. That division is the whole system.

---

**Next:** [13 — Privacy](13-privacy.md), or back to the [README](../README.md).
