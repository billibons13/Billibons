import { SectionHeading } from "@/components/ui/SectionHeading";
import { SiteImage } from "@/components/ui/SiteImage";

/** Werte statt Superlative – jede Aussage beschreibt ein überprüfbares Vorgehen. */
export const principles = [
  {
    title: "Präzision",
    text: "Wir messen, planen und prüfen, bevor wir bauen. Fluchten, Fugen und Anschlüsse werden festgelegt – nicht improvisiert.",
  },
  {
    title: "Saubere Ausführung",
    text: "Bewohnte Bereiche werden geschützt, Staub wird minimiert, die Baustelle ist jeden Abend aufgeräumt.",
  },
  {
    title: "Transparente Kommunikation",
    text: "Ein fester Ansprechpartner, ein nachvollziehbares Angebot und regelmäßige Updates zum Stand Ihres Projekts.",
  },
  {
    title: "Zuverlässige Termine",
    text: "Realistische Zeitpläne statt Versprechen. Wenn sich etwas ändert, erfahren Sie es von uns – rechtzeitig.",
  },
  {
    title: "Hochwertige Materialien",
    text: "Wir arbeiten mit aufeinander abgestimmten Systemen und beraten Sie, welches Material zu Nutzung und Budget passt.",
  },
  {
    title: "Professionelle Planung",
    text: "Gewerke in der richtigen Reihenfolge, Schnittstellen zu Elektro und Sanitär abgestimmt – damit nichts doppelt gemacht wird.",
  },
];

export function WhyUs() {
  return (
    <section className="section bg-paper-2">
      <div className="container-x grid gap-16 lg:grid-cols-12">
        <div className="lg:col-span-5">
          <div className="lg:sticky lg:top-32">
            <SectionHeading
              eyebrow="Warum wir"
              title="Qualität ist kein Versprechen. Sondern eine Arbeitsweise."
              intro="Sie vertrauen uns Ihr Zuhause oder Ihre Geschäftsräume an. Deshalb arbeiten wir nach klaren Prinzipien – vom ersten Termin bis zur Abnahme."
            />
            <SiteImage id="team" ratio="3 / 2" sizes="(min-width: 1024px) 40vw, 100vw" className="mt-10" />
          </div>
        </div>
        <ol className="lg:col-span-6 lg:col-start-7">
          {principles.map((p, i) => (
            <li key={p.title} className="grid grid-cols-[3rem_1fr] gap-4 border-t border-ink/10 py-8 first:border-t-0 first:pt-0 sm:py-10" data-reveal>
              <span className="pt-1 text-sm text-ziegel tabular-nums">{String(i + 1).padStart(2, "0")}</span>
              <div>
                <h3 className="text-h3 font-semibold">{p.title}</h3>
                <p className="mt-3 leading-relaxed text-anthrazit/75">{p.text}</p>
              </div>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
