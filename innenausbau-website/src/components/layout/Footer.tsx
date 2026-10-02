import Link from "next/link";
import { isPlaceholder, mailHref, site, telHref, whatsappHref } from "@/config/site";
import { legalNav, mainNav } from "@/content/navigation";
import { services } from "@/content/services";
import { ButtonLink } from "@/components/ui/Button";
import { Logo } from "./Logo";

export function Footer() {
  const socials = Object.entries(site.social).filter(([, url]) => url);
  const year = new Date().getFullYear();

  return (
    <footer className="bg-ink pb-24 text-paper sm:pb-0">
      <div className="container-x grid gap-14 py-20 lg:grid-cols-12 lg:py-24">
        <div className="lg:col-span-4">
          <Logo tone="light" />
          <p className="mt-6 max-w-sm text-paper/60">
            Innenausbau, Renovierung und Sanierung für Wohnungen, Häuser, Büros und Gewerbe in {site.serviceArea.label}.
          </p>
          <ButtonLink href="/kontakt#anfrage" className="mt-8">
            Projekt anfragen
          </ButtonLink>
        </div>

        <FooterCol title="Leistungen" className="lg:col-span-3">
          {services.slice(0, 8).map((s) => (
            <li key={s.slug}>
              <Link href={`/leistungen/${s.slug}`} className="hover:text-paper">
                {s.title}
              </Link>
            </li>
          ))}
          <li>
            <Link href="/leistungen" className="text-paper hover:underline">
              Alle Leistungen →
            </Link>
          </li>
        </FooterCol>

        <FooterCol title="Unternehmen" className="lg:col-span-2">
          {mainNav
            .filter((n) => n.href !== "/leistungen")
            .map((n) => (
              <li key={n.href}>
                <Link href={n.href} className="hover:text-paper">
                  {n.label}
                </Link>
              </li>
            ))}
        </FooterCol>

        <FooterCol title="Kontakt" className="lg:col-span-3">
          <li>
            <a href={telHref} className="hover:text-paper">
              {site.contact.phone}
            </a>
          </li>
          <li>
            <a href={mailHref} className="hover:text-paper">
              {site.contact.email}
            </a>
          </li>
          <li>
            <a href={whatsappHref} target="_blank" rel="noopener" className="hover:text-paper">
              WhatsApp schreiben
            </a>
          </li>
          {!isPlaceholder(site.address.street) && (
            <li className="pt-2">
              {site.address.street}
              <br />
              {site.address.postalCode} {site.address.city}
            </li>
          )}
          <li className="pt-2">Region: {site.serviceArea.label}</li>
        </FooterCol>
      </div>

      <div className="border-t border-paper/10">
        <div className="container-x flex flex-col gap-4 py-6 text-sm text-paper/50 sm:flex-row sm:items-center sm:justify-between">
          <p>
            © {year} {isPlaceholder(site.legalName) ? site.name : site.legalName}
          </p>
          <ul className="flex flex-wrap gap-6">
            {legalNav.map((n) => (
              <li key={n.href}>
                <Link href={n.href} className="hover:text-paper">
                  {n.label}
                </Link>
              </li>
            ))}
            {socials.map(([name, url]) => (
              <li key={name}>
                <a href={url} target="_blank" rel="noopener" className="capitalize hover:text-paper">
                  {name}
                </a>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </footer>
  );
}

function FooterCol({ title, children, className }: { title: string; children: React.ReactNode; className?: string }) {
  return (
    <div className={className}>
      <p className="eyebrow text-paper/40">{title}</p>
      <ul className="mt-6 space-y-3 text-paper/70">{children}</ul>
    </div>
  );
}
