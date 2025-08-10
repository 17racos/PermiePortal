# PermiePortal v2 (Astro + Tailwind)

Lean static site reboot. No Rails. No database. Just content, speed, and dirt.

## Tech
- Astro + Tailwind
- Content in `src/content` as MDX with frontmatter `{ title, date, summary, tags, slug }`
- Images in `public/`

## Scripts
- `npm run dev`
- `npm run build`
- `npm run preview`

## Structure
- `src/pages`: `/`, `/articles`, `/projects`, `/shop`, `/about`
- `src/content/articles` and `src/content/projects` for MDX entries
- Feeds:
  - RSS: `/articles/rss.xml`
  - JSON: `/projects/feed.json`

## Deploy
- Build: `npm run build`
- Output: `dist/`

### Vercel
- Framework preset: Astro
- Build command: `npm run build`
- Output directory: `dist`

### Netlify
- Build command: `npm run build`
- Publish directory: `dist`
- Redirects: none needed

### DNS
- Point `A`/`AAAA` or CNAME to your host (Vercel/Netlify). No server required.

## Content Migration
See `MIGRATION_REPORT.md` for what moved and what we ignored.
