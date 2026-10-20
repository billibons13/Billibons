import type { Metadata } from "next";
import Link from "next/link";
import { AuthCard } from "@/components/auth/auth-card";
import { ForgotPasswordForm } from "@/components/auth/forgot-password-form";
import { getMessages } from "@/lib/i18n";

const m = getMessages();

export const metadata: Metadata = { title: m.auth.forgot.metaTitle, alternates: { canonical: "/forgot-password" } };

export default function ForgotPasswordPage() {
  const f = m.auth.forgot;
  return (
    <AuthCard
      title={f.title}
      subtitle={f.subtitle}
      footer={
        <Link href="/login" className="font-medium text-foreground underline-offset-4 hover:underline">
          {f.back}
        </Link>
      }
    >
      <ForgotPasswordForm />
    </AuthCard>
  );
}
