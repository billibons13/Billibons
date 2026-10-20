import { ClipboardCheck, ScanSearch, Upload, Waypoints } from "lucide-react";
import { Container, Section, SectionHeader } from "@/components/ui/container";
import { getMessages } from "@/lib/i18n";

export function HowItWorks() {
  const how = getMessages().landing.how;
  const steps = [
    { icon: Upload, ...how.steps.upload },
    { icon: ScanSearch, ...how.steps.recognize },
    { icon: Waypoints, ...how.steps.analyze },
    { icon: ClipboardCheck, ...how.steps.review },
  ];

  return (
    <Section id="how-it-works" aria-labelledby="how-title">
      <Container>
        <SectionHeader id="how-title" eyebrow={how.eyebrow} title={how.title} subtitle={how.subtitle} />
        <ol className="mt-16 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {steps.map(({ icon: Icon, title, text }, index) => (
            <li
              key={title}
              className="group glass relative overflow-hidden rounded-2xl p-6 transition-colors hover:border-border-strong"
            >
              <div
                aria-hidden="true"
                className="absolute -right-10 -top-10 size-32 rounded-full bg-[radial-gradient(closest-side,rgb(139_147_255/0.14),transparent)] opacity-0 transition-opacity duration-500 group-hover:opacity-100"
              />
              <div className="flex items-center justify-between">
                <span className="font-display text-sm font-semibold tabular-nums text-accent-strong">
                  {String(index + 1).padStart(2, "0")}
                </span>
                <Icon className="size-5 text-muted" aria-hidden="true" />
              </div>
              <h3 className="mt-8 font-display text-lg font-semibold tracking-tight">{title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted">{text}</p>
            </li>
          ))}
        </ol>
      </Container>
    </Section>
  );
}
