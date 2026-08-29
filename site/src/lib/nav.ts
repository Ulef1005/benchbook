import { getCollection } from "astro:content";
import { publishedWiki, place, href } from "./wiki";

/** Sidebar groups for /docs and /contract. Order comes from the filename prefix. */
export async function docsNav() {
  const docs = (await getCollection("docs")).sort((a, b) => a.id.localeCompare(b.id));
  const num = (id: string) => Number(id.match(/^(\d+)/)?.[1] ?? NaN);
  const group = (id: string) => {
    const n = num(id);
    if (Number.isNaN(n)) return "Start here";
    if (n <= 7) return "Foundations";
    if (n <= 12) return "In practice";
    return "Caveats";
  };
  const groups = new Map<string, { label: string; href: string }[]>();
  for (const d of docs) {
    const label = d.data.title ?? d.id.replace(/^(\d+)-/, "$1 — ").replace(/-/g, " ");
    const g = group(d.id);
    groups.set(g, [...(groups.get(g) ?? []), { label, href: `/docs/${d.id}/` }]);
  }
  const contract = (await getCollection("contract")).map((c) => ({
    label: c.id + ".md", href: `/contract/${c.id}/`,
  }));
  groups.set("Reference", contract);
  return [...groups].map(([group, items]) => ({ group, items }));
}

/** Sidebar for /wiki — meta pages first, then a group per domain. */
export async function wikiNav() {
  const pages = await publishedWiki();
  const meta = pages.filter((p) => place(p.id).domain === "meta" || !place(p.id).slug);
  const groups = new Map<string, { label: string; href: string }[]>();
  for (const p of pages) {
    const { domain, slug } = place(p.id);
    if (!slug || domain === "meta") continue;
    groups.set(domain, [...(groups.get(domain) ?? []), { label: p.data.title, href: href(p) }]);
  }
  return [
    { group: "Meta", items: meta.map((p) => ({ label: p.data.title, href: href(p) })) },
    ...[...groups].map(([group, items]) => ({ group, items })),
  ];
}
