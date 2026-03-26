type BadgeProps = {
  children: string;
  tone?: "default" | "success" | "warning" | "error";
};

export function Badge({ children, tone = "default" }: BadgeProps) {
  return <span className={`badge badge--${tone}`}>{children}</span>;
}
