# Publishing

Everything in this wiki is already readable — it's markdown in a git repo, so any git client,
editor, or GitHub's own file browser shows it. Publishing is not a step every wiki needs. It's
for a specific surface: a phone away from a keyboard, a kitchen display, a tablet on a
workbench. If you don't have one of those, skip this doc.

**A working example ships in this repo at [`site/`](../site/)** — a minimal, unstyled Astro
site that reads `wiki/` directly and applies everything below. Real design lands there via the
`benchbook-design` skill once it exists; the structure and the `wiki/` reading logic
(`site/src/lib/wiki.js`) are already real and buildable (`npm install && npm run build`).

---

## Design before tooling

The instinct is to pick a static-site generator first and build against whatever it defaults
to. That's backwards, and the original wiki's own publishing build proves it expensively (see
the case study below).

Write requirements before touching a tool. At minimum: what surface is this for (mobile?
desktop? a fixed display?), does it need to match a specific design, does it need to stay
private, and who maintains it once it's built — you, or an agent that won't get more attentive
over time. Only then evaluate generators against that list. A tool that's excellent in the
abstract can still be the wrong pick for requirements it wasn't tested against.

---

## Case study: a framework reversal

The original wiki's publishing project picked Quartz first — a wiki-focused static-site
generator, a reasonable default choice. A full build session later, it had a header duplicated
on mobile, a navigation drawer with a duplicate-listener bug, three separate stacking-context
fights over a backdrop element, and rebuild times around two minutes that turned every small
design tweak into a wait. None of that was unusual or a sign of a bad tool — it's ordinary
framework friction, the kind every generator has somewhere.

What made it a blocking cost rather than an annoyance was a single requirement: pixel-perfect
design fidelity on mobile. Once that was non-negotiable, every fight against the framework's
defaults stopped being a minor tax and started being the entire job. The project re-gathered
requirements from scratch, evaluated tools against them again, and picked Astro — which won not
because Quartz is worse in general, but because Astro imposes far less of its own opinion on
markup and styling, which is exactly what "pixel-perfect" needs.

**The generalizable point:** a framework fight that's livable at low design ambition can become
the whole project once ambition rises. If you hit this, the fix usually isn't pushing through —
it's re-checking whether the tool still matches the requirement that just got stricter.

---

## What actually matters for a benchbook-shaped wiki

Whatever generator you pick, a few things are specific to how this wiki is structured:

- **Read the `wiki/` folder directly.** Point the site's content root at it (a symlink works
  well) rather than copying files in — copies drift the moment you forget to re-sync.
- **Relative markdown links, not wikilinks.** benchbook pages link with
  `[text](relative/path.md)`, not `[[wikilinks]]`. Confirm your generator resolves relative
  `.md` links correctly before assuming wiki-style tools are a natural fit — some assume
  wikilinks and need a plugin or a rewrite pass to handle plain relative links instead.
- **Respect `publish: false`.** Every page defaults to unpublished. The build step needs to
  filter on that frontmatter field, not publish everything by default. (`site/`'s demo build
  is the one deliberate exception — every demo page here is `publish: false` because nothing
  has been through an actual publish decision yet, not because it's meant to stay hidden, so
  the demo build opts in via a `PUBLIC_DEMO_MODE` flag rather than showing an empty site. A
  real fork's build shouldn't set that flag — it should make real per-page decisions instead.)
- **Optimize for low maintenance.** The wiki side of this system is maintained by an agent, not
  necessarily by you checking in daily. A generator with a slow feedback loop or a lot of
  framework-specific debugging is a worse fit here than one that's boring and stable, even if
  it's less flexible.

---

## Deployment target: GitHub Pages by default

The original wiki self-hosted its site (Astro build, served by a reverse proxy on its own
server) because it needed LAN-only privacy for a fixed kitchen display. Most readers won't have
that constraint, and self-hosting is real ongoing maintenance — a server to keep patched, a
proxy config to maintain, a domain to renew.

**GitHub Pages is the default recommendation instead.** Astro officially supports it via the
`withastro/action` GitHub Action: a workflow builds your site and deploys it with
`actions/deploy-pages`, no server of your own required. Two things to set up correctly:

- Set `base` in `astro.config.mjs` to your repository name, unless the repo is named
  `<username>.github.io` — otherwise your site's internal links break, since Pages serves from
  `https://<username>.github.io/<repo>/` rather than the domain root.
- **Pages on a private repository needs a paid GitHub plan** (Pro, Team, or Enterprise). On a
  free plan, Pages only works once the repository is public — which matters if your actual
  wiki content (unlike this sanitized starter kit) is something you'd rather keep private.

If you need real privacy or a non-browser display surface, self-hosting stays the right answer
— just go in with requirements written down first, per the section above.
