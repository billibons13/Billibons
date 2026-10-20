/**
 * Central access to environment variables.
 *
 * `NEXT_PUBLIC_*` values must be read with literal `process.env.NAME` access so
 * Next.js can inline them into the client bundle. Server-only values live in
 * `lib/config/server-env.ts` and must never be imported from client code.
 */

const DEFAULT_APP_URL = "http://localhost:3000";

function clean(value: string | undefined): string | undefined {
  const trimmed = value?.trim();
  return trimmed ? trimmed : undefined;
}

export const publicEnv = {
  appUrl: clean(process.env.NEXT_PUBLIC_APP_URL),
  supabaseUrl: clean(process.env.NEXT_PUBLIC_SUPABASE_URL),
  supabaseAnonKey: clean(process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY),
  posthogKey: clean(process.env.NEXT_PUBLIC_POSTHOG_KEY),
  posthogHost: clean(process.env.NEXT_PUBLIC_POSTHOG_HOST),
  planCurrency: clean(process.env.NEXT_PUBLIC_PLAN_CURRENCY),
  planPricePro: clean(process.env.NEXT_PUBLIC_PLAN_PRICE_PRO),
  planPricePremium: clean(process.env.NEXT_PUBLIC_PLAN_PRICE_PREMIUM),
} as const;

/** Absolute app URL (no trailing slash). Falls back to localhost when unset or invalid. */
export function getAppUrl(raw: string | undefined = publicEnv.appUrl): string {
  if (!raw) return DEFAULT_APP_URL;
  try {
    const url = new URL(raw);
    if (url.protocol !== "http:" && url.protocol !== "https:") return DEFAULT_APP_URL;
    return url.origin;
  } catch {
    return DEFAULT_APP_URL;
  }
}

/** True when both public Supabase variables are present. */
export function isSupabaseConfigured(): boolean {
  return Boolean(publicEnv.supabaseUrl && publicEnv.supabaseAnonKey);
}

/** Parses a positive number from an env string, otherwise returns the fallback. */
export function parsePositiveNumber(raw: string | undefined, fallback: number): number {
  if (raw === undefined || raw.trim() === "") return fallback;
  const value = Number(raw);
  return Number.isFinite(value) && value > 0 ? value : fallback;
}
