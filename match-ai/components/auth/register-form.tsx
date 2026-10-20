"use client";

import Link from "next/link";
import { useMemo } from "react";
import { Button } from "@/components/ui/button";
import { FieldError } from "@/components/ui/label";
import { useAuthForm } from "@/hooks/use-auth-form";
import { useMessages } from "@/hooks/use-messages";
import { signUpAction } from "@/lib/auth/actions";
import { createAuthSchemas } from "@/lib/auth/schemas";
import { FormStatus, PasswordField, TextField } from "./fields";

export function RegisterForm() {
  const m = useMessages();
  const r = m.auth.register;
  const schema = useMemo(() => createAuthSchemas(m).register, [m]);
  const { state, formAction, pending, onSubmit, fieldErrors } = useAuthForm(schema, signUpAction);

  if (state.status === "success") {
    return <FormStatus status="success" message={state.message} />;
  }

  return (
    <form action={formAction} onSubmit={onSubmit} noValidate className="space-y-5">
      <FormStatus status={state.status} message={state.message} />
      <TextField
        name="email"
        type="email"
        label={m.auth.emailLabel}
        placeholder={m.auth.emailPlaceholder}
        autoComplete="email"
        inputMode="email"
        required
        defaultValue={state.email}
        error={fieldErrors.email}
      />
      <PasswordField
        name="password"
        label={m.auth.passwordLabel}
        placeholder={m.auth.passwordPlaceholder}
        autoComplete="new-password"
        required
        minLength={8}
        error={fieldErrors.password}
      />
      <div className="space-y-2">
        <div className="flex items-start gap-3">
          <input
            id="field-terms"
            name="terms"
            type="checkbox"
            required
            aria-invalid={fieldErrors.terms ? true : undefined}
            aria-describedby={fieldErrors.terms ? "field-terms-error" : undefined}
            className="mt-0.5 size-4 shrink-0 rounded border-border-strong bg-transparent accent-[var(--accent)]"
          />
          <label htmlFor="field-terms" className="text-sm leading-relaxed text-muted">
            {r.termsPrefix}{" "}
            <Link href="/terms" className="text-foreground underline underline-offset-4 hover:text-accent-strong">
              {r.termsLink}
            </Link>{" "}
            {r.termsAnd}{" "}
            <Link href="/privacy" className="text-foreground underline underline-offset-4 hover:text-accent-strong">
              {r.privacyLink}
            </Link>
          </label>
        </div>
        <FieldError id="field-terms-error" message={fieldErrors.terms} />
      </div>
      <Button type="submit" size="lg" className="w-full" loading={pending} loadingText={m.common.loading}>
        {r.submit}
      </Button>
    </form>
  );
}
