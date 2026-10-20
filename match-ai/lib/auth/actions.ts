"use server";

import { redirect } from "next/navigation";
import { getAppUrl } from "@/lib/config/env";
import { createSupabaseServerClient } from "@/lib/db/server";
import { getMessages } from "@/lib/i18n";
import {
  createAuthSchemas,
  firstFieldErrors,
  formDataToObject,
  type AuthActionState,
} from "./schemas";

const messages = getMessages();

function notConfigured(): AuthActionState {
  return { status: "error", message: messages.auth.notConfigured, notConfigured: true };
}

function genericError(): AuthActionState {
  return { status: "error", message: messages.auth.genericError };
}

async function signIn(_prev: AuthActionState, formData: FormData): Promise<AuthActionState> {
  const parsed = createAuthSchemas().login.safeParse(formDataToObject(formData));
  if (!parsed.success) return { status: "error", fieldErrors: firstFieldErrors(parsed.error) };

  const supabase = await createSupabaseServerClient();
  if (!supabase) return notConfigured();

  const { error } = await supabase.auth.signInWithPassword(parsed.data);
  if (error) {
    return {
      status: "error",
      message: error.code === "invalid_credentials" ? messages.auth.invalidCredentials : messages.auth.genericError,
    };
  }
  redirect("/dashboard");
}

async function signUp(_prev: AuthActionState, formData: FormData): Promise<AuthActionState> {
  const parsed = createAuthSchemas().register.safeParse(formDataToObject(formData));
  if (!parsed.success) return { status: "error", fieldErrors: firstFieldErrors(parsed.error) };

  const supabase = await createSupabaseServerClient();
  if (!supabase) return notConfigured();

  const { data, error } = await supabase.auth.signUp({
    email: parsed.data.email,
    password: parsed.data.password,
    options: { emailRedirectTo: `${getAppUrl()}/auth/callback?next=/dashboard` },
  });
  if (error) return genericError();

  // With email confirmation enabled Supabase returns no session yet.
  if (!data.session) return { status: "success", message: messages.auth.register.checkEmail };
  redirect("/dashboard");
}

async function forgotPassword(
  _prev: AuthActionState,
  formData: FormData,
): Promise<AuthActionState> {
  const parsed = createAuthSchemas().forgot.safeParse(formDataToObject(formData));
  if (!parsed.success) return { status: "error", fieldErrors: firstFieldErrors(parsed.error) };

  const supabase = await createSupabaseServerClient();
  if (!supabase) return notConfigured();

  const { error } = await supabase.auth.resetPasswordForEmail(parsed.data.email, {
    redirectTo: `${getAppUrl()}/auth/callback?next=/reset-password`,
  });
  // Rate-limit errors are surfaced; "user not found" is never revealed.
  if (error && error.status === 429) return genericError();
  return { status: "success", message: messages.auth.forgot.sent };
}

async function resetPassword(
  _prev: AuthActionState,
  formData: FormData,
): Promise<AuthActionState> {
  const parsed = createAuthSchemas().reset.safeParse(formDataToObject(formData));
  if (!parsed.success) return { status: "error", fieldErrors: firstFieldErrors(parsed.error) };

  const supabase = await createSupabaseServerClient();
  if (!supabase) return notConfigured();

  const { data: userData } = await supabase.auth.getUser();
  if (!userData.user) return { status: "error", message: messages.auth.sessionExpired };

  const { error } = await supabase.auth.updateUser({ password: parsed.data.password });
  if (error) return genericError();
  return { status: "success", message: messages.auth.reset.success };
}

/** Echo the email back so the form keeps it after React resets the form. */
async function withEmail(
  run: (prev: AuthActionState, formData: FormData) => Promise<AuthActionState>,
  prev: AuthActionState,
  formData: FormData,
): Promise<AuthActionState> {
  const state = await run(prev, formData);
  const email = formData.get("email");
  return typeof email === "string" ? { ...state, email: email.slice(0, 254) } : state;
}

export async function signInAction(prev: AuthActionState, formData: FormData) {
  return withEmail(signIn, prev, formData);
}

export async function signUpAction(prev: AuthActionState, formData: FormData) {
  return withEmail(signUp, prev, formData);
}

export async function forgotPasswordAction(prev: AuthActionState, formData: FormData) {
  return withEmail(forgotPassword, prev, formData);
}

export async function resetPasswordAction(prev: AuthActionState, formData: FormData) {
  return withEmail(resetPassword, prev, formData);
}

export async function signOutAction(): Promise<void> {
  const supabase = await createSupabaseServerClient();
  if (supabase) await supabase.auth.signOut();
  redirect("/login");
}
