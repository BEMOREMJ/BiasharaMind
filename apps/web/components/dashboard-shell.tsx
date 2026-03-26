import Link from "next/link";
import type { ReactNode } from "react";

import { Badge } from "@/components/badge";
import { BrandLogo } from "@/components/brand-logo";
import { dashboardNavigation } from "@/lib/navigation";

type DashboardShellProps = {
  children: ReactNode;
};

export function DashboardShell({ children }: DashboardShellProps) {
  return (
    <main className="dashboard-shell">
      <aside className="dashboard-sidebar">
        <BrandLogo mode="lockup" />
        <div className="dashboard-stack">
          <Badge tone="success">V1 workspace</Badge>
          <p className="muted-copy">
            Placeholder surfaces for onboarding, assessment, results, roadmap, and history.
          </p>
        </div>
        <nav aria-label="Dashboard" className="dashboard-nav">
          {dashboardNavigation.map((item) => (
            <Link className="dashboard-nav__link" href={item.href} key={item.href}>
              <span className="dashboard-nav__label">{item.label}</span>
              <span className="dashboard-nav__description">{item.description}</span>
            </Link>
          ))}
        </nav>
      </aside>
      <div className="dashboard-main">{children}</div>
    </main>
  );
}
