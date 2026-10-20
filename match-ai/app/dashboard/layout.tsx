import Link from "next/link";
import { Logo } from "@/components/layout/logo";
import { Container } from "@/components/ui/container";
import { getMessages } from "@/lib/i18n";

export default function DashboardLayout({ children }: LayoutProps<"/dashboard">) {
  const m = getMessages();
  return (
    <div className="flex min-h-dvh flex-col overflow-x-clip">
      <header className="border-b border-border">
        <Container className="flex h-16 items-center justify-between">
          <Logo />
          <Link href="/#pricing" className="rounded-full px-3 py-2 text-sm text-muted hover:text-foreground">
            {m.nav.pricing}
          </Link>
        </Container>
      </header>
      <main id="main" className="flex-1">
        {children}
      </main>
      <footer className="border-t border-border py-6 text-center text-xs text-subtle">
        <Container>{m.common.responsibleUse}</Container>
      </footer>
    </div>
  );
}
