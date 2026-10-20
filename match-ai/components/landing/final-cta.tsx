import { ArrowRight } from "lucide-react";
import { ButtonLink } from "@/components/ui/button";
import { Container } from "@/components/ui/container";
import { getMessages } from "@/lib/i18n";

export function FinalCta() {
  const m = getMessages();
  const cta = m.landing.finalCta;
  return (
    <section aria-labelledby="final-cta-title" className="pb-24 pt-8 sm:pb-32">
      <Container>
        <div className="relative overflow-hidden rounded-[2rem] border border-border-strong bg-surface px-6 py-16 text-center sm:px-12 sm:py-20">
          <div aria-hidden="true" className="pointer-events-none absolute inset-0">
            <div className="absolute left-1/2 top-0 h-72 w-[40rem] -translate-x-1/2 -translate-y-1/2 rounded-full bg-[radial-gradient(closest-side,rgb(139_147_255/0.35),transparent)] blur-2xl" />
            <div className="bg-grid absolute inset-0 opacity-60 [mask-image:radial-gradient(60%_70%_at_50%_0%,black,transparent)]" />
          </div>
          <div className="relative">
            <h2 id="final-cta-title" className="font-display text-3xl font-semibold tracking-tight text-balance sm:text-5xl">
              {cta.title}
            </h2>
            <p className="mx-auto mt-4 max-w-xl text-base text-muted text-pretty sm:text-lg">{cta.subtitle}</p>
            <ButtonLink href="/register" size="lg" className="mt-9">
              {cta.cta}
              <ArrowRight aria-hidden="true" />
            </ButtonLink>
            <p className="mt-6 text-xs text-subtle">{m.common.responsibleUse}</p>
          </div>
        </div>
      </Container>
    </section>
  );
}
