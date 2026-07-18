/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        navy: {
          DEFAULT: '#14203D',
          50: '#EEF1F7',
          100: '#D6DCEA',
          400: '#4A5B85',
          600: '#233257',
          900: '#0D1526',
        },
        brand: {
          DEFAULT: '#2C6BED',
          50: '#EAF1FE',
          100: '#D3E2FD',
          500: '#2C6BED',
          600: '#1E54C9',
          700: '#173F99',
        },
        ink: '#101828',
        slate: {
          DEFAULT: '#667085',
          200: '#E4E7EC',
          300: '#D0D5DD',
        },
        bg: '#F5F7FB',
        success: '#12B76A',
        warning: '#F79009',
        danger: '#F04438',
      },
      fontFamily: {
        display: ['Sora', 'system-ui', 'sans-serif'],
        body: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
      borderRadius: {
        card: '14px',
        ticket: '10px',
      },
      boxShadow: {
        card: '0 1px 2px rgba(16, 24, 40, 0.06), 0 1px 3px rgba(16, 24, 40, 0.08)',
        'card-hover': '0 4px 12px rgba(16, 24, 40, 0.10)',
      },
    },
  },
  plugins: [],
}
