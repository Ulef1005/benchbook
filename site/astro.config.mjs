// @ts-check
import { defineConfig } from 'astro/config';

// GitHub Pages serves this repo at https://<username>.github.io/benchbook/ — `base` has to
// match the repo name, or every internal link 404s. See docs/15-publishing.md.
// https://astro.build/config
export default defineConfig({
	site: 'https://ulef1005.github.io',
	base: '/benchbook',
});
