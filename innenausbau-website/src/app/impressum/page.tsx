import { site } from "@/config/site";
import { pageMetadata } from "@/lib/seo/metadata";
import { PageHeader } from "@/components/sections/PageHeader";

export const metadata = pageMetadata({ title: "Impressum", description: `Impressum von ${site.name}.`, path: "/impressum", noindex: true });

/** Angaben nach § 5 DDG. Alle Platzhalter vor Livegang ersetzen und rechtlich prüfen lassen. */
export default function ImpressumPage() {
  const a = site.address;
  return (
    <>
      <PageHeader trail={[{ name: "Impressum", path: "/impressum" }]} title="Impressum" />
      <section className="pb-24">
        <div className="container-x max-w-3xl space-y-8 leading-relaxed text-anthrazit/85 [&_h2]:mb-2 [&_h2]:font-semibold [&_h2]:text-ink">
          <div>
            <h2>Angaben gemäß § 5 DDG</h2>
            <p>
              {site.legalName}
              <br />
              {a.street}
              <br />
              {a.postalCode} {a.city}
            </p>
          </div>
          <div>
            <h2>Vertreten durch</h2>
            <p>[Geschäftsführer/in bzw. Inhaber/in]</p>
          </div>
          <div>
            <h2>Kontakt</h2>
            <p>
              Telefon: {site.contact.phone}
              <br />
              E-Mail: {site.contact.email}
            </p>
          </div>
          <div>
            <h2>Registereintrag</h2>
            <p>[Registergericht, Registernummer – falls vorhanden]</p>
          </div>
          <div>
            <h2>Umsatzsteuer-ID</h2>
            <p>[USt-IdNr. gemäß § 27a UStG – falls vorhanden]</p>
          </div>
          <div>
            <h2>Handwerksrechtliche Angaben</h2>
            <p>
              [Zuständige Handwerkskammer, Eintragung in die Handwerksrolle, Berufsbezeichnung und Staat der Verleihung –
              nur falls zutreffend]
            </p>
          </div>
          <div>
            <h2>Berufshaftpflichtversicherung</h2>
            <p>[Name und Sitz des Versicherers, räumlicher Geltungsbereich – falls Pflichtangabe]</p>
          </div>
          <div>
            <h2>Verbraucherstreitbeilegung</h2>
            <p>
              Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer
              Verbraucherschlichtungsstelle teilzunehmen. [Bitte prüfen]
            </p>
          </div>
        </div>
      </section>
    </>
  );
}
