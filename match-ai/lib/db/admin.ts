import "server-only";

import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import { publicEnv } from "@/lib/config/env";
import { serverEnv } from "@/lib/config/server-env";

/**
 * Service-role client — BYPASSES RLS. Server-only, for trusted jobs such as
 * Stripe webhooks, usage accounting and image retention cleanup.
 * Never use it with user-controlled filters without an explicit user_id check.
 */
export function createSupabaseAdminClient(): SupabaseClient | null {
  if (!publicEnv.supabaseUrl || !serverEnv.supabaseServiceRoleKey) return null;
  return createClient(publicEnv.supabaseUrl, serverEnv.supabaseServiceRoleKey, {
    auth: { autoRefreshToken: false, persistSession: false },
  });
}
