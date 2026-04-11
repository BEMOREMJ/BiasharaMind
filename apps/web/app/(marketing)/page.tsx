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
            <Badge>Built for growing SMEs</Badge>
            <SectionHeader
              description="Get clear business insights, focused priorities, and a practical action plan tailored to how your business operates today."
              eyebrow="Practical business guidance"
              title="BiasharaMind helps businesses see what matters, fix what slows growth, and plan the next 90 days."
            />
            <div className="hero__actions">
              <PrimaryButton href="/signup">Create account</PrimaryButton>
              <SecondaryButton href="/login">Log in</SecondaryButton>
            </div>
          </div>
        </section>
        <div className="info-grid">
          <DashboardCard
            description="Capture the key details about your business so BiasharaMind can understand your current operations, challenges, and growth context."
            title="Clear business inputs"
          />
          <DashboardCard
            description="Turn assessment responses into clear strengths, risks, and priority areas your business can act on with confidence."
            title="Actionable insights"
          />
          <DashboardCard
            description="From assessment to roadmap, BiasharaMind is designed to help SMEs make smarter decisions and move forward step by step."
            title="Built for steady growth"
          />
        </div>
      </div>
    </PageContainer>
  );
}
