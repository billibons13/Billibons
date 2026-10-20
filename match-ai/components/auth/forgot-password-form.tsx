"use client";

import { useMemo } from "react";
import { Button } from "@/components/ui/button";
import { useAuthForm } from "@/hooks/use-auth-form";
import { useMessages } from "@/hooks/use-messages";
import { forgotPasswordAction } from "@/lib/auth/actions";
import { createAuthSchemas } from "@/lib/auth/schemas";
import { FormStatus, TextField } from "./fields";

export function ForgotPasswordForm() {
  const m = useMessages();
  const schema = useMemo(() => createAuthSchemas(m).forgot, [m]);
  const { state, formAction, pending, onSubmit, fieldErrors } = useAuthForm(schema, forgotPasswordAction);

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
      <Button type="submit" size="lg" className="w-full" loading={pending} loadingText={m.common.loading}>
        {m.auth.forgot.submit}
      </Button>
    </form>
  );
}
