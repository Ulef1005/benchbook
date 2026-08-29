import { visit } from "unist-util-visit";
import path from "node:path";

/**
 * Relative `.md` links keep the markdown valid on GitHub. On the site they have to become
 * routes. Mapping, by where the file lives in the repo:
 *   wiki/<domain>/<kind>/<slug>.md  -> /wiki/<domain>/<slug>/
 *   wiki/index-<domain>.md          -> /wiki/<domain>/
 *   docs/<n>-<slug>.md              -> /docs/<n>-<slug>/
 *   agents-*.md | AGENTS.md         -> /contract/<slug>/
 * Anything else that resolves inside the repo (skills, README, LICENSE — real files, just not
 * part of any collection this site renders) points at its GitHub blob instead of failing the
 * build; a link is only unresolvable, and only then throws, if it doesn't resolve to a file in
 * the repo at all.
 */
const BASE = "/benchbook";
const REPO_ROOT = path.resolve(process.cwd(), "..");
const GITHUB_BLOB = "https://github.com/Ulef1005/benchbook/blob/main";

function toRoute(abs) {
  const rel = abs.split(/[\\/]/).join("/");
  const i = rel.lastIndexOf("/wiki/");
  if (i !== -1) {
    const p = rel.slice(i + 6).replace(/\.md$/, "");
    const idx = p.match(/^index-(.+)$/);
    if (idx) return `${BASE}/wiki/${idx[1]}/`;
    if (p === "index") return `${BASE}/wiki/`;
    const parts = p.split("/");
    const slug = parts.pop();
    const domain = parts[0] === "people" ? "people" : parts[0] || "wiki";
    return `${BASE}/wiki/${domain}/${slug}/`;
  }
  const d = rel.lastIndexOf("/docs/");
  if (d !== -1) return `${BASE}/docs/${rel.slice(d + 6).replace(/\.md$/, "")}/`;
  const base = rel.split("/").pop();
  if (/^(AGENTS|agents-.+)\.md$/.test(base)) return `${BASE}/contract/${base.replace(/\.md$/, "")}/`;
  const repoRel = path.relative(REPO_ROOT, abs).split(path.sep).join("/");
  if (!repoRel.startsWith("..") && !path.isAbsolute(repoRel)) return `${GITHUB_BLOB}/${repoRel}`;
  return null;
}

export default function remarkWikiLinks() {
  return (tree, file) => {
    const dir = path.dirname(file.history?.[0] ?? file.path ?? ".");
    visit(tree, "link", (node) => {
      const url = node.url;
      if (!url || /^[a-z]+:/i.test(url) || url.startsWith("#") || url.startsWith("/")) return;
      const [target, hash = ""] = url.split("#");
      if (!target.endsWith(".md")) return;
      const route = toRoute(path.resolve(dir, target));
      if (!route) {
        throw new Error(`Unresolvable markdown link "${url}" in ${file.history?.[0] ?? "unknown file"}`);
      }
      node.url = hash ? `${route}#${hash}` : route;
    });
  };
}
