import { processSteps } from "@/content/process";
import { ButtonLink } from "@/components/ui/Button";
import { SectionHeading } from "@/components/ui/SectionHeading";

export function ProcessSteps({ withCta = true, headingAs = "h2" }: { withCta?: boolean; headingAs?: "h1" | "h2" }) {
  return (
    <section className="section">
      <div className="container-x">
        <SectionHeading
          as={headingAs}
          eyebrow="Arbeitsprozess"
          title="Sechs Schritte. Kein Rätselraten."
          intro="Sie wissen jederzeit, was als Nächstes passiert, wer zuständig ist und wann Ihr Projekt fertig wird."
          align="split"
        />
        <ol className="mt-16 grid gap-px overflow-hidden bg-beton-100 sm:grid-cols-2 lg:grid-cols-3">
          {processSteps.map((s, i) => (
            <li
              key={s.no}
              className="group relative bg-paper p-7 transition-colors duration-500 hover:bg-ink hover:text-paper sm:p-9"
              data-reveal
              style={{ "--reveal-delay": `${(i % 3) * 90}ms` } as React.CSSProperties}
            >
              <p className="text-6xl font-semibold tracking-tighter text-beton-100 transition-colors duration-500 group-hover:text-ziegel">
                {s.no}
              </p>
              <h3 className="text-h3 mt-8 font-semibold">{s.title}</h3>
              <p className="mt-3 leading-relaxed text-anthrazit/75 transition-colors duration-500 group-hover:text-paper/70">{s.text}</p>
            </li>
          ))}
        </ol>
        {withCta && (
          <div className="mt-14 flex flex-col items-start gap-4 sm:flex-row sm:items-center">
            <ButtonLink href="/kontakt#anfrage">Besichtigung vereinbaren</ButtonLink>
            <ButtonLink href="/ablauf" variant="ghost">
              Ablauf im Detail
            </ButtonLink>
          </div>
        )}
      </div>
    </section>
  );
}
