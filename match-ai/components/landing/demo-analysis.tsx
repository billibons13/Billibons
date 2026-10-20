import { Minus, TrendingDown, TrendingUp } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Container, Section, SectionHeader } from "@/components/ui/container";
import { getMessages } from "@/lib/i18n";
import { cn } from "@/lib/utils";
import { ConfidenceRing } from "./confidence-ring";
import { DemoExplainButton } from "./demo-explain-button";

type Impact = "positive" | "negative" | "neutral";

const IMPACT_ICON = { positive: TrendingUp, negative: TrendingDown, neutral: Minus } as const;

/** ILLUSTRATIVE example — static demo values, not produced by any model. */
const DEMO_CONFIDENCE = 0.78;

export function DemoAnalysis() {
  const m = getMessages();
  const demo = m.landing.demo;
  const factors: { key: string; title: string; detail: string; impact: Impact }[] = [
    { key: "form", ...demo.factors.form, impact: "positive" },
    { key: "h2h", ...demo.factors.h2h, impact: "neutral" },
    { key: "home", ...demo.factors.home, impact: "positive" },
    { key: "recent", ...demo.factors.recent, impact: "negative" },
  ];

  return (
    <Section aria-labelledby="demo-title" className="bg-[radial-gradient(50%_40%_at_50%_50%,rgb(139_147_255/0.07),transparent)]">
      <Container>
        <SectionHeader id="demo-title" eyebrow={demo.eyebrow} title={demo.title} subtitle={demo.subtitle} />

        <article className="glass mx-auto mt-14 max-w-3xl overflow-hidden rounded-[1.6rem] bg-surface/60 shadow-glow-soft">
          <header className="flex flex-wrap items-center justify-between gap-3 border-b border-border px-5 py-4 sm:px-7">
            <Badge variant="warning">{m.common.demoBadge}</Badge>
            <DemoExplainButton />
          </header>

          <div className="grid gap-8 p-5 sm:p-7 md:grid-cols-[auto_1fr] md:items-center">
            <ConfidenceRing value={DEMO_CONFIDENCE} label={demo.confidence} size={132} gradientId="ring-demo" className="mx-auto" />
            <div className="text-center md:text-left">
              <p className="text-xs uppercase tracking-[0.16em] text-subtle">{demo.league}</p>
              <h3 className="mt-2 font-display text-2xl font-semibold tracking-tight sm:text-3xl">
                {demo.teamA} <span className="text-subtle">vs</span> {demo.teamB}
              </h3>
              <p className="mt-3 text-sm leading-relaxed text-muted">{m.landing.mock.summaryText}</p>
            </div>
          </div>

          <div className="border-t border-border p-5 sm:p-7">
            <h4 className="text-xs font-semibold uppercase tracking-[0.16em] text-subtle">{demo.keyFactors}</h4>
            <ul className="mt-4 grid gap-3 sm:grid-cols-2">
              {factors.map((factor) => {
                const Icon = IMPACT_ICON[factor.impact];
                return (
                  <li key={factor.key} className="rounded-xl border border-border bg-surface-2/60 p-4">
                    <div className="flex items-center justify-between gap-2">
                      <p className="text-sm font-semibold">{factor.title}</p>
                      <span
                        className={cn(
                          "inline-flex items-center gap-1 text-xs",
                          factor.impact === "positive" && "text-positive",
                          factor.impact === "negative" && "text-negative",
                          factor.impact === "neutral" && "text-muted",
                        )}
                      >
                        <Icon className="size-3.5" aria-hidden="true" />
                        {demo.impact[factor.impact]}
                      </span>
                    </div>
                    <p className="mt-1.5 text-sm leading-relaxed text-muted">{factor.detail}</p>
                  </li>
                );
              })}
            </ul>
            <div className="mt-5 rounded-xl border border-warning/20 bg-warning/[0.05] p-4">
              <p className="text-xs font-semibold uppercase tracking-[0.16em] text-warning">{demo.uncertainties}</p>
              <p className="mt-1.5 text-sm text-muted">{demo.uncertaintyText}</p>
            </div>
          </div>

          <footer className="border-t border-border px-5 py-4 text-center text-xs text-subtle sm:px-7">
            {m.common.illustrativeNote} {m.common.responsibleUse}
          </footer>
        </article>
      </Container>
    </Section>
  );
}
