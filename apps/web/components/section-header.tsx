type SectionHeaderProps = {
  description: string;
  eyebrow?: string;
  title: string;
};

export function SectionHeader({ description, eyebrow, title }: SectionHeaderProps) {
  return (
    <div className="section-header">
      {eyebrow ? <span className="section-header__eyebrow">{eyebrow}</span> : null}
      <h1 className="section-header__title">{title}</h1>
      <p className="section-header__description">{description}</p>
    </div>
  );
}
