import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

/**
 * Post-build assertion: nothing marked `publish: false` may appear in dist/.
 * Matches on the wiki page titles rather than trusting the build to have filtered.
 */
const wikiDir = "../wiki";
const priv = [];
(function walk(dir) {
  for (const f of readdirSync(dir)) {
    const p = join(dir, f);
    if (statSync(p).isDirectory()) walk(p);
    else if (f.endsWith(".md")) {
      const src = readFileSync(p, "utf8");
      const fm = src.split("---")[1] ?? "";
      if (/publish:\s*false/.test(fm)) {
        const title = fm.match(/title:\s*"?([^"\n]+)"?/)?.[1]?.trim();
        if (title) priv.push({ file: p, title });
      }
    }
  }
})(wikiDir);

const html = [];
(function walk(dir) {
  for (const f of readdirSync(dir)) {
    const p = join(dir, f);
    if (statSync(p).isDirectory()) walk(p);
    else if (f.endsWith(".html")) html.push([p, readFileSync(p, "utf8")]);
  }
})("dist");

const leaks = [];
for (const { file, title } of priv) {
  for (const [p, body] of html) {
    if (body.includes(`<h1>${title}</h1>`)) leaks.push(`${title} (${file}) → ${p}`);
  }
}

if (leaks.length) {
  console.error("PRIVACY CHECK FAILED — publish: false content reached dist/:");
  leaks.forEach((l) => console.error("  " + l));
  process.exit(1);
}
console.log(`privacy check ok — ${priv.length} unpublished pages, none in dist/`);
