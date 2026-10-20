import { NextResponse, type NextRequest } from "next/server";
import { createSupabaseServerClient } from "@/lib/db/server";

/** Only allow same-origin relative redirects (prevents open redirects). */
function safeNext(value: string | null): string {
  if (!value || !value.startsWith("/") || value.startsWith("//") || value.startsWith("/\\")) return "/dashboard";
  return value;
}

/**
 * Supabase email links (confirm signup, password reset) land here with a
 * one-time `code` that is exchanged for a session cookie.
 */
export async function GET(request: NextRequest) {
  const { searchParams, origin } = request.nextUrl;
  const code = searchParams.get("code");
  const next = safeNext(searchParams.get("next"));

  const supabase = await createSupabaseServerClient();
  if (!supabase || !code) {
    return NextResponse.redirect(new URL("/login", origin));
  }

  const { error } = await supabase.auth.exchangeCodeForSession(code);
  if (error) {
    return NextResponse.redirect(new URL("/login", origin));
  }
  return NextResponse.redirect(new URL(next, origin));
}
