import Link from "next/link";
import { site } from "@/config/site";
import { locations } from "@/content/locations";

/**
 * Lokaler SEO-Block. Orte werden nur verlinkt, wenn eine eigenständige
 * Standortseite mit echtem Inhalt veröffentlicht ist (keine Doorway Pages).
 */
export function RegionBlock() {
  return (
    <section className="section border-t border-beton-100">
      <div className="container-x grid gap-12 lg:grid-cols-12">
        <div className="lg:col-span-5">
          <p className="eyebrow flex items-center gap-3" data-reveal>
            <span className="h-px w-8 bg-ziegel" aria-hidden />
            Region
          </p>
          <h2 className="text-h2 mt-5 font-semibold text-balance" data-reveal>
            Innenausbau in Schleswig-Holstein
          </h2>
        </div>
        <div className="space-y-5 text-lg leading-relaxed text-anthrazit/80 lg:col-span-6 lg:col-start-7" data-reveal>
          <p>
            Ob Backsteinhaus aus den 30ern, Reihenhaus aus den 70ern oder Gewerbeeinheit im Neubau: Die Bausubstanz im
            Norden ist vielfältig – und jede bringt eigene Anforderungen an Putz, Trockenbau, Abdichtung und Boden mit.
          </p>
          <p>
            Wir übernehmen Innenausbau, Renovierung und Sanierung in {site.serviceArea.label} – unter anderem in den
            Regionen {site.serviceArea.regions.join(", ")}.
          </p>
          <ul className="flex flex-wrap gap-2 pt-2">
            {locations.map((l) => (
              <li key={l.slug}>
                {l.published && l.intro ? (
                  <Link href={`/innenausbau/${l.slug}`} className="inline-block border border-ink/20 px-3 py-1.5 text-sm hover:border-ink">
                    Innenausbau {l.city}
                  </Link>
                ) : (
                  <span className="inline-block border border-beton-100 px-3 py-1.5 text-sm text-anthrazit/70">{l.city}</span>
                )}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
