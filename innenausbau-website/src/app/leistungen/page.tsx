import { serviceGroups, services, type ServiceGroup } from "@/content/services";
import { pageMetadata } from "@/lib/seo/metadata";
import { CtaBand } from "@/components/sections/CtaBand";
import { PageHeader } from "@/components/sections/PageHeader";
import { ServiceCard } from "@/components/sections/ServiceCard";

export const metadata = pageMetadata({
  title: "Leistungen – Innenausbau, Renovierung & Sanierung",
  description:
    "Trockenbau, Innenputz, Malerarbeiten, Bodenbeläge, Fliesen, Bad- und Küchenrenovierung bis zur Komplettrenovierung – alle Leistungen in Schleswig-Holstein.",
  path: "/leistungen",
  image: "komplett",
});

export default function LeistungenPage() {
  const groups = Object.keys(serviceGroups) as ServiceGroup[];
  let n = 0;
  return (
    <>
      <PageHeader
        trail={[{ name: "Leistungen", path: "/leistungen" }]}
        eyebrow="Leistungen"
        title="Innenausbau, Renovierung und Sanierung."
        intro="Einzelne Gewerke oder das komplette Projekt: Wir übernehmen, was Ihr Raum braucht – und koordinieren alles Weitere."
      />
      {groups.map((g) => (
        <section key={g} className="pb-24 lg:pb-32">
          <div className="container-x">
            <h2 className="flex items-center gap-4 border-t border-ink pt-5 text-sm font-semibold tracking-[0.2em] uppercase">
              {serviceGroups[g]}
            </h2>
            <div className="mt-10 grid gap-x-8 gap-y-14 sm:grid-cols-2 lg:grid-cols-3">
              {services
                .filter((s) => s.group === g)
                .map((s) => (
                  <ServiceCard key={s.slug} service={s} index={n++} />
                ))}
            </div>
          </div>
        </section>
      ))}
      <CtaBand title="Nicht sicher, welche Leistung Sie brauchen?" text="Beschreiben Sie einfach Ihr Vorhaben – wir sagen Ihnen, was sinnvoll ist und was nicht." />
    </>
  );
}
