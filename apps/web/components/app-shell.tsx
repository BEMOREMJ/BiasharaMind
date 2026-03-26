import Link from "next/link";
import type { ReactNode } from "react";

import { BrandLogo } from "@/components/brand-logo";

type AppShellProps = {
  children: ReactNode;
};

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="app-shell app-shell-layout">
      <header className="site-header">
        <div className="site-header__inner">
          <Link aria-label="BiasharaMind home" href="/">
            <BrandLogo />
          </Link>
          <nav aria-label="Global" className="site-nav">
            <Link className="nav-link" href="/">
              Home
            </Link>
            <Link className="nav-link" href="/login">
              Login
            </Link>
            <Link className="nav-link" href="/signup">
              Sign up
            </Link>
            <Link className="nav-link" href="/dashboard">
              Dashboard
            </Link>
          </nav>
        </div>
      </header>
      {children}
    </div>
  );
}
