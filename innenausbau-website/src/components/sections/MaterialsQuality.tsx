import { SectionHeading } from "@/components/ui/SectionHeading";
import { SiteImage } from "@/components/ui/SiteImage";
import { CheckIcon } from "@/components/ui/Icons";

const checks = [
  "Untergrundprüfung vor jedem Belag und Anstrich",
  "Spachtelqualität Q1–Q4 vorab vereinbart",
  "Abdichtung in Nassbereichen nach anerkannten Regeln der Technik",
  "Material- und Farbmuster vor der Ausführung",
  "Fotodokumentation verdeckter Arbeiten",
  "Gemeinsame Abnahme mit Protokoll",
];

export function MaterialsQuality() {
  return (
    <section className="section">
      <div className="container-x grid gap-12 lg:grid-cols-12 lg:gap-16">
        <div className="grid grid-cols-2 gap-4 lg:col-span-6 lg:gap-6">
          <SiteImage id="material" ratio="4 / 5" sizes="(min-width: 1024px) 25vw, 50vw" className="mt-12" />
          <div className="grid gap-4 lg:gap-6">
            <SiteImage id="fliesen" ratio="4 / 5" sizes="(min-width: 1024px) 25vw, 50vw" />
          </div>
        </div>
        <div className="lg:col-span-5 lg:col-start-8 lg:self-center">
          <SectionHeading
            eyebrow="Materialien & Qualität"
            title="Was man später nicht sieht, entscheidet über das, was bleibt."
            intro="Gute Oberflächen beginnen im Untergrund. Deshalb sind Prüfungen und Abstimmungen fester Teil jedes Projekts – nicht nur, wenn Zeit dafür ist."
          />
          <ul className="mt-10 grid gap-4">
            {checks.map((c) => (
              <li key={c} className="flex gap-4 border-t border-beton-100 pt-4" data-reveal>
                <CheckIcon className="mt-1 size-4 shrink-0 text-ziegel" />
                <span>{c}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
