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
          <Badge tone="success">Business workspace</Badge>
          <p className="muted-copy">
            Manage your business profile, complete assessments, review insights, and build practical action plans in one place.
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
