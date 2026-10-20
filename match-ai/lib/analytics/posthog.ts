import { publicEnv } from "@/lib/config/env";
import type { AnalyticsAdapter } from "./index";

const DEFAULT_HOST = "https://eu.i.posthog.com";
const ID_KEY = "analytics-anon-id";

function anonymousId(): string {
  try {
    const existing = window.localStorage.getItem(ID_KEY);
    if (existing) return existing;
    const id = crypto.randomUUID();
    window.localStorage.setItem(ID_KEY, id);
    return id;
  } catch {
    return "anonymous";
  }
}

/** Minimal PostHog capture adapter via fetch (no SDK). Null when no key is set. */
export function createPosthogAdapter(): AnalyticsAdapter | null {
  const key = publicEnv.posthogKey;
  if (!key) return null;
  const host = (publicEnv.posthogHost ?? DEFAULT_HOST).replace(/\/$/, "");
  return {
    capture(event, props) {
      void fetch(`${host}/capture/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ api_key: key, event, distinct_id: anonymousId(), properties: props }),
        keepalive: true,
      }).catch(() => undefined);
    },
  };
}
