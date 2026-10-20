"use client";

import { createBrowserClient } from "@supabase/ssr";
import type { SupabaseClient } from "@supabase/supabase-js";
import { isSupabaseConfigured, publicEnv } from "@/lib/config/env";

let client: SupabaseClient | null = null;

/** Browser Supabase client (anon key, RLS applies). Null when not configured. */
export function getSupabaseBrowserClient(): SupabaseClient | null {
  if (!isSupabaseConfigured()) return null;
  client ??= createBrowserClient(publicEnv.supabaseUrl!, publicEnv.supabaseAnonKey!);
  return client;
}
