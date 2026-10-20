import "server-only";

import { createSupabaseServerClient } from "@/lib/db/server";

export interface CurrentUser {
  id: string;
  email: string | null;
  createdAt: string | null;
}

/**
 * Data Access Layer: the single place that reads the authenticated user.
 * Uses getUser() (verifies the JWT with Supabase) rather than getSession().
 * Returns null when Supabase is not configured or nobody is signed in.
 */
export async function getCurrentUser(): Promise<CurrentUser | null> {
  const supabase = await createSupabaseServerClient();
  if (!supabase) return null;
  const { data, error } = await supabase.auth.getUser();
  if (error || !data.user) return null;
  return { id: data.user.id, email: data.user.email ?? null, createdAt: data.user.created_at ?? null };
}
