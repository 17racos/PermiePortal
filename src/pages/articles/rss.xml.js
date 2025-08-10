import rss from '@astrojs/rss';

export async function GET(context) {
  const modules = import.meta.glob('../../content/articles/**/*.mdx', { eager: true });
  const items = Object.values(modules)
    .map((m) => ({ ...(m.frontmatter || {}), url: m.url }))
    .filter((a) => a.title)
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

  return rss({
    title: 'PermiePortal — Articles',
    description: 'Rotten articles roasting bad ideas and field-tested hacks.',
    site: context.site || 'https://permieportal.example',
    items: items.map((a) => ({
      title: a.title,
      description: a.summary,
      link: a.url || `/articles/${a.slug}`,
      pubDate: new Date(a.date)
    }))
  });
}


