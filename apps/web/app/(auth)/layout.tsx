import type { ReactNode } from "react";
import { redirect } from "next/navigation";

import { getAuthenticatedUser } from "@/lib/supabase/server";

type AuthLayoutProps = {
  children: ReactNode;
};

export default async function AuthLayout({ children }: AuthLayoutProps) {
  const user = await getAuthenticatedUser();

  if (user) {
    redirect("/dashboard");
  }

  return <main className="auth-layout">{children}</main>;
}
