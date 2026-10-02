import { pageMetadata } from "@/lib/seo/metadata";
import { faq } from "@/content/faq";
import { CtaBand } from "@/components/sections/CtaBand";
import { Faq } from "@/components/sections/Faq";
import { PageHeader } from "@/components/sections/PageHeader";
import { ProcessSteps } from "@/components/sections/ProcessSteps";
import { SiteImage } from "@/components/ui/SiteImage";

export const metadata = pageMetadata({
  title: "Ablauf – von der Anfrage bis zur Abnahme",
  description:
    "So läuft Ihre Renovierung ab: Anfrage, Besichtigung, Planung, Angebot, Umsetzung und Abnahme – transparent und mit festem Ansprechpartner.",
  path: "/ablauf",
  image: "team",
});

const details = [
  {
    title: "Was Sie vorbereiten können",
    items: ["Fotos der Räume", "Grundriss oder ungefähre Maße", "Wünsche und Prioritäten", "Ihren zeitlichen Rahmen"],
  },
  {
    title: "Was Sie von uns erhalten",
    items: ["Besichtigung vor Ort", "Angebot mit Einzelpositionen", "Zeitplan mit Bauabschnitten", "Abnahmeprotokoll"],
  },
  {
    title: "Während der Bauphase",
    items: ["Fester Ansprechpartner", "Regelmäßige Updates mit Fotos", "Geschützte, aufgeräumte Baustelle", "Abstimmung bei Änderungen vorab"],
  },
];

export default function AblaufPage() {
  return (
    <>
      <PageHeader
        trail={[{ name: "Ablauf", path: "/ablauf" }]}
        eyebrow="Ablauf"
        title="Klarer Prozess. Planbares Ergebnis."
        intro="Renovieren muss kein Stress sein. Unser Ablauf sorgt dafür, dass Sie jederzeit wissen, woran Sie sind."
      />
      <div className="container-x" data-reveal="mask">
        <SiteImage id="team" ratio="21 / 9" sizes="(min-width: 1440px) 1360px, 100vw" priority />
      </div>
      <ProcessSteps withCta={false} />
      <section className="pb-24 lg:pb-32">
        <div className="container-x grid gap-12 md:grid-cols-3">
          {details.map((d) => (
            <div key={d.title} className="border-t border-ink pt-6" data-reveal>
              <h2 className="text-h3 font-semibold">{d.title}</h2>
              <ul className="mt-6 space-y-3 text-anthrazit/80">
                {d.items.map((i) => (
                  <li key={i} className="border-t border-beton-100 pt-3">
                    {i}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>
      <Faq items={faq} />
      <CtaBand title="Besichtigung vereinbaren." />
    </>
  );
}
