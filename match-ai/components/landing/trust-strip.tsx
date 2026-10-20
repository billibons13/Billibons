import { BrainCircuit, LayoutList, ShieldCheck, Zap } from "lucide-react";
import { Container } from "@/components/ui/container";
import { getMessages } from "@/lib/i18n";

export function TrustStrip() {
  const t = getMessages().landing.trust;
  const items = [
    { icon: BrainCircuit, ...t.items.ai },
    { icon: Zap, ...t.items.fast },
    { icon: LayoutList, ...t.items.structured },
    { icon: ShieldCheck, ...t.items.secure },
  ];

  return (
    <section aria-label={t.label} className="border-y border-border bg-surface/40">
      <Container>
        <ul className="grid grid-cols-1 gap-px py-3 min-[480px]:grid-cols-2 sm:py-0 lg:grid-cols-4">
          {items.map(({ icon: Icon, title, text }) => (
            <li key={title} className="flex items-start gap-3 px-1 py-3 sm:px-6 sm:py-7">
              <span className="mt-0.5 inline-flex size-9 shrink-0 items-center justify-center rounded-xl border border-border bg-white/[0.03]">
                <Icon className="size-4 text-accent-strong" aria-hidden="true" />
              </span>
              <div>
                <p className="text-sm font-semibold">{title}</p>
                <p className="mt-0.5 text-sm text-muted">{text}</p>
              </div>
            </li>
          ))}
        </ul>
      </Container>
    </section>
  );
}
