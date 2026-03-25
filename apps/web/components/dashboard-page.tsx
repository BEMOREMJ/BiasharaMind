type DashboardPageProps = {
  title: string;
  description: string;
};

export function DashboardPage({ title, description }: DashboardPageProps) {
  return (
    <section className="dashboard-content">
      <span className="eyebrow">Dashboard</span>
      <h1>{title}</h1>
      <p>{description}</p>
    </section>
  );
}
