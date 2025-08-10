import { defineCollection, z } from 'astro:content';

const baseSchema = z.object({
  title: z.string(),
  date: z.date(),
  summary: z.string(),
  tags: z.array(z.string()).default([]),
});

export const collections = {
  articles: defineCollection({ type: 'content', schema: baseSchema }),
  projects: defineCollection({ type: 'content', schema: baseSchema }),
};
