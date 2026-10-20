"use client";

import { useActionState, useState, type FormEvent } from "react";
import type { z } from "zod";
import {
  firstFieldErrors,
  formDataToObject,
  initialAuthState,
  type AuthActionState,
  type FieldErrors,
} from "@/lib/auth/schemas";

type AuthAction = (prev: AuthActionState, formData: FormData) => Promise<AuthActionState>;

/**
 * Wires a zod schema (client-side validation) to a server action
 * (authoritative validation + Supabase call). Server messages are rendered
 * inline by <FormStatus> (role="alert"), so no extra toast is shown.
 */
export function useAuthForm(schema: z.ZodType, action: AuthAction) {
  const [state, formAction, pending] = useActionState(action, initialAuthState);
  const [clientErrors, setClientErrors] = useState<FieldErrors | null>(null);
  function onSubmit(event: FormEvent<HTMLFormElement>) {
    const result = schema.safeParse(formDataToObject(new FormData(event.currentTarget)));
    if (!result.success) {
      event.preventDefault();
      const errors = firstFieldErrors(result.error);
      setClientErrors(errors);
      const first = Object.keys(errors)[0];
      if (first) event.currentTarget.querySelector<HTMLElement>(`[name="${first}"]`)?.focus();
      return;
    }
    setClientErrors(null);
  }

  const fieldErrors: FieldErrors = clientErrors ?? state.fieldErrors ?? {};
  return { state, formAction, pending, onSubmit, fieldErrors };
}
