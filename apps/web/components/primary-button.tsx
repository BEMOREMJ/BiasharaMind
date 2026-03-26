import Link from "next/link";
import type { ButtonHTMLAttributes, ReactNode } from "react";

type PrimaryButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  children: ReactNode;
  href?: string;
};

export function PrimaryButton({ children, href, type = "button", ...props }: PrimaryButtonProps) {
  if (href) {
    return (
      <Link className="button button--primary" href={href}>
        {children}
      </Link>
    );
  }

  return (
    <button className="button button--primary" type={type} {...props}>
      {children}
    </button>
  );
}
