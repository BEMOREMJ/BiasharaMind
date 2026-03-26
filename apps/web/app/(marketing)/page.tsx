import { Badge } from "@/components/badge";
import { DashboardCard } from "@/components/dashboard-card";
import { PrimaryButton } from "@/components/primary-button";
import { SecondaryButton } from "@/components/secondary-button";
import { SectionHeader } from "@/components/section-header";
import { PageContainer } from "@/components/page-container";

export default function LandingPage() {
  return (
    <PageContainer>
      <div className="marketing-stack">
        <section className="hero">
          <div className="hero__content">
            <Badge>V1 foundation</Badge>
            <SectionHeader
              description="This is still placeholder product content, but it now sits on the first branded UI layer for BiasharaMind."
              eyebrow="Intelligent business guidance"
              title="BiasharaMind helps SMEs identify gaps and plan the next 90 days."
            />
            <div className="hero__actions">
              <PrimaryButton href="/signup">Create account</PrimaryButton>
              <SecondaryButton href="/login">Log in</SecondaryButton>
            </div>
          </div>
        </section>
        <div className="info-grid">
          <DashboardCard
            description="Structured onboarding and assessment flows will guide businesses through their current operating reality."
            title="Clear input capture"
          />
          <DashboardCard
            description="Results, priorities, and roadmap outputs will align to a calm, actionable product surface."
            title="Trustworthy outputs"
          />
          <DashboardCard
            description="The UI tokens and primitives introduced here are intended to scale into the dashboard experience."
            title="Reusable foundation"
          />
        </div>
      </div>
    </PageContainer>
  );
}
