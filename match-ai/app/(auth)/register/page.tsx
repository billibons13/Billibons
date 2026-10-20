import type { Metadata } from "next";
import Link from "next/link";
import { AuthCard } from "@/components/auth/auth-card";
import { RegisterForm } from "@/components/auth/register-form";
import { PLAN_LIMITS } from "@/lib/config/plans";
import { format, getMessages } from "@/lib/i18n";

const m = getMessages();

export const metadata: Metadata = { title: m.auth.register.metaTitle, alternates: { canonical: "/register" } };

export default function RegisterPage() {
  const r = m.auth.register;
  return (
    <AuthCard
      title={r.title}
      subtitle={format(r.subtitle, { count: PLAN_LIMITS.free })}
      footer={
        <>
          {r.hasAccount}{" "}
          <Link href="/login" className="font-medium text-foreground underline-offset-4 hover:underline">
            {r.loginLink}
          </Link>
        </>
      }
    >
      <RegisterForm />
    </AuthCard>
  );
}
