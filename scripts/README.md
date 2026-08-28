# scripts/ — code store

Code that is **not** a live deployed service:

- Wiki tooling — `lint.py` and friends, loose at the root
- Per-project build recipes or firmware source whose deployed form is a separate artifact,
  each in `scripts/<slug>/` with its own `README.md` linking back to the wiki page

Continuously-running deployed services belong in their own infrastructure repo, where the
on-host path **is** the git working tree. A repo that is a *copy* of what's running on a
server rots: someone applies a fix in the field at 11pm, it works, and the repo silently stops
describing reality.

## Conventions

1. **Faithful backup.** Byte-for-byte copies of the on-disk originals — no added headers, no
   helpful reformatting. The moment a stored copy differs cosmetically, diffing it against the
   original stops being useful. Re-copy after any edit.
2. **No secrets.** Only environment variables, secret references, or vault indirection. This
   matters more here than in a normal repo, because the wiki's whole purpose is to be
   comprehensive — and comprehensiveness is exactly the instinct that leads to pasting a
   working config with a real token in it. LINT scans this folder and treats a hardcoded
   credential as an error.
3. **Two-way link.** The wiki page links to the files; the subfolder README links back.
4. **Not a wiki page.** No frontmatter, not indexed.
