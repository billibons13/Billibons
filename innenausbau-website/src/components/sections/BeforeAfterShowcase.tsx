import Link from "next/link";
import { projects } from "@/content/projects";
import { BeforeAfterSlider } from "@/components/ui/BeforeAfterSlider";
import { SectionHeading } from "@/components/ui/SectionHeading";

export function BeforeAfterShowcase() {
  const [main, ...rest] = projects;
  if (!main) return null;
  return (
    <section className="section bg-ink text-paper">
      <div className="container-x">
        <SectionHeading
          tone="dark"
          eyebrow="Vorher / Nachher"
          title="Der Unterschied liegt im Ergebnis."
          intro="Ziehen Sie den Regler und sehen Sie, wie aus einem Bestand ein Raum wird, in dem man gerne lebt und arbeitet."
          align="split"
        />
        <div className="mt-14" data-reveal>
          <BeforeAfterSlider before={main.before} after={main.after} sizes="(min-width: 1440px) 1360px, 100vw" ratio="16 / 10" />
          <Caption title={main.title} services={main.services} slug={main.slug} />
        </div>
        <div className="mt-14 grid gap-12 md:grid-cols-2">
          {rest.map((p) => (
            <div key={p.slug} data-reveal>
              <BeforeAfterSlider before={p.before} after={p.after} sizes="(min-width: 768px) 50vw, 100vw" />
              <Caption title={p.title} services={p.services} slug={p.slug} />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Caption({ title, services, slug }: { title: string; services: string[]; slug: string }) {
  return (
    <div className="mt-5 flex flex-wrap items-baseline justify-between gap-3 border-t border-paper/15 pt-5">
      <div>
        <h3 className="text-h3 font-semibold">{title}</h3>
        <p className="mt-1 text-sm text-paper/55">{services.join(" · ")}</p>
      </div>
      <Link href={`/projekte/${slug}`} className="text-sm font-medium text-paper underline-offset-8 hover:underline">
        Projekt ansehen →
      </Link>
    </div>
  );
}
