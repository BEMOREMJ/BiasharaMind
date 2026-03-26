import type { ReactNode } from "react";

type DashboardCardProps = {
  children?: ReactNode;
  description?: string;
  title: string;
  tone?: "default" | "hero";
};

export function DashboardCard({
  children,
  description,
  title,
  tone = "default",
}: DashboardCardProps) {
  const className = tone === "hero" ? "dashboard-card dashboard-card--hero" : "dashboard-card";

  return (
    <section className={className}>
      <h2 className="card-title">{title}</h2>
      {description ? <p className="card-description">{description}</p> : null}
      {children}
    </section>
  );
}
