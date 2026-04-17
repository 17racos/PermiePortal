import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = await getCollection('articles');
  const items = posts
    .sort((a,b)=> b.data.date.getTime()-a.data.date.getTime())
    .map((p) => ({
      title: p.data.title,
      description: p.data.summary,
      link: `/articles/${p.data.slug}`,
      pubDate: p.data.date,
    }));

  return rss({
    title: 'PermiePortal — Articles',
    description: 'Rotten ideas and field-tested hacks.',
    site: context.site || 'https://www.permieportal.com',
    items,
  });
}


