import { ButtonLink } from "@/components/ui/button";
import { Container } from "@/components/ui/container";
import { getMessages } from "@/lib/i18n";
import { Logo } from "./logo";
import { MobileMenu } from "./mobile-menu";
import { getNavLinks } from "./nav-links";

export function Navbar() {
  const m = getMessages();
  const links = getNavLinks(m);
  return (
    <header className="sticky top-0 z-50 border-b border-transparent bg-background/70 backdrop-blur-xl supports-[backdrop-filter]:bg-background/55">
      <Container className="flex h-16 items-center justify-between gap-6">
        <Logo />
        <nav aria-label={m.nav.primaryLabel} className="hidden md:block">
          <ul className="flex items-center gap-1">
            {links.map((link) => (
              <li key={link.href}>
                <a
                  href={link.href}
                  className="rounded-full px-3.5 py-2 text-sm text-muted transition-colors hover:text-foreground"
                >
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>
        <div className="hidden items-center gap-2 md:flex">
          <ButtonLink href="/login" variant="ghost" size="sm">
            {m.nav.login}
          </ButtonLink>
          <ButtonLink href="/register" size="sm">
            {m.nav.tryFree}
          </ButtonLink>
        </div>
        <MobileMenu links={links} />
      </Container>
      <div aria-hidden="true" className="h-px w-full bg-gradient-to-r from-transparent via-white/10 to-transparent" />
    </header>
  );
}
