import { FileWarning } from "lucide-react";
import { Container } from "@/components/ui/container";
import { getMessages } from "@/lib/i18n";

export interface LegalSection {
  readonly h: string;
  readonly p: readonly string[];
}

function slug(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

/** Shared layout for legal TEMPLATE pages (privacy, terms, imprint). */
export function LegalPage({ title, sections }: { title: string; sections: readonly LegalSection[] }) {
  const legal = getMessages().legal;
  return (
    <Container className="max-w-3xl py-16 sm:py-24">
      <h1 className="font-display text-4xl font-semibold tracking-tight sm:text-5xl">{title}</h1>
      <p className="mt-3 text-sm text-subtle">{legal.lastUpdated}</p>
      <div role="note" className="mt-8 flex gap-3 rounded-2xl border border-warning/25 bg-warning/[0.06] p-5 text-sm leading-relaxed text-foreground/90">
        <FileWarning className="mt-0.5 size-5 shrink-0 text-warning" aria-hidden="true" />
        <p>{legal.templateNotice}</p>
      </div>
      {sections.length > 3 ? (
        <nav aria-label={legal.onThisPage} className="mt-10 rounded-2xl border border-border bg-surface/50 p-5">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-subtle">{legal.onThisPage}</p>
          <ol className="mt-3 grid gap-1.5 text-sm sm:grid-cols-2">
            {sections.map((section) => (
              <li key={section.h}>
                <a href={`#${slug(section.h)}`} className="text-muted hover:text-foreground">
                  {section.h}
                </a>
              </li>
            ))}
          </ol>
        </nav>
      ) : null}
      <div className="mt-12 space-y-10">
        {sections.map((section) => (
          <section key={section.h} aria-labelledby={slug(section.h)}>
            <h2 id={slug(section.h)} className="font-display text-xl font-semibold tracking-tight">
              {section.h}
            </h2>
            <div className="mt-3 space-y-2.5 text-[0.95rem] leading-relaxed text-muted">
              {section.p.map((paragraph) => (
                <p key={paragraph}>{paragraph}</p>
              ))}
            </div>
          </section>
        ))}
      </div>
    </Container>
  );
}
