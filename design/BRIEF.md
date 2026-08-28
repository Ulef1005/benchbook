# Design Brief — benchbook

Handoff for Claude Design. Everything needed to make the GitHub repo look like a real
project rather than a folder someone pushed.

---

## 1. What you're designing for

**benchbook** is an open-source system for keeping a personal wiki that an AI agent maintains
for you. Plain markdown files in git — no app, no database, no fancy UI. The AI reads a
written contract file at the start of every session that tells it what it may create, what it
must ask permission for, and what it must never touch.

The problem it solves: you build things with AI, fast, and three months later you have no idea
*why* you made the choices you made. The code survived; the reasoning didn't. benchbook
captures the reasoning as a side effect of working.

**Audience:** developers and technical hobbyists who use agentic coding tools daily. People
who build homelabs, ESP32 projects, self-hosted services. They are allergic to marketing
polish and will trust a design that looks *engineered* over one that looks *branded*.

**Where this lands:** a GitHub repository. That's the whole surface. No website (yet).

---

## 2. The name — this is the key to the logo

**"benchbook"** = the notebook you keep at the workbench. Where you write down what you did,
what broke, and what you'd do differently.

There's a second meaning worth mining, and it may be the stronger one:

> A **benchmark**, in surveying, is a permanent reference mark cut into stone — a fixed point
> of known elevation that everything else is measured against. It doesn't move. You come back
> to it.

That's exactly what this project is: fixed reference points you can return to. The traditional
British Ordnance Survey benchmark symbol — a horizontal bar with an arrow pointing up at it —
is geometrically simple, genuinely obscure, and carries precisely the right meaning.

Worth exploring seriously. It's distinctive in a category full of brain icons.

---

## 3. Personality

| It should feel | It should not feel |
|---|---|
| Engineered, measured, precise | Slick, startup-y, venture-funded |
| Workshop, bench, hand-tools | Corporate SaaS |
| Durable, plain-text, archival | Trendy, of-the-moment |
| Quietly confident | Loud or clever |
| A little bit analogue | Futuristic |

The tone of the writing it accompanies is dry, specific, and unimpressed with itself. The
design should match that. If it looks like it's trying to sell something, it's wrong.

---

## 4. Deliverables

### Essential

| # | Asset | Spec | Notes |
|---|---|---|---|
| 1 | **Primary mark** | Square, SVG, legible from 16px to 512px | The icon alone, no text |
| 2 | **Wordmark** | Horizontal lockup: mark + "benchbook" | For the README header |
| 3 | **Social preview card** | **1280 × 640 px**, PNG, under 1 MB | The one people forget. This is what renders when the repo link is pasted into Slack, X, or LinkedIn. GitHub → Settings → Social preview |
| 4 | **README hero banner** | ~1280 px wide, flexible height | Sits at the very top of the README |
| 5 | **Favicon set** | 16, 32, 180, 512 px PNG + SVG | For a future docs site |
| 6 | **Palette + type spec** | Hex values, font names, usage rules | So future assets stay consistent |

### Nice to have

| # | Asset | Notes |
|---|---|---|
| 7 | **Architecture diagram** | The three layers: `raw/` (immutable, you write) → `wiki/` (the agent writes) → the contract (co-owned). Currently an ASCII block in `docs/03-architecture.md` |
| 8 | **The loop diagram** | Capture → Decide → Execute → Close. Currently a table in `docs/day-in-the-life.md` |
| 9 | **Monochrome variant** | Single-colour version of the mark for stamps, watermarks, terminal-adjacent contexts |

Diagrams should be SVG, and must be readable in both GitHub light and dark themes.

---

## 5. Hard constraints

These are not preferences. Break them and the assets don't work where they need to work.

- **Light AND dark mode.** GitHub renders both, and readers are split roughly evenly. Either
  design a mark that survives both, or supply two variants — GitHub supports
  `<picture>` with `prefers-color-scheme` in READMEs.
- **Transparent background** on the mark. No baked-in white square.
- **Legible at 16 px.** The favicon test kills most detailed marks. If it needs more than
  three or four shapes, it's too complex.
- **Works in pure monochrome.** Test it black-on-white before adding any colour.
- **SVG for everything vector.** Repos are read on every kind of screen.
- **No text inside the mark itself.** The wordmark is a separate lockup.

