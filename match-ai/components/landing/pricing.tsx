import { Check } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { ButtonLink } from "@/components/ui/button";
import { Container, Section, SectionHeader } from "@/components/ui/container";
import { formatPrice, plans } from "@/lib/config/plans";
import { format, getMessages } from "@/lib/i18n";
import { cn } from "@/lib/utils";

/** Pricing cards. All numbers come from lib/config/plans.ts — nothing is hardcoded here. */
export function Pricing() {
  const p = getMessages().landing.pricing;

  return (
    <Section id="pricing" aria-labelledby="pricing-title">
      <Container>
        <SectionHeader id="pricing-title" eyebrow={p.eyebrow} title={p.title} subtitle={p.subtitle} />
        <ul className="mx-auto mt-16 grid max-w-5xl gap-4 lg:grid-cols-3">
          {plans.map((plan) => {
            const copy = p.plans[plan.id];
            return (
              <li
                key={plan.id}
                className={cn(
                  "relative flex flex-col rounded-2xl p-7",
                  plan.highlighted
                    ? "border border-accent/40 bg-[linear-gradient(180deg,rgb(139_147_255/0.12),rgb(139_147_255/0.02))] shadow-glow"
                    : "glass",
                )}
              >
                <div className="flex items-center justify-between gap-2">
                  <h3 className="font-display text-lg font-semibold tracking-tight">{copy.name}</h3>
                  {plan.highlighted ? <Badge variant="accent">{p.popular}</Badge> : null}
                </div>
                <p className="mt-1.5 text-sm text-muted">{copy.description}</p>
                <p className="mt-7 flex items-baseline gap-1.5">
                  <span className="font-display text-4xl font-semibold tracking-tight tabular-nums">
                    {formatPrice(plan.price)}
                  </span>
                  <span className="text-sm text-subtle">{p.perMonth}</span>
                </p>
                <p className="mt-2 text-sm font-medium text-accent-strong">
                  {format(p.analysesPerMonth, { count: plan.analysesPerMonth })}
                </p>
                <ul className="mt-7 flex-1 space-y-3 border-t border-border pt-6">
                  {p.featureList[plan.id].map((feature) => (
                    <li key={feature} className="flex items-start gap-2.5 text-sm text-foreground/90">
                      <Check className="mt-0.5 size-4 shrink-0 text-accent-2" aria-hidden="true" />
                      {feature}
                    </li>
                  ))}
                </ul>
                <ButtonLink
                  href={plan.paid ? `/register?plan=${plan.id}` : "/register"}
                  variant={plan.highlighted ? "primary" : "secondary"}
                  className="mt-8 w-full"
                >
                  {copy.cta}
                </ButtonLink>
              </li>
            );
          })}
        </ul>
        <p className="mt-8 text-center text-xs text-subtle">{p.preliminary}</p>
      </Container>
    </Section>
  );
}
