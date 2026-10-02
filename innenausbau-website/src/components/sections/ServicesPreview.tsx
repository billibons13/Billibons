import { featuredServiceSlugs, services } from "@/content/services";
import { ButtonLink } from "@/components/ui/Button";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { ServiceCard } from "./ServiceCard";

export function ServicesPreview() {
  const featured = featuredServiceSlugs.map((slug) => services.find((s) => s.slug === slug)!).filter(Boolean);
  return (
    <section className="section">
      <div className="container-x">
        <SectionHeading
          eyebrow="Leistungen"
          title="Alles für den Innenraum. Koordiniert aus einer Hand."
          intro="Von einzelnen Gewerken bis zur Komplettrenovierung: Wir planen die Reihenfolge, stimmen Schnittstellen ab und liefern ein Ergebnis, das bis ins Detail stimmt."
          align="split"
        />
        <div className="mt-16 grid gap-x-8 gap-y-14 sm:grid-cols-2 lg:grid-cols-3">
          {featured.map((s, i) => (
            <ServiceCard key={s.slug} service={s} index={i} />
          ))}
        </div>
        <div className="mt-16 flex justify-center">
          <ButtonLink href="/leistungen" variant="outline">
            Alle {services.length} Leistungen ansehen
          </ButtonLink>
        </div>
      </div>
    </section>
  );
}
