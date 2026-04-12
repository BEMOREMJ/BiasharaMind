import { signOutAction } from "@/app/actions/auth";

type SignOutButtonProps = {
  fullWidth?: boolean;
  variant?: "primary" | "secondary";
};

export function SignOutButton({
  fullWidth = false,
  variant = "secondary",
}: SignOutButtonProps) {
  return (
    <form action={signOutAction}>
      <button
        className={`button button--${variant}${fullWidth ? " button--full-width" : ""}`}
        type="submit"
      >
        Sign out
      </button>
    </form>
  );
}
