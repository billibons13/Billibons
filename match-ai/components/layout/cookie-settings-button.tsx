"use client";

import { useMessages } from "@/hooks/use-messages";
import { clearConsent } from "@/lib/consent";

/** Re-opens the cookie banner so the user can change or withdraw consent. */
export function CookieSettingsButton({ className }: { className?: string }) {
  const m = useMessages();
  return (
    <button type="button" className={className} onClick={() => clearConsent()}>
      {m.footer.cookieSettings}
    </button>
  );
}
