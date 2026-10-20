import Link from "next/link";
import { Container } from "@/components/ui/container";
import { brand } from "@/lib/config/brand";
import { getMessages } from "@/lib/i18n";
import { CookieSettingsButton } from "./cookie-settings-button";
import { Logo } from "./logo";
import { getNavLinks } from "./nav-links";

async function CurrentYear() {
  "use cache";
  return <>{new Date().getFullYear()}</>;
}

export function Footer() {
  const m = getMessages();
  const linkClass = "text-sm text-muted transition-colors hover:text-foreground";

  return (
    <footer className="relative border-t border-border">
      <Container className="grid grid-cols-2 gap-x-6 gap-y-10 py-14 lg:grid-cols-[1.4fr_1fr_1fr_1fr]">
        <div className="col-span-2 max-w-xs lg:col-span-1">
          <Logo />
          <p className="mt-4 text-sm leading-relaxed text-muted">{brand.tagline}</p>
        </div>
        <nav aria-label={m.footer.product}>
          <h2 className="text-xs font-semibold uppercase tracking-[0.16em] text-subtle">{m.footer.product}</h2>
          <ul className="mt-4 space-y-3">
            {getNavLinks(m).map((link) => (
              <li key={link.href}>
                <a href={link.href} className={linkClass}>
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>
        <nav aria-label={m.footer.legal}>
          <h2 className="text-xs font-semibold uppercase tracking-[0.16em] text-subtle">{m.footer.legal}</h2>
          <ul className="mt-4 space-y-3">
            <li>
              <Link href="/privacy" className={linkClass}>
                {m.footer.privacy}
              </Link>
            </li>
            <li>
              <Link href="/terms" className={linkClass}>
                {m.footer.terms}
              </Link>
            </li>
            <li>
              <Link href="/imprint" className={linkClass}>
                {m.footer.imprint}
              </Link>
            </li>
            <li>
              <CookieSettingsButton className={linkClass} />
            </li>
          </ul>
        </nav>
        <div>
          <h2 className="text-xs font-semibold uppercase tracking-[0.16em] text-subtle">{m.footer.support}</h2>
          <ul className="mt-4 space-y-3">
            <li>
              <a href={`mailto:${brand.supportEmail}`} className={linkClass}>
                {brand.supportEmail}
              </a>
            </li>
          </ul>
        </div>
      </Container>
      <Container className="flex flex-col gap-2 border-t border-border py-6 text-xs text-subtle sm:flex-row sm:items-center sm:justify-between">
        <p>
          © <CurrentYear /> {brand.legalEntity}. {m.footer.rights}
        </p>
        <p>{m.common.responsibleUse}</p>
      </Container>
    </footer>
  );
}
