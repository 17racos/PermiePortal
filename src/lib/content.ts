import type { CollectionEntry } from 'astro:content';
export function kebab(s: string) {
  return s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
}

export function getSlug(data: { slug?: string; title?: string }) {
  if (data?.slug && data.slug.trim()) return data.slug;
  const base = (data?.title ?? '').toString().trim().toLowerCase();
  return kebab(base);
}

export function entrySlug<E extends CollectionEntry<string>>(e: E): string {
  return e.data?.slug?.trim() ? e.data.slug : e.slug;
}

export function fmt(date: Date) {
  return new Date(date).toLocaleDateString();
}