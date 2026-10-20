import { hasAnalyticsConsent } from "@/lib/consent";
import { createPosthogAdapter } from "./posthog";

export const ANALYTICS_EVENTS = [
  "signup",
  "login",
  "analysis_started",
  "analysis_completed",
  "analysis_failed",
  "upgrade_clicked",
  "subscription_started",
] as const;

export type AnalyticsEvent = (typeof ANALYTICS_EVENTS)[number];
export type AnalyticsProps = Record<string, string | number | boolean | null>;

export interface AnalyticsAdapter {
  capture(event: AnalyticsEvent, props: AnalyticsProps): void;
}

let adapter: AnalyticsAdapter | null | undefined;

function getAdapter(): AnalyticsAdapter | null {
  if (adapter === undefined) adapter = createPosthogAdapter();
  return adapter;
}

/** Test hook / alternative providers. Pass null to disable. */
export function setAnalyticsAdapter(next: AnalyticsAdapter | null): void {
  adapter = next;
}

/**
 * Provider-agnostic tracking. No-op unless (a) running in the browser,
 * (b) an analytics provider is configured and (c) the user consented.
 * Never pass personal data (emails, names, image contents) in props.
 */
export function track(event: AnalyticsEvent, props: AnalyticsProps = {}): void {
  if (typeof window === "undefined") return;
  if (!hasAnalyticsConsent()) return;
  const current = getAdapter();
  if (!current) return;
  try {
    current.capture(event, props);
  } catch {
    // Analytics must never break the product.
  }
}
