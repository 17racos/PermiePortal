import { defineCollection, z } from "astro:content";

const base = z.object({
  title: z.string(),
  date: z.coerce.date(),
  summary: z.string().max(300),
  tags: z.array(z.string()).default([]),
  slug: z.string(),
});

export const collections = {
  articles: defineCollection({ type: "content", schema: base }),
  projects: defineCollection({ type: "content", schema: base }),
};
