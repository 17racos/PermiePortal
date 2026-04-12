import { defineCollection, z } from "astro:content";

const base = z.object({
  title: z.string(),
  date: z.coerce.date().default(new Date()),
  summary: z.string().max(300),
  tags: z.array(z.string()).default([]),
  image: z.string().optional(),
  // slug is optional; we’ll compute a fallback from title when rendering
  slug: z.string().optional(),
});

export const collections = {
  articles: defineCollection({ type: "content", schema: base }),
  projects: defineCollection({ type: "content", schema: base }),
};
