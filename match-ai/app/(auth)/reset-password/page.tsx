import type { Metadata } from "next";
import { AuthCard } from "@/components/auth/auth-card";
import { ResetPasswordForm } from "@/components/auth/reset-password-form";
import { getMessages } from "@/lib/i18n";

const m = getMessages();

export const metadata: Metadata = { title: m.auth.reset.metaTitle, robots: { index: false } };

/** Reached from the password-reset email via /auth/callback?next=/reset-password. */
export default function ResetPasswordPage() {
  return (
    <AuthCard title={m.auth.reset.title} subtitle={m.auth.reset.subtitle}>
      <ResetPasswordForm />
    </AuthCard>
  );
}
