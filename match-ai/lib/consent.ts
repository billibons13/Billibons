/**
 * Cookie / analytics consent stored in localStorage. Every access is wrapped in
 * try/catch: storage can be unavailable (private mode, blocked site data).
 */
export type ConsentValue = "essential" | "analytics";

export const CONSENT_STORAGE_KEY = "cookie-consent:v1";
export const CONSENT_EVENT = "cookie-consent-change";

/** In-memory fallback when localStorage is unavailable. */
let memoryConsent: ConsentValue | null = null;

export function readConsent(): ConsentValue | null {
  if (typeof window === "undefined") return null;
  try {
    const value = window.localStorage.getItem(CONSENT_STORAGE_KEY);
    return value === "essential" || value === "analytics" ? value : memoryConsent;
  } catch {
    return memoryConsent;
  }
}

export function writeConsent(value: ConsentValue): void {
  if (typeof window === "undefined") return;
  memoryConsent = value;
  try {
    window.localStorage.setItem(CONSENT_STORAGE_KEY, value);
  } catch {
    // Storage unavailable — the choice applies to this page view only.
  }
  window.dispatchEvent(new CustomEvent<ConsentValue>(CONSENT_EVENT, { detail: value }));
}

export function clearConsent(): void {
  if (typeof window === "undefined") return;
  memoryConsent = null;
  try {
    window.localStorage.removeItem(CONSENT_STORAGE_KEY);
  } catch {
    // ignore
  }
  window.dispatchEvent(new CustomEvent(CONSENT_EVENT, { detail: null }));
}

export function hasAnalyticsConsent(): boolean {
  return readConsent() === "analytics";
}
