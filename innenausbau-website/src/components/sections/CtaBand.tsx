import { site, telHref, whatsappHref } from "@/config/site";
import { ButtonLink } from "@/components/ui/Button";
import { PhoneIcon, WhatsAppIcon } from "@/components/ui/Icons";
import { SiteImage } from "@/components/ui/SiteImage";

export function CtaBand({
  title = "Jetzt Projekt besprechen.",
  text = "Erzählen Sie uns, was Sie vorhaben. Wir melden uns zeitnah und vereinbaren auf Wunsch einen Besichtigungstermin.",
}: {
  title?: string;
  text?: string;
}) {
  return (
    <section className="relative overflow-hidden bg-ink text-paper">
      <SiteImage id="komplett" sizes="100vw" className="absolute! inset-0 opacity-25" label={false} />
      <div className="container-x relative py-24 sm:py-32">
        <p className="eyebrow flex items-center gap-3 text-paper/55" data-reveal>
          <span className="h-px w-8 bg-ziegel" aria-hidden />
          Kostenlose Anfrage
        </p>
        <h2 className="text-display mt-6 max-w-4xl font-semibold text-balance" data-reveal>
          {title}
        </h2>
        <p className="mt-6 max-w-xl text-lg text-paper/70" data-reveal>
          {text}
        </p>
        <div className="mt-10 flex flex-col gap-3 sm:flex-row" data-reveal>
          <ButtonLink href="/kontakt#anfrage" size="lg">
            Projekt anfragen
          </ButtonLink>
          <a href={telHref} className="inline-flex min-h-14 items-center justify-center gap-3 border border-paper/30 px-7 font-medium hover:bg-paper hover:text-ink">
            <PhoneIcon className="size-4" /> {site.contact.phone}
          </a>
          <a href={whatsappHref} target="_blank" rel="noopener" className="inline-flex min-h-14 items-center justify-center gap-3 border border-paper/30 px-7 font-medium hover:bg-paper hover:text-ink">
            <WhatsAppIcon className="size-4" /> WhatsApp
          </a>
        </div>
      </div>
    </section>
  );
}
