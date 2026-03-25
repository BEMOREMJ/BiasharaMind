import Link from "next/link";

import { PageContainer } from "@/components/page-container";

export default function LandingPage() {
  return (
    <PageContainer>
      <section className="hero">
        <span className="eyebrow">V1 Placeholder</span>
        <h1>BiasharaMind helps SMEs identify gaps and plan the next 90 days.</h1>
        <p>
          This landing page placeholder marks the future marketing entry point for
          onboarding, positioning, and product conversion.
        </p>
        <div className="hero-actions">
          <Link className="button-link button-link--primary" href="/signup">
            Create account
          </Link>
          <Link className="button-link button-link--secondary" href="/login">
            Log in
          </Link>
        </div>
      </section>
    </PageContainer>
  );
}
