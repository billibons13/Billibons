"use client";

import { useSyncExternalStore } from "react";
import { CONSENT_EVENT, CONSENT_STORAGE_KEY, readConsent, type ConsentValue } from "@/lib/consent";

function subscribe(callback: () => void): () => void {
  const onStorage = (event: StorageEvent) => {
    if (event.key === CONSENT_STORAGE_KEY) callback();
  };
  window.addEventListener(CONSENT_EVENT, callback);
  window.addEventListener("storage", onStorage);
  return () => {
    window.removeEventListener(CONSENT_EVENT, callback);
    window.removeEventListener("storage", onStorage);
  };
}

/** Current consent; `undefined` during SSR / before hydration. */
export function useConsent(): ConsentValue | null | undefined {
  return useSyncExternalStore<ConsentValue | null | undefined>(subscribe, readConsent, () => undefined);
}
