// Reads the wiki/ folder directly at build time — no content duplication, no symlink.
// This is intentionally plain fs + gray-matter + marked rather than Astro's content
// collections API, so it stays readable without knowing Astro's abstractions, and so a fork
// that renames or restructures wiki/ only has to change this one file.

import fs from 'node:fs';
import path from 'node:path';
import posix from 'node:path/posix';
import matter from 'gray-matter';
import { marked } from 'marked';

// Resolved from process.cwd(), not import.meta.url — the latter breaks once Vite bundles
// this file, since the built chunk lands at a different depth (dist/.prerender/chunks/) than
// the source. Astro always runs `astro build`/`astro dev` with cwd = the project root (where
// package.json lives), so `../wiki` from there is stable regardless of bundling.
export const WIKI_ROOT = path.resolve(process.cwd(), '../wiki');

function walk(dir) {
	let files = [];
	for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
		const full = path.join(dir, entry.name);
		if (entry.isDirectory()) {
			files.push(...walk(full));
		} else if (entry.name.endsWith('.md')) {
			files.push(full);
		}
	}
	return files;
}

// A slug is the file's path relative to wiki/, without the .md extension, always
// forward-slashed regardless of OS — e.g. "knowledge/entities/esphome".
function slugFor(absPath) {
	return path.relative(WIKI_ROOT, absPath).replace(/\.md$/, '').split(path.sep).join('/');
}

// Correct default: only publish: true pages, matching docs/15-publishing.md ("The build step
// needs to filter on that frontmatter field, not publish everything by default"). This repo's
// own demo content is all publish: false — the convention's default, not a considered "keep
// private" decision, since nothing here has ever gone through a real publish call — so the
// demo build opts into includeUnpublished via PUBLIC_DEMO_MODE (see package.json). A fork that
// brings real wiki content should drop that env var and make actual per-page publish: true
// decisions instead.
export function loadAllPages({ includeUnpublished = false } = {}) {
	return walk(WIKI_ROOT)
		.map((absPath) => {
			const raw = fs.readFileSync(absPath, 'utf-8');
			const { data, content } = matter(raw);
			return { slug: slugFor(absPath), data, content };
		})
		.filter((page) => includeUnpublished || page.data.publish === true);
}

export function loadPage(slug) {
	const absPath = path.join(WIKI_ROOT, `${slug}.md`);
	const raw = fs.readFileSync(absPath, 'utf-8');
	const { data, content } = matter(raw);
	return { slug, data, content };
}

// Rewrites rendered `<a href="relative/path.md">` links to site routes, resolving them
// relative to the *page's own directory* — the same resolution rule the wiki's own convention
// (agents-core.md Hard Rule 4) uses. Anchors and external links pass through untouched.
export function rewriteLinks(html, currentSlug) {
	const currentDir = posix.dirname(currentSlug);
	return html.replace(/href="([^"]+\.md)(#[^"]*)?"/g, (match, mdPath, anchor = '') => {
		if (/^https?:\/\//.test(mdPath)) return match;
		const resolvedSlug = posix.normalize(posix.join(currentDir, mdPath)).replace(/\.md$/, '');
		return `href="/benchbook/page/${resolvedSlug}${anchor}"`;
	});
}

export function renderBody(content, slug) {
	return rewriteLinks(marked.parse(content), slug);
}

// Domains found across all pages, each with its page count — `domain: null` (meta/people
// pages) is excluded, matching how the wiki's own index.md treats it.
export function domainCounts(pages) {
	const counts = new Map();
	for (const page of pages) {
		if (!page.data.domain) continue;
		counts.set(page.data.domain, (counts.get(page.data.domain) ?? 0) + 1);
	}
	return [...counts.entries()].sort(([a], [b]) => a.localeCompare(b));
}
