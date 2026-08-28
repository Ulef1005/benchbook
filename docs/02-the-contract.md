# The Contract

Everything else in benchbook is downstream of one file.

`agents-core.md` sits at the repo root. The agent reads it at the start of every session,
before it does anything else. It is the operating contract: what the agent may create, what
it must ask about first, what it is never permitted to touch, and where to find the detailed
rules when it needs them.

If you take one idea from this repo, take this one. Skills without a contract are just
disconnected prompts that each re-invent your conventions slightly differently.

---

## Why a file, and not a system prompt

Three properties matter, and a file has all of them:

**It's versioned.** The contract lives in git alongside the wiki it governs. When a rule
changes you can see when, and the commit sits next to the mess that caused the change. Half
the value of the contract is its own history.

**It's inspectable.** You can read the rules your agent is following. When it does something
surprising, the explanation is in a file you can open, not in a hidden preamble or a vendor's
memory feature.

**It's portable.** It survives model upgrades, tool changes, and starting a fresh session. It
is not tied to any provider's persistence mechanism.

There's a fourth, less obvious one: **a file can be argued with.** The contract is co-owned —
the agent proposes changes to it, and only a human commits them. That turns the schema into a
negotiation with a record, rather than something that drifts silently as the agent improvises.

---

## What's in it

The contract is short by design. Roughly:

```
1. Session Start        — read this file; how to greet; what NOT to preload
2. Hard Rules           — the non-negotiables, numbered
3. Operations           — INGEST / QUERY / LINT, each as ordered steps
4. Architecture         — the folder layers and what owns what
5. Page Conventions     — pointer to the satellite file
6. Index / Log / Todo   — what goes where, and explicitly what doesn't
7. Domain Rules         — pointer to the per-domain satellites
8. Reference            — connection details, standing facts
```

The Hard Rules section is the load-bearing part. They're numbered so they can be cited in
conversation ("that's Hard Rule 13"), and they're phrased as absolutes. A sample of the ones
that earn their place:

- **Never modify the raw source folder.** Ingested material is immutable. The lint pass may
  *archive* old files after 14 days; nothing deletes them.
- **Always include frontmatter, `publish: false` by default.** Private unless deliberately
  made otherwise.
- **Flag contradictions explicitly — never silently overwrite conflicting information.**
  When new input disagrees with what's on a page, the agent surfaces both and asks.
- **Ask before creating pages.** During an interactive session the agent proposes; the human
  approves.
- **Propose changes to this file — don't modify the schema silently.**
- **The No-Deletion Rule.** Before deleting a file or dropping content during a rewrite, the
  agent must stop and ask: *"about to discard X, which contains Y — does it belong somewhere
  else?"* This applies to migrations, to content that doesn't fit the target page, and to
  links that would break.

Notice how many of these are about *restraint*. That's the pattern. An agent with file-write
access and good intentions will helpfully reorganise your knowledge base into something you
can no longer navigate. Most of the contract exists to prevent enthusiasm.

---

## The satellite pattern

The obvious failure mode of a contract file is that it grows. Every convention you codify
makes it longer, and it's read at the top of every session, so length is a tax on every
single conversation you have.

benchbook solves this by splitting on **load frequency**:

```
agents-core.md              ← always read. Structure, hard rules, dispatch table.
├── agents-page-conventions.md   ← read before creating or editing any page
├── agents-lint-checks.md        ← read only when running LINT
└── agents-domain-<name>.md      ← read only when working in that domain
```

The core file doesn't restate what's in the satellites. It says *which* satellite to read and
*when*. So the always-loaded cost stays roughly constant while the total ruleset grows
without limit — the per-domain files can be as detailed as they need to be, because nobody
pays for the cooking rules while working on the homelab.

This is a context-budget technique more than a documentation one, and it generalises well
beyond wikis. The rule of thumb: **anything read every session belongs in the core file;
anything read conditionally belongs behind a pointer.**

The core file explicitly instructs the agent *not* to preload the indexes, for the same
reason. They're read at the point of use, by the operation that needs them.

---

## How it evolves

The contract changes when reality proves it wrong, and the change gets recorded with its
cause. In practice the cycle is:

1. Something goes wrong or drifts — usually noticed during a lint pass.
2. The agent reports it and proposes a schema change.
3. The human accepts, modifies, or rejects it.
4. The new rule goes in with a dated note explaining what it's fixing.

That last step is what makes the file worth re-reading later. A rule like *"`update` is
deliberately **not** a valid log operation"* is unhelpful on its own and obvious once it
carries its reason: it was the escape hatch that made the log grow ten times faster than
intended, and here are the audit numbers.

See [11 — Keeping It Honest](11-keeping-it-honest.md) for the full set of rules that came out
of failures, and the data behind them.

---

## Adapting it

Fork the contract and change it. It is not a standard, and roughly a third of it encodes
decisions specific to one person's setup.

What to keep:

- Session-start read, and the greeting (it's how you confirm the contract actually loaded)
- The hard-rules section, especially the restraint rules — ask before creating, never
  silently overwrite, no deletion without asking
- The satellite split
- The operations as ordered, named steps

What to replace:

- The domain list — yours will differ, and should
- Anything in the Reference section
- The page-length thresholds, once you know your own writing

What to add early:

- Any rule you find yourself repeating to the agent twice. That repetition *is* the signal.

---

**Next:** [03 — Architecture](03-architecture.md) covers the folder layers the contract
governs, and why the raw layer is immutable.
