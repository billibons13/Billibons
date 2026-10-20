"use client";

import { useMemo } from "react";
import { ButtonLink, Button } from "@/components/ui/button";
import { useAuthForm } from "@/hooks/use-auth-form";
import { useMessages } from "@/hooks/use-messages";
import { resetPasswordAction } from "@/lib/auth/actions";
import { createAuthSchemas } from "@/lib/auth/schemas";
import { FormStatus, PasswordField } from "./fields";

export function ResetPasswordForm() {
  const m = useMessages();
  const schema = useMemo(() => createAuthSchemas(m).reset, [m]);
  const { state, formAction, pending, onSubmit, fieldErrors } = useAuthForm(schema, resetPasswordAction);

  if (state.status === "success") {
    return (
      <div className="space-y-5">
        <FormStatus status="success" message={state.message} />
        <ButtonLink href="/dashboard" size="lg" className="w-full">
          {m.nav.dashboard}
        </ButtonLink>
      </div>
    );
  }

  return (
    <form action={formAction} onSubmit={onSubmit} noValidate className="space-y-5">
      <FormStatus status={state.status} message={state.message} />
      <PasswordField
        name="password"
        label={m.auth.passwordLabel}
        placeholder={m.auth.passwordPlaceholder}
        autoComplete="new-password"
        required
        minLength={8}
        error={fieldErrors.password}
      />
      <PasswordField
        name="confirmPassword"
        label={m.auth.confirmPasswordLabel}
        autoComplete="new-password"
        required
        error={fieldErrors.confirmPassword}
      />
      <Button type="submit" size="lg" className="w-full" loading={pending} loadingText={m.common.loading}>
        {m.auth.reset.submit}
      </Button>
    </form>
  );
}
