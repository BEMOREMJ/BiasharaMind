import Link from "next/link";
import type { ReactNode } from "react";

import { dashboardNavigation } from "@/lib/navigation";

type DashboardShellProps = {
  children: ReactNode;
};

export function DashboardShell({ children }: DashboardShellProps) {
  return (
    <main className="dashboard-shell">
      <aside className="dashboard-sidebar">
        <h2>Workspace</h2>
        <nav aria-label="Dashboard" className="dashboard-nav">
          {dashboardNavigation.map((item) => (
            <Link href={item.href} key={item.href}>
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>
      {children}
    </main>
  );
}
