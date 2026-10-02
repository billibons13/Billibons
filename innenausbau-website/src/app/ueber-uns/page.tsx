import { site } from "@/config/site";
import { pageMetadata } from "@/lib/seo/metadata";
import { CtaBand } from "@/components/sections/CtaBand";
import { PageHeader } from "@/components/sections/PageHeader";
import { principles } from "@/components/sections/WhyUs";
import { SiteImage } from "@/components/ui/SiteImage";

export const metadata = pageMetadata({
  title: "Über uns – Ihr Partner für Innenausbau im Norden",
  description:
    "Wer wir sind und wie wir arbeiten: Innenausbau, Renovierung und Sanierung in Schleswig-Holstein mit Präzision, Sauberkeit und transparenter Kommunikation.",
  path: "/ueber-uns",
  image: "team",
});

export default function UeberUnsPage() {
  const f = site.facts;
  const facts = [
    f.foundedYear && { k: "Gegründet", v: String(f.foundedYear) },
    f.teamSize && { k: "Team", v: `${f.teamSize} Mitarbeitende` },
    f.completedProjects && { k: "Abgeschlossene Projekte", v: String(f.completedProjects) },
    { k: "Region", v: site.serviceArea.label },
  ].filter(Boolean) as { k: string; v: string }[];

  return (
    <>
      <PageHeader
        trail={[{ name: "Über uns", path: "/ueber-uns" }]}
        eyebrow="Über uns"
        title="Handwerk mit Anspruch. Aus dem Norden."
        intro="Wir sind ein Innenausbau-Betrieb aus Schleswig-Holstein. Unser Antrieb: Räume so zu verwandeln, dass sie besser funktionieren und länger Freude machen."
      />
      <div className="container-x grid gap-4 sm:grid-cols-3 lg:gap-6">
        <SiteImage id="team" ratio="4 / 5" sizes="(min-width: 640px) 33vw, 100vw" className="sm:col-span-2 sm:aspect-auto!" priority />
        <div className="grid gap-4 lg:gap-6">
          <SiteImage id="putz" ratio="4 / 3" sizes="(min-width: 640px) 33vw, 100vw" />
          <SiteImage id="decke" ratio="4 / 3" sizes="(min-width: 640px) 33vw, 100vw" />
        </div>
      </div>

      <section className="section">
        <div className="container-x grid gap-16 lg:grid-cols-12">
          <div className="space-y-6 text-xl leading-relaxed text-pretty lg:col-span-6" data-reveal>
            {/* TODO: Gründungsgeschichte, Inhaber, Qualifikation (z. B. Meisterbetrieb) – nur echte Angaben */}
            <p>
              [Kurzporträt des Inhabers bzw. der Inhaberin: Ausbildung, Erfahrung, warum der Betrieb gegründet wurde.]
            </p>
            <p>
              Was uns auszeichnet, ist keine einzelne Leistung, sondern die Art, wie wir arbeiten: sorgfältig geplant,
              sauber ausgeführt und mit offener Kommunikation – vom ersten Termin bis zur Abnahme.
            </p>
            <p>
              Wir arbeiten für private Eigentümer, Vermieter, Hausverwaltungen sowie Büro- und Gewerbekunden in{" "}
              {site.serviceArea.label}.
            </p>
          </div>
          <dl className="grid content-start gap-0 lg:col-span-4 lg:col-start-9">
            {facts.map((x) => (
              <div key={x.k} className="border-t border-ink/15 py-5">
                <dt className="eyebrow">{x.k}</dt>
                <dd className="mt-2 text-2xl font-semibold tracking-tight">{x.v}</dd>
              </div>
            ))}
            {f.certifications.length > 0 && (
              <div className="border-t border-ink/15 py-5">
                <dt className="eyebrow">Zertifizierungen</dt>
                <dd className="mt-2">{f.certifications.join(", ")}</dd>
              </div>
            )}
            {f.memberships.length > 0 && (
              <div className="border-t border-ink/15 py-5">
                <dt className="eyebrow">Mitgliedschaften</dt>
                <dd className="mt-2">{f.memberships.join(", ")}</dd>
              </div>
            )}
          </dl>
        </div>
      </section>

      <section className="section bg-paper-2">
        <div className="container-x">
          <h2 className="text-h2 max-w-3xl font-semibold" data-reveal>
            Woran Sie unsere Arbeit erkennen.
          </h2>
          <div className="mt-14 grid gap-px bg-beton-100 sm:grid-cols-2 lg:grid-cols-3">
            {principles.map((p) => (
              <div key={p.title} className="bg-paper-2 p-8" data-reveal>
                <h3 className="text-h3 font-semibold">{p.title}</h3>
                <p className="mt-3 leading-relaxed text-anthrazit/75">{p.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
      <CtaBand />
    </>
  );
}
