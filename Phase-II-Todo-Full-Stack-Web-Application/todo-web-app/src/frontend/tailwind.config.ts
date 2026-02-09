import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: 'var(--background)',
        foreground: 'var(--foreground)',
        'neon-pink': 'var(--neon-pink)',
        'neon-pink-light': 'var(--neon-pink-light)',
        'neon-pink-glow-medium': 'var(--neon-pink-glow-medium)',
        'neon-pink-glow-strong': 'var(--neon-pink-glow-strong)',
        'neon-red': 'var(--neon-red)',
        'neon-red-glow-medium': 'var(--neon-red-glow-medium)',
        'neon-red-glow-strong': 'var(--neon-red-glow-strong)',
      },
      textShadow: {
        sm: '0 1px 2px var(--tw-shadow-color)',
        DEFAULT: '0 2px 4px var(--tw-shadow-color)',
        lg: '0 8px 16px var(--tw-shadow-color)',
      },
    },
  },
  plugins: [],
};

export default config;
