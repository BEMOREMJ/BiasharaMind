import type { ReactNode } from "react";

import { DashboardShell } from "@/components/dashboard-shell";
import { requireAuthenticatedUser } from "@/lib/supabase/server";

type DashboardLayoutProps = {
  children: ReactNode;
};

export default async function DashboardLayout({ children }: DashboardLayoutProps) {
  const user = await requireAuthenticatedUser();

  return <DashboardShell userEmail={user.email}>{children}</DashboardShell>;
}