---

## 6. Suggested directions

Three to explore. Not exhaustive — better ideas welcome.

### Direction A — The benchmark cut *(recommended)*

The surveyor's mark: a horizontal bar with an arrow pointing up into it. Abstract it into
something geometric and modern. Reads as a fixed reference point. Extremely simple, so it
survives the 16 px test easily, and the meaning rewards anyone who looks it up.

Risk: obscure. Most people won't get the reference unaided. Mitigate by explaining it in one
line in the README — which is itself a nice detail.

### Direction B — The ruled page

An open notebook or a ruled/graph-paper page, radically simplified — perhaps just the ruling
itself, with one mark that isn't a rule line. Says "notebook" instantly and speaks to
structure-plus-record.

Risk: notebook icons are common. Needs a genuinely distinctive execution to not look stock.

### Direction C — The bench

The workbench itself, reduced to its silhouette — a flat top and legs. Warm, hand-tools,
maker-adjacent. Pairs naturally with the "bench" half of the name.

Risk: can read as furniture, or as a park bench. Needs care.

**A combination is fine** — for instance, the benchmark arrow used as the one non-rule mark on
a ruled page.

---

## 7. Anti-brief — please avoid

This category is drowning in visual clichés. All of the following are disqualifying:

- 🧠 **Brains of any kind.** The project was deliberately renamed *away* from "second brain."
  A brain icon undoes that.
- **Neural networks, node-and-edge graphs, connected dots.** Every AI project uses these.
- **Glowing orbs, particle effects, "intelligence" auras.**
- **Robot faces or friendly robot mascots.**
- **Lightbulbs, sparkles, ✨, or magic-wand imagery.**
- **Purple-to-blue gradients.** The default AI palette; instantly generic.
- **Books rendered realistically** with pages and a spine — too literal for the name, and
  illegible when small.

---

## 8. Colour and type direction

**Palette suggestion**, to react to rather than follow:

- **Graphite** as the primary — near-black, slightly warm, like pencil rather than ink
- **Paper** as the light ground — soft off-white, not pure `#FFFFFF`
- **One accent only.** Suggest a brass/ochre — workbench, pencil ferrule, machined metal.
  Warmer and more distinctive than the technical blue this category defaults to.
- Blueprint blue is the obvious alternative; it's more expected, and expected is the risk here.

Whatever you pick must clear contrast checks on both a light and a dark ground.

**Type:**

- A **monospace** face is thematically right — this is markdown in git — and should feature in
  the wordmark or at minimum in supporting text.
- Full monospace for everything gets tiring; consider mono for the wordmark plus a clean
  grotesque for supporting copy on the social card.
- Set **"benchbook" lowercase.** It's a lowercase-repo-name kind of project, and it matches
  the tone.

---

## 9. Social preview card — content

This one needs a content decision, not just a visual. It's the highest-traffic asset: it
renders wherever the link is shared, often to people who have never heard of the project.

Should carry:

- The mark
- **benchbook**
- One line. Best current candidate: *"A wiki your AI maintains — under rules it can't quietly
  change."*
- Nothing else. No feature list, no badges, no screenshots.

It must survive being displayed at roughly 400 px wide in a chat client, so the tagline needs
to still be legible small.

---

## 10. Reference points

Aesthetics worth looking at, none to copy directly:

- Ordnance Survey benchmarks and trig-point markings
- Engineering drawing conventions — dimension lines, tolerance marks, section arrows
- Vintage lab notebooks and Moleskine ruling
- Machinist's tools — calipers, squares, gauge blocks
- Documentation-first open-source projects that look considered rather than corporate

---

## 11. Delivery

- SVG for all vector assets, PNG at the sizes listed above
- Everything into `design/` in this repo, with a short `design/README.md` documenting the
  palette hexes, fonts, and where each asset is used
- Any font must be freely licensed and embeddable

---

## 12. Context if you want more

The repo's own docs explain the system. Most useful for design context:

- `README.md` — tone of voice, the three worked examples
- `docs/day-in-the-life.md` — what people actually do with it
- `docs/01-concept.md` — the problem being solved

> **Note:** this brief is a working document. Consider removing or gitignoring it before the
> repo is made public, unless the design process is something worth showing.
