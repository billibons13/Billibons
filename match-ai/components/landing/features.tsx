import { Gauge, History, LayoutDashboard, ListTree, ScanEye, Trophy } from "lucide-react";
import { Container, Section, SectionHeader } from "@/components/ui/container";
import { getMessages } from "@/lib/i18n";

export function Features() {
  const f = getMessages().landing.features;
  const items = [
    { icon: ScanEye, ...f.items.vision },
    { icon: Trophy, ...f.items.recognition },
    { icon: ListTree, ...f.items.structured },
    { icon: Gauge, ...f.items.confidence },
    { icon: History, ...f.items.history },
    { icon: LayoutDashboard, ...f.items.dashboard },
  ];

  return (
    <Section id="features" aria-labelledby="features-title">
      <Container>
        <SectionHeader id="features-title" eyebrow={f.eyebrow} title={f.title} subtitle={f.subtitle} />
        <ul className="mt-16 grid gap-px overflow-hidden rounded-2xl border border-border bg-border sm:grid-cols-2 lg:grid-cols-3">
          {items.map(({ icon: Icon, title, text }) => (
            <li key={title} className="bg-background p-7 transition-colors hover:bg-surface">
              <span className="inline-flex size-10 items-center justify-center rounded-xl border border-accent/20 bg-accent/10">
                <Icon className="size-5 text-accent-strong" aria-hidden="true" />
              </span>
              <h3 className="mt-5 font-display text-base font-semibold tracking-tight">{title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted">{text}</p>
            </li>
          ))}
        </ul>
      </Container>
    </Section>
  );
}
