import Link from "next/link";
import { Logo } from "@/components/layout/logo";
import { Container } from "@/components/ui/container";
import { getMessages } from "@/lib/i18n";

export default function AuthLayout({ children }: LayoutProps<"/">) {
  const m = getMessages();
  return (
    <div className="relative flex min-h-dvh flex-col overflow-x-clip">
      <div aria-hidden="true" className="pointer-events-none absolute inset-0 -z-10">
        <div className="bg-grid absolute inset-0 [mask-image:radial-gradient(60%_50%_at_50%_0%,black,transparent)]" />
        <div className="absolute left-1/2 top-[-16rem] h-[30rem] w-[44rem] -translate-x-1/2 rounded-full bg-[radial-gradient(closest-side,rgb(139_147_255/0.22),transparent)] blur-2xl" />
      </div>
      <header>
        <Container className="flex h-16 items-center justify-between">
          <Logo />
          <Link href="/" className="rounded-full px-3 py-2 text-sm text-muted transition-colors hover:text-foreground">
            {m.common.backToHome}
          </Link>
        </Container>
      </header>
      <main id="main" className="flex flex-1 items-start justify-center px-4 pb-16 pt-8 sm:items-center sm:pt-4">
        {children}
      </main>
      <footer className="pb-8 text-center text-xs text-subtle">
        <Container>
          <p>{m.auth.responsibleNote}</p>
          <p className="mt-2 flex justify-center gap-4">
            <Link href="/privacy" className="hover:text-foreground">{m.footer.privacy}</Link>
            <Link href="/terms" className="hover:text-foreground">{m.footer.terms}</Link>
            <Link href="/imprint" className="hover:text-foreground">{m.footer.imprint}</Link>
          </p>
        </Container>
      </footer>
    </div>
  );
}
