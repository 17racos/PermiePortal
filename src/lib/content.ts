export function getSlug(data: { slug?: string; title?: string }) {
  if (data?.slug) return data.slug;
  const base = (data?.title ?? '').toString().trim().toLowerCase();
  return base.replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

export function kebab(s: string) {
    return s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
  }
  export function getSlug(data: { slug?: string; title: string }) {
    return data.slug && data.slug.trim() ? data.slug : kebab(data.title);
  }
  export function fmt(date: Date) {
    return new Date(date).toLocaleDateString();
  }
  
  