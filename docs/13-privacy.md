# Privacy

A wiki like this becomes personal fast. Not because you set out to record anything sensitive,
but because it works: you file the server's configuration, then your training data, then the
reasoning behind a decision that involved your family, and none of those felt like a
disclosure at the time.

Plan for that on day one, not on the day you want to share something.

---

## `publish: false` by default

Every page carries a `publish` field, and it defaults to `false`. A human flips individual
pages to `true`.

The default direction is the entire point. A default of `true` means every page is public
until someone remembers otherwise, and "someone remembers otherwise" is not a security model.
With `false` as the default, forgetting is safe — the failure mode of inattention is a page
nobody sees, rather than a page everybody sees.

In the live setup this field gates a static site build, which filters on it. Even with no
publishing pipeline at all, keep the field: it's the marker for *"I have consciously decided
this is shareable,"* and you'll want that distinction the first time you consider sharing
anything.

---

## The repo itself

The wiki is a git repo. Decide its visibility before the first commit, because git history is
forever and a private-to-public flip publishes every commit ever made, not just the current
state.

Sane default: **private repo, `publish: false` pages, and a separate deliberate act for
anything public.** Two independent gates. This repo followed exactly that — created private,
with the flip to public as its own approval step behind a sanitization review.

---

## What actually leaks

From doing this sanitization for real, the things that catch you are rarely the obvious ones.
You will remember not to commit a password. You will not remember these:

**Infrastructure identifiers.** Internal IPs, hostnames, subdomains, port numbers, container
names. Individually harmless; collectively a map of your network drawn by someone who knows it
well.

**Location, inferred.** Not your address — the regional sites you use, the local services, the
language of a source, the weather station you pull from, a currency in a price table. Three of
these together locate you to a city.

**Other people.** Family members, friends who recommended things, colleagues in a decision.
They did not choose to be in your wiki. This is the category that most deserves care, because
the subject can't check what you wrote.

**Health and body data.** Trivially accumulated by a wiki that tracks training, and among the
most sensitive categories you can hold.

**Secrets in "just an example."** The comprehensiveness instinct is what gets you: you paste a
working config so the page is complete, and the working config works because it has a real
token in it. The contract's rule — only environment variables, secret references, or vault
lookups, ever — exists for this exact moment.

**Purchase and financial detail.** Prices paid, accounts, subscriptions. Individually dull, in
aggregate a decent financial profile.

---

## Sanitizing before you share

If you're publishing part of a personal wiki, a workable order:

1. **Grep for the mechanical things first** — IPs, your domains, hostnames, known names,
   `token`, `key`, `password`, `secret`. Cheap and catches most of it.

   ```bash
   grep -rniE "yourdomain\.com|192\.168|10\.0\.|token|secret|passwd" --include="*.md" .
   ```

2. **Read every page you're publishing, in full.** Grep does not find "the guy at the shop
   near us" or an inferrable location. There is no substitute for reading it.

3. **Check the git history**, not just the working tree. A secret removed in a later commit is
   still in the repo.

4. **Reconsider aggregation.** Each page can be fine while the set is not. Reading twenty
   pages of someone's homelab tells you things no single page did.

5. **Prefer describing to naming.** "A regional classifieds site" carries the same meaning as
   the name and doesn't pin your country. The docs in this repo do this throughout — the point
   of a case study is the mechanism, not the vendor.

---

## Two structural notes

**Sources embed full external content.** That's deliberate — it keeps the wiki self-contained
when URLs rot — but it means your repo contains other people's copyrighted material. Fine for
a private repo, a genuine problem for a public one. If you publish, publish the pages you
wrote, not the transcripts you archived.

**The agent reads everything.** Anything in the wiki may enter a model context in a later
session. That's the feature. But it means "I'll put it in the wiki and remember it's
sensitive" doesn't hold — the wiki has no privacy tiers within itself. If something shouldn't
be readable by the agent, it doesn't belong in the wiki.

---

**Next:** [14 — Cost & Limits](14-cost-and-limits.md).
