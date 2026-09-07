/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        ink: {
          950: '#0B0E15',
          900: '#0F1420',
          800: '#171D2B',
          700: '#202839',
          600: '#2A3244',
          500: '#3A4359'
        },
        paper: {
          100: '#F4F1EA'
        },
        text: {
          primary: '#E8EAF0',
          muted: '#8B93A7',
          faint: '#5B6478'
        },
        tag: {
          amber: '#E8A33D',
          rust: '#C8623A',
          moss: '#5C8A5A',
          wine: '#A8455C'
        }
      },
      fontFamily: {
        display: ['"Barlow Condensed"', 'sans-serif'],
        body: ['"IBM Plex Sans"', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'monospace']
      }
    }
  },
  plugins: []
}
