import type { Metadata } from 'next';
import { Inter, Roboto_Mono } from 'next/font/google';
import { Providers } from './providers';
import './globals.css';

const inter = Inter({
  variable: '--font-inter',
  subsets: ['latin'],
  display: 'swap',
});

const robotoMono = Roboto_Mono({
  variable: '--font-roboto-mono',
  subsets: ['latin'],
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'Kai Kagawa King — Portfolio',
  description:
    'Data Science & Economics student at Northeastern University with experience in econometrics, machine learning, and policy analysis.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${robotoMono.variable} h-full antialiased`}
      suppressHydrationWarning
    >
      <body className="min-h-full flex flex-col bg-white dark:bg-neutral-950 text-black dark:text-white font-sans">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
