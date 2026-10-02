import { site } from "@/config/site";
import { heroVideo } from "@/content/assets";
import { ButtonLink } from "@/components/ui/Button";
import { SiteImage, VisualizationBadge } from "@/components/ui/SiteImage";
import { HeroVideo } from "./HeroVideo";

export function Hero() {
  return (
    <section className="relative pt-8 pb-16 sm:pt-14 lg:pt-20 lg:pb-24">
      <div className="container-x">
        <div className="grid gap-10 lg:grid-cols-12 lg:items-end">
          <div className="lg:col-span-8">
            <p className="eyebrow flex items-center gap-3" data-reveal>
              <span className="h-px w-8 bg-ziegel" aria-hidden />
              Innenausbau &amp; Renovierung · {site.address.region}
            </p>
            <h1 className="text-display mt-6 font-semibold text-balance" data-reveal style={{ "--reveal-delay": "80ms" } as React.CSSProperties}>
              Wir verwandeln
              <br />
              Räume<span className="text-ziegel">.</span>
            </h1>
          </div>
          <div className="lg:col-span-4 lg:pb-3" data-reveal style={{ "--reveal-delay": "160ms" } as React.CSSProperties}>
            <p className="text-lg leading-relaxed text-anthrazit/80 text-pretty">
              Professioneller Innenausbau, Renovierung und Sanierung – präzise geplant und sauber umgesetzt. Für Wohnungen,
              Häuser, Büros und Gewerbeflächen.
            </p>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row lg:flex-col 2xl:flex-row">
              <ButtonLink href="/kontakt#anfrage" size="lg">
                Projekt anfragen
              </ButtonLink>
              <ButtonLink href="/leistungen" variant="outline" size="lg">
                Unsere Leistungen
              </ButtonLink>
            </div>
          </div>
        </div>
      </div>

      <div className="container-x mt-12 lg:mt-16">
        <div className="relative aspect-[4/5] overflow-hidden sm:aspect-[16/9] lg:aspect-[21/9]" data-reveal="mask">
          <SiteImage
            id={heroVideo.poster}
            sizes="(min-width: 1440px) 1360px, 100vw"
            priority
            className="absolute! inset-0"
            label={false}
          />
          <HeroVideo src={heroVideo.src} />
          <div className="pointer-events-none absolute inset-x-0 bottom-0 h-1/3 bg-gradient-to-t from-ink/50 to-transparent" />
          <p className="absolute bottom-5 left-5 flex items-center gap-3 text-sm font-medium tracking-wide text-paper sm:bottom-8 sm:left-8">
            <span className="bg-paper/15 px-2.5 py-1 backdrop-blur-sm">Vorher</span>
            <span aria-hidden>→</span>
            <span className="bg-paper px-2.5 py-1 text-ink">Nachher</span>
          </p>
          {site.labelVisualizations && <VisualizationBadge className="right-4 bottom-5 sm:right-8 sm:bottom-8" />}
        </div>
      </div>
    </section>
  );
}
