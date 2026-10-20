import { ButtonLink } from "@/components/ui/button";
import { getMessages } from "@/lib/i18n";

export default function NotFound() {
  const m = getMessages();
  return (
    <main id="main" className="flex min-h-dvh flex-col items-center justify-center px-4 text-center">
      <p className="font-display text-sm font-semibold tracking-[0.2em] text-accent-strong">404</p>
      <h1 className="mt-4 font-display text-4xl font-semibold tracking-tight">{m.notFound.title}</h1>
      <p className="mt-3 max-w-md text-muted">{m.notFound.body}</p>
      <ButtonLink href="/" className="mt-8">
        {m.notFound.cta}
      </ButtonLink>
    </main>
  );
}
