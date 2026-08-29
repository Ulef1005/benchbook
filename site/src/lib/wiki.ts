import { getCollection, type CollectionEntry } from "astro:content";

export type WikiEntry = CollectionEntry<"wiki">;

/** The privacy gate. Every wiki read in the site goes through this — no exceptions. */
export async function publishedWiki(): Promise<WikiEntry[]> {
  return (await getCollection("wiki")).filter((e) => e.data.publish === true);
}

/** wiki/knowledge/entities/esp32-c6 -> { domain: "knowledge", slug: "esp32-c6" } */
export function place(id: string) {
  const p = id.replace(/\.md$/, "");
  const m = p.match(/^index-(.+)$/);
  if (m) return { domain: m[1], slug: null, kind: "index" as const };
  const parts = p.split("/");
  const slug = parts.pop()!;
  const domain = parts[0] ?? "meta";
  const kind = parts[1] ?? parts[0] ?? "meta";
  return { domain, slug, kind };
}

export function href(entry: WikiEntry) {
  const { domain, slug } = place(entry.id);
  return slug ? `/wiki/${domain}/${slug}/` : `/wiki/${domain}/`;
}

/**
 * Backlinks, computed at build. The contract already enforces that `sources:` and the body
 * links mirror each other, so both directions are trustworthy without extra authoring.
 */
export async function backlinkMap() {
  const pages = await publishedWiki();
  const bySlug = new Map(pages.map((p) => [place(p.id).slug, p]));
  const map = new Map<string, WikiEntry[]>();
  const add = (slug: string, from: WikiEntry) => {
    const list = map.get(slug) ?? [];
    if (!list.some((e) => e.id === from.id)) list.push(from);
    map.set(slug, list);
  };
  for (const page of pages) {
    for (const s of page.data.sources) add(s.replace(/\.md$/, "").split("/").pop()!, page);
    for (const m of page.body?.matchAll(/\]\(([^)]+?\.md)(?:#[^)]*)?\)/g) ?? []) {
      const slug = m[1].split("/").pop()!.replace(/\.md$/, "");
      if (bySlug.has(slug) && slug !== place(page.id).slug) add(slug, page);
    }
  }
  return map;
}
