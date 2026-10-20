import { z } from "zod";
import { getMessages, type Messages } from "@/lib/i18n";

/** Zod schemas shared by client-side validation and server actions. */
export function createAuthSchemas(messages: Messages = getMessages()) {
  const v = messages.auth.validation;

  const email = z
    .string({ error: v.emailRequired })
    .trim()
    .min(1, { error: v.emailRequired })
    .max(254, { error: v.emailInvalid })
    .pipe(z.email({ error: v.emailInvalid }));

  const newPassword = z
    .string({ error: v.passwordRequired })
    .min(1, { error: v.passwordRequired })
    .min(8, { error: v.passwordMin })
    .max(72, { error: v.passwordMax });

  const login = z.object({
    email,
    password: z.string({ error: v.passwordRequired }).min(1, { error: v.passwordRequired }),
  });

  const register = z.object({
    email,
    password: newPassword,
    terms: z.literal("on", { error: v.termsRequired }),
  });

  const forgot = z.object({ email });

  const reset = z
    .object({ password: newPassword, confirmPassword: z.string() })
    .refine((data) => data.password === data.confirmPassword, {
      path: ["confirmPassword"],
      error: v.passwordsMismatch,
    });

  return { login, register, forgot, reset };
}

export type AuthFormName = keyof ReturnType<typeof createAuthSchemas>;

export type FieldErrors = Partial<Record<string, string>>;

/** Converts a FormData into a plain object of string values. */
export function formDataToObject(formData: FormData): Record<string, string> {
  const out: Record<string, string> = {};
  for (const [key, value] of formData.entries()) {
    if (typeof value === "string") out[key] = value;
  }
  return out;
}

export function firstFieldErrors(error: z.ZodError): FieldErrors {
  const out: FieldErrors = {};
  for (const issue of error.issues) {
    const key = String(issue.path[0] ?? "form");
    out[key] ??= issue.message;
  }
  return out;
}

export interface AuthActionState {
  status: "idle" | "error" | "success";
  message?: string;
  fieldErrors?: FieldErrors;
  /** True when the failure is because Supabase env vars are missing. */
  notConfigured?: boolean;
  /** Submitted email, echoed back so the field is not cleared. */
  email?: string;
}

export const initialAuthState: AuthActionState = { status: "idle" };
