import plantsData from '../data/plants.json';
import pestsData from '../data/pests.json';

export async function GET() {
  const base = 'https://www.permieportal.com';

  const staticPaths = ['/', '/plants', '/pests', '/diagnose', '/articles', '/projects', '/about'];
  const plantPaths = plantsData.map(p => `/plants/${p.slug}`);
  const pestPaths = pestsData.map(p => `/pests/${p.slug}`);

  const allPaths = [...staticPaths, ...plantPaths, ...pestPaths];

  const xml =
    `<?xml version="1.0" encoding="UTF-8"?>\n` +
    `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
    allPaths.map(p => `  <url><loc>${base}${p}</loc></url>`).join('\n') +
    `\n</urlset>`;

  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } });
}
