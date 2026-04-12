"use client";

import { useRouter } from "next/navigation";
import { useMemo, useState, type FormEvent } from "react";

import { Badge } from "@/components/badge";
import { InputField } from "@/components/input-field";
import { PrimaryButton } from "@/components/primary-button";
import { SecondaryButton } from "@/components/secondary-button";
import { SectionHeader } from "@/components/section-header";
import { getSupabaseBrowserClient } from "@/lib/supabase/browser";

type AuthMode = "login" | "signup";

type AuthCardProps = {
  description: string;
  mode: AuthMode;
  title: string;
};

function readAuthErrorMessage(error: unknown, fallback: string): string {
  if (error instanceof Error && error.message.trim()) {
    return error.message;
  }

  return fallback;
}

export function AuthCard({ description, mode, title }: AuthCardProps) {
  const router = useRouter();
  const supabase = useMemo(() => getSupabaseBrowserClient(), []);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const isSignup = mode === "signup";

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitting(true);
    setErrorMessage(null);
    setStatusMessage(null);

    try {
      if (isSignup && password !== confirmPassword) {
        throw new Error("Passwords do not match.");
      }

      if (isSignup) {
        const { data, error } = await supabase.auth.signUp({
          email: email.trim(),
          password,
        });

        if (error) {
          throw error;
        }

        if (data.session) {
          setStatusMessage("Account created. Redirecting to your workspace...");
          router.replace("/dashboard");
          router.refresh();
          return;
        }

        setStatusMessage(
          "Account created. If email confirmation is enabled in Supabase, check your inbox before logging in.",
        );
        setPassword("");
        setConfirmPassword("");
        return;
      }

      const { error } = await supabase.auth.signInWithPassword({
        email: email.trim(),
        password,
      });

      if (error) {
        throw error;
      }

      setStatusMessage("Signed in successfully. Redirecting to your workspace...");
      router.replace("/dashboard");
      router.refresh();
    } catch (error) {
      setErrorMessage(
        readAuthErrorMessage(
          error,
          isSignup ? "Unable to create your account." : "Unable to sign you in.",
        ),
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section className="auth-card">
      <div className="auth-stack">
        <Badge>Account access</Badge>
        <SectionHeader description={description} eyebrow="BiasharaMind" title={title} />
      </div>

      <form className="auth-card__form" onSubmit={handleSubmit}>
        <InputField
          autoComplete="email"
          id={`${mode}-email`}
          label="Email"
          onChange={(event) => setEmail(event.target.value)}
          placeholder="owner@business.com"
          required
          type="email"
          value={email}
        />
        <InputField
          autoComplete={isSignup ? "new-password" : "current-password"}
          id={`${mode}-password`}
          label="Password"
          minLength={8}
          onChange={(event) => setPassword(event.target.value)}
          placeholder="Enter password"
          required
          type="password"
          value={password}
        />
        {isSignup ? (
          <InputField
            autoComplete="new-password"
            id="signup-confirm-password"
            label="Confirm password"
            minLength={8}
            onChange={(event) => setConfirmPassword(event.target.value)}
            placeholder="Re-enter password"
            required
            type="password"
            value={confirmPassword}
          />
        ) : null}

        {(statusMessage || errorMessage) && (
          <div
            className={`status-banner ${
              errorMessage ? "status-banner--error" : "status-banner--success"
            }`}
          >
            {errorMessage ?? statusMessage}
          </div>
        )}

        <div className="button-row">
          <PrimaryButton disabled={isSubmitting} type="submit">
            {isSubmitting ? (isSignup ? "Creating account..." : "Signing in...") : title}
          </PrimaryButton>
          <SecondaryButton href="/">Back to home</SecondaryButton>
        </div>
      </form>
    </section>
  );
}
