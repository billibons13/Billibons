import { Counter } from "@/components/ui/Counter";
import { services } from "@/content/services";
import { processSteps } from "@/content/process";

/**
 * Vertrauensanker ohne erfundene Zahlen: Es werden nur belegbare Werte gezählt
 * (Anzahl Leistungen/Schritte aus dem Content). Echte Kennzahlen (Projekte, Jahre)
 * erst ergänzen, wenn sie in config/site.ts → facts gepflegt sind.
 */
export function TrustBar() {
  const items = [
    { value: <Counter value={services.length} />, label: "Leistungen aus einer Hand" },
    { value: <Counter value={processSteps.length} />, label: "klare Schritte bis zur Abnahme" },
    { value: <Counter value={1} />, label: "fester Ansprechpartner pro Projekt" },
    { value: "SH + HH", label: "Schleswig-Holstein & Hamburg" },
  ];
  return (
    <section aria-label="Auf einen Blick" className="border-y border-beton-100">
      <div className="container-x grid grid-cols-2 lg:grid-cols-4">
        {items.map((it, i) => (
          <div
            key={it.label}
            className={`py-8 pr-4 sm:py-10 ${i % 2 ? "border-l border-beton-100 pl-5 sm:pl-8" : ""} ${i === 2 ? "border-t border-beton-100 lg:border-t-0 lg:border-l lg:pl-8" : ""} ${i === 3 ? "border-t border-beton-100 lg:border-t-0" : ""}`}
            data-reveal
            style={{ "--reveal-delay": `${i * 80}ms` } as React.CSSProperties}
          >
            <p className="text-4xl font-semibold tracking-tight sm:text-5xl">{it.value}</p>
            <p className="mt-2 text-sm text-anthrazit/70">{it.label}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
