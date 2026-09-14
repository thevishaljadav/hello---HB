import '../styles/globals.css';

export const metadata = {
  title: { default: 'MastiFlix', template: '%s | MastiFlix' },
  description: 'Indian vertical stories, series, music and community — made for mobile.',
};

export default function RootLayout({ children }) {
  return <html lang="en"><head><link rel="icon" href="/favicon.svg" sizes="any" /></head><body>{children}</body></html>;
}
