import '../styles/globals.css';

export const metadata = {
  title: { default: 'Asia Drama', template: '%s | Asia Drama' },
  description: 'Asia Drama — vertical stories, series, music and community, made for mobile.',
};

export default function RootLayout({ children }) {
  return <html lang="en"><head><link rel="icon" href="/favicon.svg" sizes="any" /></head><body>{children}</body></html>;
}
