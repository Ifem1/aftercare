import type { Metadata } from 'next';
import './globals.css';
import './studio.css';
import './wallet.css';
export const metadata: Metadata = { title: 'AFTERCARE — Fund what didn’t break', description: 'Retroactive public-goods funding for invisible maintenance.' };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }
