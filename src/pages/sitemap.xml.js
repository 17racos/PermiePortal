export async function GET() {
  const base = 'https://permieportal.example';
  const urls = ['/', '/articles', '/projects', '/about'];
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n` +
  `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">` +
  urls.map((p) => `<url><loc>${base}${p}</loc></url>`).join('') + `</urlset>`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } });
}


