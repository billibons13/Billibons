import type { ReactNode } from "react";
import { Info } from "lucide-react";
import { isSupabaseConfigured } from "@/lib/config/env";
import { getMessages } from "@/lib/i18n";

export function AuthCard({
  title,
  subtitle,
  children,
  footer,
}: {
  title: string;
  subtitle?: string;
  children: ReactNode;
  footer?: ReactNode;
}) {
  const m = getMessages();
  return (
    <div className="w-full max-w-md">
      <div className="glass rounded-[1.6rem] bg-surface/70 p-6 shadow-glow-soft sm:p-8">
        <h1 className="font-display text-2xl font-semibold tracking-tight sm:text-[1.7rem]">{title}</h1>
        {subtitle ? <p className="mt-2 text-sm leading-relaxed text-muted">{subtitle}</p> : null}
        {!isSupabaseConfigured() ? (
          <p role="note" className="mt-5 flex gap-2.5 rounded-xl border border-warning/25 bg-warning/[0.06] p-3.5 text-sm leading-relaxed text-foreground/90">
            <Info className="mt-0.5 size-4 shrink-0 text-warning" aria-hidden="true" />
            {m.auth.notConfiguredNotice}
          </p>
        ) : null}
        <div className="mt-7">{children}</div>
      </div>
      {footer ? <div className="mt-6 text-center text-sm text-muted">{footer}</div> : null}
    </div>
  );
}
