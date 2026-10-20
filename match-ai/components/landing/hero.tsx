import { ArrowRight, Sparkles } from "lucide-react";
import { ButtonLink } from "@/components/ui/button";
import { Container } from "@/components/ui/container";
import { getMessages } from "@/lib/i18n";
import { AnalysisMock } from "./analysis-mock";

export function Hero() {
  const m = getMessages();
  const hero = m.landing.hero;

  return (
    <section aria-labelledby="hero-title" className="relative overflow-hidden pt-16 pb-20 sm:pt-24 sm:pb-28">
      <div aria-hidden="true" className="pointer-events-none absolute inset-0 -z-10">
        <div className="bg-grid absolute inset-0 [mask-image:radial-gradient(70%_55%_at_50%_0%,black,transparent)]" />
        <div className="absolute left-1/2 top-[-18rem] h-[36rem] w-[56rem] -translate-x-1/2 rounded-full bg-[radial-gradient(closest-side,rgb(139_147_255/0.28),transparent)] blur-2xl" />
        <div className="absolute right-[-10rem] top-[8rem] h-[22rem] w-[22rem] rounded-full bg-[radial-gradient(closest-side,rgb(94_234_212/0.12),transparent)] blur-2xl" />
      </div>

      <Container className="flex flex-col items-center text-center">
        <p className="glass inline-flex animate-fade-up items-center gap-2 rounded-full px-3.5 py-1.5 text-xs font-medium text-muted">
          <Sparkles className="size-3.5 text-accent-strong" aria-hidden="true" />
          {hero.eyebrow}
        </p>
        <h1
          id="hero-title"
          className="mt-7 max-w-4xl animate-fade-up font-display text-[2.6rem] font-semibold leading-[1.04] tracking-[-0.035em] text-balance sm:text-6xl lg:text-[4.6rem]"
        >
          <span className="text-gradient">{hero.title}</span>
        </h1>
        <p className="mt-6 max-w-2xl animate-fade-up text-base leading-relaxed text-muted text-pretty sm:text-lg [animation-delay:80ms]">
          {hero.subtitle}
        </p>
        <div className="mt-9 flex w-full animate-fade-up flex-col items-center justify-center gap-3 sm:w-auto sm:flex-row [animation-delay:140ms]">
          <ButtonLink href="/register" size="lg" className="w-full sm:w-auto">
            {hero.primaryCta}
            <ArrowRight aria-hidden="true" />
          </ButtonLink>
          <ButtonLink href="#how-it-works" variant="secondary" size="lg" className="w-full sm:w-auto">
            {hero.secondaryCta}
          </ButtonLink>
        </div>
        <p className="mt-5 text-xs text-subtle">{hero.note}</p>
      </Container>

      <Container className="mt-16 sm:mt-20">
        <AnalysisMock />
      </Container>
    </section>
  );
}
