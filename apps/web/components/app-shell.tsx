import Link from "next/link";
import type { ReactNode } from "react";

import { BrandLogo } from "@/components/brand-logo";
import { SignOutButton } from "@/components/sign-out-button";
import { getAuthenticatedUser } from "@/lib/supabase/server";

type AppShellProps = {
  children: ReactNode;
};

export async function AppShell({ children }: AppShellProps) {
  const user = await getAuthenticatedUser();

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
            <Link className="nav-link" href="/dashboard">
              Dashboard
            </Link>
            {user ? (
              <>
                <span className="nav-link nav-link--muted">{user.email ?? "Signed in"}</span>
                <SignOutButton />
              </>
            ) : (
              <>
                <Link className="nav-link" href="/login">
                  Login
                </Link>
                <Link className="nav-link" href="/signup">
                  Sign up
                </Link>
              </>
            )}
          </nav>
        </div>
      </header>
      {children}
    </div>
  );
}
