import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

// Nothing is copied into the site: every collection points at the repo's own markdown.
const docs = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "../docs" }),
  schema: z.object({ title: z.string().optional(), description: z.string().optional() }).passthrough(),
});

const contract = defineCollection({
  loader: glob({ pattern: ["AGENTS.md", "agents-*.md"], base: ".." }),
  schema: z.object({ title: z.string().optional() }).passthrough(),
});

const domains = defineCollection({
  loader: glob({ pattern: "*/README.md", base: "../domains" }),
  schema: z.object({ title: z.string().optional() }).passthrough(),
});

// Mirrors docs/05-page-types.md. Keep in sync with scripts/lint.py — if the lint pass
// gains a required field, add it here too, so a bad page fails the build as well.
// DEMO.md is excluded: like the raw/ files it documents, it carries no frontmatter and isn't
// itself a wiki page — it's a README for the demo content, meant to be removed along with it.
const wiki = defineCollection({
  loader: glob({ pattern: ["**/*.md", "!DEMO.md"], base: "../wiki" }),
  schema: z.object({
    title: z.string(),
    type: z.enum(["source", "entity", "reference", "project", "overview", "person"]),
    created: z.coerce.date(),
    domain: z.string().nullable().default(null),
    subdomain: z.string().nullable().default(null),
    publish: z.boolean().default(false),
    status: z.string().optional(),
    tags: z.array(z.string()).default([]),
    sources: z.array(z.string()).default([]),
    source_url: z.string().url().optional(),
    repo_url: z.string().url().optional(),
    channel: z.string().optional(),
    change_history: z.boolean().optional(),
  }),
});

export const collections = { docs, contract, domains, wiki };
