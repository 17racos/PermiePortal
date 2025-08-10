export async function GET() {
  const modules = import.meta.glob('../../content/projects/**/*.mdx', { eager: true });
  const items = Object.values(modules)
    .map((m) => ({ ...(m.frontmatter || {}), url: m.url }))
    .filter((p) => p.title)
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

  return new Response(JSON.stringify({
    version: 'https://jsonfeed.org/version/1',
    title: 'PermiePortal — Projects',
    home_page_url: 'https://permieportal.example/projects',
    items: items.map((p) => ({
      id: p.slug,
      url: p.url || `/projects/${p.slug}`,
      title: p.title,
      content_text: p.summary,
      date_published: new Date(p.date).toISOString(),
      tags: p.tags || []
    }))
  }), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' }
  });
}


