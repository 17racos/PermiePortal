import { getCollection } from 'astro:content';

export async function GET() {
  const base = 'https://permieportal.com';

  const staticPaths = ['/', '/articles', '/projects', '/about'];

  const articles = await getCollection('articles');
  const articlePaths = articles.map(a => `/articles/${a.slug}`);

  const plants = await getCollection('plants');
  const plantPaths = plants.map(p => `/plants/${p.slug}`);

  const allPaths = [...staticPaths, ...articlePaths, ...plantPaths];

  const xml =
    `<?xml version="1.0" encoding="UTF-8"?>\n` +
    `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">` +
    allPaths.map(p => `<url><loc>${base}${p}</loc></url>`).join('') +
    `</urlset>`;

  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } });
}
