import { site } from "@/config/site";
import { pageMetadata } from "@/lib/seo/metadata";
import { PageHeader } from "@/components/sections/PageHeader";

export const metadata = pageMetadata({ title: "Datenschutz", description: "Datenschutzerklärung.", path: "/datenschutz", noindex: true });

/**
 * Struktur-Vorlage. Muss vor Livegang durch eine geprüfte Datenschutzerklärung
 * (Anwalt oder Generator) ersetzt werden – insbesondere Hosting, Make.com (USA/EU),
 * Google Workspace, Telegram, CRM und ggf. Analytics.
 */
export default function DatenschutzPage() {
  return (
    <>
      <PageHeader trail={[{ name: "Datenschutz", path: "/datenschutz" }]} title="Datenschutzerklärung" />
      <section className="pb-24">
        <div className="container-x max-w-3xl space-y-8 leading-relaxed text-anthrazit/85 [&_h2]:mb-2 [&_h2]:text-lg [&_h2]:font-semibold [&_h2]:text-ink">
          <p className="border-l-2 border-ziegel pl-4 text-sm">
            [Entwurf – vor Veröffentlichung rechtlich prüfen und vervollständigen.]
          </p>
          <div>
            <h2>1. Verantwortlicher</h2>
            <p>
              {site.legalName}, {site.address.street}, {site.address.postalCode} {site.address.city}, E-Mail:{" "}
              {site.contact.email}
            </p>
          </div>
          <div>
            <h2>2. Hosting und Server-Logfiles</h2>
            <p>[Hosting-Anbieter, Serverstandort, Art der Logdaten, Speicherdauer, Rechtsgrundlage Art. 6 Abs. 1 lit. f DSGVO.]</p>
          </div>
          <div>
            <h2>3. Kontakt- und Anfrageformular</h2>
            <p>
              Wenn Sie uns über das Formular eine Anfrage senden, verarbeiten wir Ihre Angaben (Name, Telefon, E-Mail, Ort,
              Projektangaben, Nachricht, hochgeladene Fotos) zur Bearbeitung Ihrer Anfrage und zur Vorbereitung eines
              Angebots (Art. 6 Abs. 1 lit. b DSGVO) sowie auf Grundlage Ihrer Einwilligung (Art. 6 Abs. 1 lit. a DSGVO).
            </p>
            <p className="mt-3">
              Zur Verarbeitung nutzen wir folgende Dienstleister als Auftragsverarbeiter: [Make.com (Celonis SE),
              Google Workspace (Tabellen/Drive/Gmail), Telegram (interne Benachrichtigung), CRM-Anbieter]. [Angaben zu
              Drittlandübermittlung, Standardvertragsklauseln, Speicherdauer.]
            </p>
          </div>
          <div>
            <h2>4. Kontakt per Telefon, E-Mail oder WhatsApp</h2>
            <p>[Hinweis zur Nutzung von WhatsApp (Meta Platforms Ireland Ltd.), Drittlandübermittlung, Alternativen.]</p>
          </div>
          <div>
            <h2>5. Schriftarten</h2>
            <p>Die Schriftart wird lokal von unserem Server ausgeliefert. Es findet keine Verbindung zu Google-Servern statt.</p>
          </div>
          <div>
            <h2>6. Ihre Rechte</h2>
            <p>
              Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit, Widerspruch sowie
              Widerruf erteilter Einwilligungen. Beschwerderecht bei einer Aufsichtsbehörde, z. B. dem Unabhängigen
              Landeszentrum für Datenschutz Schleswig-Holstein (ULD).
            </p>
          </div>
        </div>
      </section>
    </>
  );
}
