import { defineConfig } from "astro/config";
import remarkWikiLinks from "./plugins/remark-wiki-links.mjs";

// Project page: https://ulef1005.github.io/benchbook/
// On a custom domain, drop `base` and set `site` to the domain.
export default defineConfig({
  site: "https://ulef1005.github.io",
  base: "/benchbook",
  trailingSlash: "always",
  markdown: {
    remarkPlugins: [remarkWikiLinks],
    shikiConfig: { theme: "vitesse-dark", wrap: true },
  },
});
