import '../styles/globals.css';
import { Inter } from 'next/font/google';
import { Providers } from '../components/Providers';
import { ReactNode } from 'react';
import { cn } from '../lib/utils';

const inter = Inter({ subsets: ['latin'] });

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en">
      <body className={cn('min-h-screen bg-background font-sans antialiased', inter.className)}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}