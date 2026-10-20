"use client";

import Link from "next/link";
import { Cookie } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useConsent } from "@/hooks/use-consent";
import { useMessages } from "@/hooks/use-messages";
import { writeConsent, type ConsentValue } from "@/lib/consent";
import { useToast } from "@/components/ui/toast";

/**
 * Minimal consent banner: only essential storage by default; analytics are
 * enabled only after "Accept analytics" (see lib/analytics).
 */
export function CookieConsent() {
  const consent = useConsent();
  const m = useMessages();
  const { toast } = useToast();

  function choose(value: ConsentValue) {
    writeConsent(value);
    toast({ variant: "success", title: m.cookies.saved });
  }

  // undefined = not hydrated yet; a value = decision already made.
  if (consent !== null) return null;

  return (
    <section
      aria-label={m.cookies.regionLabel}
      className="fixed inset-x-0 bottom-0 z-50 p-3 sm:bottom-4 sm:left-4 sm:right-auto sm:p-0"
    >
      <div className="w-full animate-fade-up rounded-2xl border border-border-strong bg-surface-2 p-5 shadow-card sm:max-w-md">
        <div className="flex items-start gap-3">
          <Cookie className="mt-0.5 size-5 shrink-0 text-accent-strong" aria-hidden="true" />
          <div>
            <h2 className="text-sm font-semibold">{m.cookies.title}</h2>
            <p className="mt-1.5 text-sm leading-relaxed text-muted">
              {m.cookies.body}{" "}
              <Link href="/privacy" className="text-foreground underline underline-offset-4 hover:text-accent-strong">
                {m.cookies.learnMore}
              </Link>
            </p>
          </div>
        </div>
        <div className="mt-4 flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
          <Button variant="secondary" size="sm" onClick={() => choose("essential")}>
            {m.cookies.essentialOnly}
          </Button>
          <Button variant="secondary" size="sm" onClick={() => choose("analytics")}>
            {m.cookies.acceptAll}
          </Button>
        </div>
      </div>
    </section>
  );
}
