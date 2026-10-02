import { site } from "@/config/site";
import { testimonials } from "@/content/testimonials";
import { ButtonLink } from "@/components/ui/Button";
import { SectionHeading } from "@/components/ui/SectionHeading";

/**
 * Zeigt ausschließlich echte Kundenstimmen. Solange keine vorliegen,
 * erscheint ein ehrlicher Hinweis – keine Fake-Reviews.
 */
export function Testimonials() {
  return (
    <section className="section bg-paper-2">
      <div className="container-x">
        <SectionHeading eyebrow="Kundenstimmen" title="Was unsere Kunden sagen." align="split"
          intro={testimonials.length ? "Echte Rückmeldungen nach abgeschlossenen Projekten." : undefined} />

        {testimonials.length > 0 ? (
          <div className="mt-14 grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {testimonials.map((t) => (
              <figure key={t.name + t.project} className="flex flex-col justify-between bg-paper p-8" data-reveal>
                <blockquote className="text-lg leading-relaxed text-pretty">„{t.quote}“</blockquote>
                <figcaption className="mt-8 border-t border-beton-100 pt-5 text-sm">
                  <span className="font-semibold">{t.name}</span>
                  <span className="text-beton-500"> · {t.location} · {t.project}</span>
                  {t.source && <span className="block text-xs text-beton-500">Quelle: {t.source}</span>}
                </figcaption>
              </figure>
            ))}
          </div>
        ) : (
          <div className="mt-14 grid gap-8 border-t border-ink/10 pt-10 lg:grid-cols-12" data-reveal>
            <p className="text-xl leading-relaxed text-pretty lg:col-span-7">
              Wir veröffentlichen hier ausschließlich echte Bewertungen unserer Kundinnen und Kunden – mit deren
              Einverständnis. Gern nennen wir Ihnen auf Anfrage Referenzprojekte in Ihrer Nähe.
            </p>
            <div className="flex flex-col gap-3 lg:col-span-4 lg:col-start-9">
              {site.social.googleBusiness && (
                <ButtonLink href={site.social.googleBusiness} variant="outline" target="_blank" rel="noopener">
                  Google-Bewertungen ansehen
                </ButtonLink>
              )}
              <ButtonLink href="/kontakt#anfrage">Referenzen anfragen</ButtonLink>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
