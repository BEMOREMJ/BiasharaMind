import Link from "next/link";
import type { ButtonHTMLAttributes, ReactNode } from "react";

type SecondaryButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  children: ReactNode;
  href?: string;
};

export function SecondaryButton({
  children,
  href,
  type = "button",
  ...props
}: SecondaryButtonProps) {
  if (href) {
    return (
      <Link className="button button--secondary" href={href}>
        {children}
      </Link>
    );
  }

  return (
    <button className="button button--secondary" type={type} {...props}>
      {children}
    </button>
  );
}
