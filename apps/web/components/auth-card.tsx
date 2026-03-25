type AuthCardProps = {
  title: string;
  description: string;
};

export function AuthCard({ title, description }: AuthCardProps) {
  return (
    <section className="auth-shell">
      <span className="eyebrow">Auth</span>
      <h1>{title}</h1>
      <p>{description}</p>
    </section>
  );
}
