/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{astro,html,js,jsx,ts,tsx,md,mdx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0b0b0b",
        surface: "#161616",
        border: "#2a2a2a",
        text: "#e6e6e6",
        muted: "#9ca3af",
        accent: "#a3e635",
      },
      borderRadius: { xl: "0.75rem", "2xl": "1rem" },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
