import type { Metadata } from "next";
import Link from "next/link";
import type { ReactNode } from "react";

import "./globals.css";

export const metadata: Metadata = {
  title: "BiasharaMind",
  description: "AI business consultant platform for SMEs.",
};

type RootLayoutProps = {
  children: ReactNode;
};

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en">
      <body>
        <div className="app-shell">
          <header className="site-header">
            <div className="site-header__inner">
              <Link className="brand" href="/">
                BiasharaMind
              </Link>
              <nav aria-label="Global" className="site-nav">
                <Link href="/">Home</Link>
                <Link href="/login">Login</Link>
                <Link href="/signup">Sign up</Link>
                <Link href="/dashboard">Dashboard</Link>
              </nav>
            </div>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
