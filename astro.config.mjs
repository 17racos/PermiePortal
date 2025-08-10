import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import mdx from '@astrojs/mdx';

export default defineConfig({
  site: 'https://permieportal.example',
  integrations: [tailwind({ applyBaseStyles: true }), mdx()],
  server: { host: true, port: 4321 },
  markdown: { smartypants: true },
  output: 'static',
});
