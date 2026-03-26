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
          <Badge>Placeholder page</Badge>
          <SectionHeader description={description} eyebrow="Workspace" title={title} />
        </div>
      </DashboardCard>
      <div className="dashboard-grid">
        <DashboardCard
          description="This area will receive real product modules when the corresponding feature work begins."
          title="Current scope"
        />
        <DashboardCard title="Next implementation">
          <ul className="list-copy">
            <li>Replace placeholder text with feature-specific UI.</li>
            <li>Connect the page to shared contracts and API data.</li>
            <li>Keep the branded surface system consistent across flows.</li>
          </ul>
        </DashboardCard>
      </div>
    </>
  );
}
