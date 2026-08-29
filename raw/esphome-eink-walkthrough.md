<!--
  DEMO raw file.

  This is the immutable layer: source material as it arrived. The agent reads
  from here and never edits it. Note the shape — unpolished, with clipper
  metadata at the top and no frontmatter. It is not a wiki page.

  Ingesting this produced:
    wiki/sources/esphome-eink-dashboard-walkthrough.md
  which links to the ONLINE url, never back to this path (Hard Rule 14).

  After 14 days LINT offers to move this to raw/_archived/knowledge/ —
  which is exactly why page bodies must not link to raw paths.
-->

source: https://example.com/esphome-eink-walkthrough
saved: 2026-08-12
channel: Example Maker Channel

---

...so the thing that gets everyone the first time is the refresh mode. If you just set it up
the default way, every single update does a full refresh — that's the flashing you see, black
to white to black, takes about three seconds. Looks broken. What you actually want is partial
refresh for routine updates, and then a full refresh maybe every twenty updates or so, just to
clear the ghosting that builds up.

The second thing is sleep current. I had a build where I was getting maybe four days out of a
battery that should have lasted two months, and it turned out the display component was
holding a lock that stopped the board entering deep sleep at all. It looked fine in the logs.
You have to actually put a meter on it.

And then the wake interval. This is the one nobody thinks about hard enough. If you wake every
minute you're looking at days of battery life. Fifteen minutes and you're into months. Ask
yourself how often the thing you're displaying actually changes — for a calendar, it's not
every minute.

Board choice: I went C6 over C3 mostly for the deep sleep number...
