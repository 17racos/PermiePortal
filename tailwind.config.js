import typography from '@tailwindcss/typography';
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/**/*.{astro,html,md,mdx}',
    './src/components/**/*.{astro,html,md,mdx}',
    './src/pages/**/*.{astro,html,md,mdx}'
  ],
  theme: {
    extend: {
      colors: {
        ink: '#0b0b0c',
        swamp: '#0f172a',
        limewash: '#e2e8f0',
        citrus: '#f59e0b'
      }
    }
  },
  plugins: [typography]
};


