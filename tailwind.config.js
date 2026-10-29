/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./App.jsx"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Poppins', 'Nunito', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      colors: {
        cream: {
          50: '#FFFEFA',
          100: '#FFF9EF',
          200: '#FAF0DF',
          DEFAULT: '#FFF9EF',
          dark: '#EFE4D0',
        },
        'card-border': '#EBE3D5',
        saffron: {
          DEFAULT: '#F58220',
          dark: '#D66C12',
          light: '#FFF4EA',
          contrast: '#B85A0B',
        },
        leaf: {
          DEFAULT: '#257A4B',
          dark: '#1B5E39',
          light: '#E8F5EE',
        },
        charcoal: {
          DEFAULT: '#1F1A17',
          muted: '#594D46',
        },
        white: '#FFFFFF',
      },
      boxShadow: {
        'warm-sm': '0 2px 8px rgba(31,26,23,.04)',
        'warm-md': '0 8px 24px rgba(31,26,23,.06)',
        'warm-lg': '0 16px 36px rgba(31,26,23,.09)',
        'saffron-glow': '0 8px 20px rgba(245,130,32,.28)',
      },
      borderRadius: {
        'xl': '0.75rem',
        '2xl': '1rem',
        '3xl': '1.5rem',
      }
    },
  },
  plugins: [],
}
