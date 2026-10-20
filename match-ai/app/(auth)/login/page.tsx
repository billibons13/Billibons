import type { Metadata } from "next";
import Link from "next/link";
import { AuthCard } from "@/components/auth/auth-card";
import { LoginForm } from "@/components/auth/login-form";
import { getMessages } from "@/lib/i18n";

const m = getMessages();

export const metadata: Metadata = { title: m.auth.login.metaTitle, alternates: { canonical: "/login" } };

export default function LoginPage() {
  const l = m.auth.login;
  return (
    <AuthCard
      title={l.title}
      subtitle={l.subtitle}
      footer={
        <>
          {l.noAccount}{" "}
          <Link href="/register" className="font-medium text-foreground underline-offset-4 hover:underline">
            {l.registerLink}
          </Link>
        </>
      }
    >
      <LoginForm />
    </AuthCard>
  );
}
