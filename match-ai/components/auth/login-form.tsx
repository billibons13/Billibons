"use client";

import Link from "next/link";
import { useMemo } from "react";
import { Button } from "@/components/ui/button";
import { useAuthForm } from "@/hooks/use-auth-form";
import { useMessages } from "@/hooks/use-messages";
import { signInAction } from "@/lib/auth/actions";
import { createAuthSchemas } from "@/lib/auth/schemas";
import { FormStatus, PasswordField, TextField } from "./fields";

export function LoginForm() {
  const m = useMessages();
  const schema = useMemo(() => createAuthSchemas(m).login, [m]);
  const { state, formAction, pending, onSubmit, fieldErrors } = useAuthForm(schema, signInAction);

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
      <div className="space-y-2">
        <PasswordField
          name="password"
          label={m.auth.passwordLabel}
          autoComplete="current-password"
          required
          error={fieldErrors.password}
        />
        <div className="flex justify-end">
          <Link href="/forgot-password" className="text-sm text-muted underline-offset-4 hover:text-foreground hover:underline">
            {m.auth.login.forgot}
          </Link>
        </div>
      </div>
      <Button type="submit" size="lg" className="w-full" loading={pending} loadingText={m.common.loading}>
        {m.auth.login.submit}
      </Button>
    </form>
  );
}
