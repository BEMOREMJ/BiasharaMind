import { Badge } from "@/components/badge";
import { InputField } from "@/components/input-field";
import { PrimaryButton } from "@/components/primary-button";
import { SecondaryButton } from "@/components/secondary-button";
import { SectionHeader } from "@/components/section-header";

type AuthCardProps = {
  description: string;
  title: string;
};

export function AuthCard({ description, title }: AuthCardProps) {
  const fieldPrefix = title.toLowerCase().replace(/\s+/g, "-");

  return (
    <section className="auth-card">
      <div className="auth-stack">
        <Badge>Account access</Badge>
        <SectionHeader description={description} eyebrow="BiasharaMind" title={title} />
      </div>
      <div className="auth-card__form" aria-hidden="true">
        <InputField
          autoComplete="email"
          hint="Authentication is not available in this preview yet."
          id={`${fieldPrefix}-email`}
          label="Email"
          placeholder="owner@business.com"
          type="email"
        />
        <InputField
          autoComplete="current-password"
          id={`${fieldPrefix}-password`}
          label="Password"
          placeholder="Enter password"
          type="password"
        />
        <div className="button-row">
          <PrimaryButton>{title}</PrimaryButton>
          <SecondaryButton href="/">Back to home</SecondaryButton>
        </div>
      </div>
    </section>
  );
}
