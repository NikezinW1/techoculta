import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const blog = defineCollection({
	// Load Markdown and MDX files in the `src/content/blog/` directory.
	loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
	// Type-check frontmatter using a schema
	schema: ({ image }) =>
		z.object({
			title: z.string(),
			description: z.string(),
			// Transform string to Date object
			pubDate: z.coerce.date(),
			updatedDate: z.coerce.date().optional(),
			heroImage: z.optional(image()),
			category: z.string().optional(),
			tags: z.array(z.string()).optional(),
			author: z.string().default('Nikezin Indica'),
			featured: z.boolean().default(false),
			articleType: z.enum(['informational', 'comparison', 'guide', 'deal']).optional(),
			relatedArticles: z.array(z.string()).optional(),
			pros: z.array(z.string()).optional(),
			cons: z.array(z.string()).optional(),
			review: z.object({
				custoBeneficio: z.number().optional(),
				desempenho: z.number().optional(),
				construcao: z.number().optional(),
				recursos: z.number().optional(),
				notaFinal: z.number()
			}).optional(),
			relatedPosts: z.array(z.string()).optional(), // Legacy, replaced by relatedArticles over time
		}),
});

export const collections = { blog };
