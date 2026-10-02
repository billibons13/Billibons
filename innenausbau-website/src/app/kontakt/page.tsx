import { mailHref, site, telHref, whatsappHref } from "@/config/site";
import { pageMetadata } from "@/lib/seo/metadata";
import { LeadForm } from "@/components/forms/LeadForm";
import { MailIcon, PhoneIcon, WhatsAppIcon } from "@/components/ui/Icons";
import { PageHeader } from "@/components/sections/PageHeader";

export const metadata = pageMetadata({
  title: "Kontakt & Projektanfrage",
  description:
    "Projekt anfragen: Beschreiben Sie Ihr Vorhaben, laden Sie Fotos hoch und erhalten Sie eine Rückmeldung zu Ihrer Renovierung in Schleswig-Holstein.",
  path: "/kontakt",
});

export default function KontaktPage() {
  const channels = [
    { href: telHref, icon: <PhoneIcon />, label: "Anrufen", value: site.contact.phone },
    { href: whatsappHref, icon: <WhatsAppIcon />, label: "WhatsApp", value: "Nachricht schreiben", external: true },
    { href: mailHref, icon: <MailIcon />, label: "E-Mail", value: site.contact.email },
  ];
  return (
    <>
      <PageHeader
        trail={[{ name: "Kontakt", path: "/kontakt" }]}
        eyebrow="Kontakt"
        title="Erzählen Sie uns von Ihrem Projekt."
        intro="Je mehr wir wissen, desto konkreter können wir Ihnen antworten. Pflichtfelder sind in einer Minute ausgefüllt."
      />
      <section className="pb-24 lg:pb-32">
        <div className="container-x grid gap-16 lg:grid-cols-12">
          <div id="anfrage" className="scroll-mt-24 lg:col-span-7">
            <LeadForm />
          </div>
          <aside className="lg:col-span-4 lg:col-start-9">
            <div className="lg:sticky lg:top-28">
              <h2 className="eyebrow">Direkter Kontakt</h2>
              <ul className="mt-6 divide-y divide-beton-100 border-y border-beton-100">
                {channels.map((c) => (
                  <li key={c.label}>
                    <a
                      href={c.href}
                      {...(c.external ? { target: "_blank", rel: "noopener" } : {})}
                      className="group flex min-h-20 items-center gap-5 py-4"
                    >
                      <span className="flex size-12 items-center justify-center border border-ink/15 transition-colors group-hover:border-ziegel group-hover:bg-ziegel group-hover:text-paper">
                        {c.icon}
                      </span>
                      <span>
                        <span className="block text-sm text-beton-500">{c.label}</span>
                        <span className="block font-medium">{c.value}</span>
                      </span>
                    </a>
                  </li>
                ))}
              </ul>
              <div className="mt-10 bg-paper-2 p-6">
                <h3 className="font-semibold">Was nach Ihrer Anfrage passiert</h3>
                <ol className="mt-4 space-y-3 text-sm text-anthrazit/80">
                  <li>1. Sie erhalten eine Eingangsbestätigung.</li>
                  <li>2. Wir melden uns zeitnah telefonisch oder per E-Mail.</li>
                  <li>3. Wir vereinbaren einen Besichtigungstermin.</li>
                </ol>
              </div>
              <p className="mt-8 text-sm text-anthrazit/70">Einsatzgebiet: {site.serviceArea.label}</p>
            </div>
          </aside>
        </div>
      </section>
    </>
  );
}
