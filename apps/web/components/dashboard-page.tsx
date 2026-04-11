import { Badge } from "@/components/badge";
import { DashboardCard } from "@/components/dashboard-card";
import { SectionHeader } from "@/components/section-header";

type DashboardPageProps = {
  description: string;
  title: string;
};

export function DashboardPage({ description, title }: DashboardPageProps) {
  return (
    <>
      <DashboardCard tone="hero" title={title}>
        <div className="dashboard-stack">
          <Badge>Business workspace</Badge>
          <SectionHeader description={description} eyebrow="Workspace" title={title} />
        </div>
      </DashboardCard>
      <div className="dashboard-grid">
        <DashboardCard
          description="Review the latest information available in this workspace and keep your business priorities in view."
          title="Current focus"
        />
        <DashboardCard title="What you can expect here">
          <ul className="list-copy">
            <li>See recent business activity and saved outputs in one place.</li>
            <li>Track how your priorities change over time.</li>
            <li>Stay aligned on the next actions that support steady growth.</li>
          </ul>
        </DashboardCard>
      </div>
    </>
  );
}
