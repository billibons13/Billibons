import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getService, services } from "@/content/services";
import { projects } from "@/content/projects";
import { faq } from "@/content/faq";
import { serviceLd } from "@/lib/seo/jsonld";
import { pageMetadata } from "@/lib/seo/metadata";
import { ButtonLink } from "@/components/ui/Button";
import { CheckIcon } from "@/components/ui/Icons";
import { JsonLd } from "@/components/ui/JsonLd";
import { SiteImage } from "@/components/ui/SiteImage";
import { CtaBand } from "@/components/sections/CtaBand";
import { Faq } from "@/components/sections/Faq";
import { PageHeader } from "@/components/sections/PageHeader";
import { ProjectCard } from "@/components/sections/ProjectCard";
import { ServiceCard } from "@/components/sections/ServiceCard";

type Props = { params: Promise<{ slug: string }> };

export const dynamicParams = false;

export function generateStaticParams() {
  return services.map((s) => ({ slug: s.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const s = getService((await params).slug);
  if (!s) return {};
  return pageMetadata({ title: s.seo.title, description: s.seo.description, path: `/leistungen/${s.slug}`, image: s.image });
}

export default async function ServicePage({ params }: Props) {
  const service = getService((await params).slug);
  if (!service) notFound();

  const related = projects.filter((p) => p.services.includes(service.title)).slice(0, 2);
  const others = services.filter((s) => s.group === service.group && s.slug !== service.slug).slice(0, 3);

  return (
    <>
      <PageHeader
        trail={[
          { name: "Leistungen", path: "/leistungen" },
          { name: service.title, path: `/leistungen/${service.slug}` },
        ]}
        eyebrow={`${service.title} · Schleswig-Holstein`}
        title={service.title}
        intro={service.short}
      />

      <div className="container-x">
        <div data-reveal="mask">
          <SiteImage id={service.image} ratio="21 / 9" sizes="(min-width: 1440px) 1360px, 100vw" priority className="hidden sm:block" />
          <SiteImage id={service.image} ratio="4 / 3" sizes="100vw" priority className="sm:hidden" />
        </div>
      </div>

      <section className="section">
        <div className="container-x grid gap-16 lg:grid-cols-12">
          <div className="lg:col-span-5">
            <p className="text-xl leading-relaxed text-pretty sm:text-2xl" data-reveal>
              {service.intro}
            </p>
            <div className="mt-10 flex flex-col gap-3 sm:flex-row lg:flex-col xl:flex-row" data-reveal>
              <ButtonLink href={`/kontakt?leistung=${encodeURIComponent(service.title)}#anfrage`}>Kostenlose Anfrage</ButtonLink>
              <ButtonLink href="/projekte" variant="outline">
                Projekte ansehen
              </ButtonLink>
            </div>
          </div>
          <div className="grid gap-12 sm:grid-cols-2 lg:col-span-6 lg:col-start-7">
            <List title="Ihre Vorteile" items={service.benefits} />
            <List title="Was dazugehört" items={service.includes} />
            <div className="sm:col-span-2" data-reveal>
              <h2 className="eyebrow">Typische Anlässe</h2>
              <ul className="mt-5 flex flex-wrap gap-2">
                {service.occasions.map((o) => (
                  <li key={o} className="border border-ink/15 px-3 py-1.5 text-sm">
                    {o}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>

      {related.length > 0 && (
        <section className="pb-24 lg:pb-32">
          <div className="container-x">
            <h2 className="text-h2 font-semibold" data-reveal>
              Projekte mit {service.title}
            </h2>
            <div className="mt-12 grid gap-12 md:grid-cols-2">
              {related.map((p, i) => (
                <ProjectCard key={p.slug} project={p} index={i} />
              ))}
            </div>
          </div>
        </section>
      )}

      <Faq items={faq.slice(0, 5)} title={`Fragen zu ${service.title}`} />

      {others.length > 0 && (
        <section className="pb-24 lg:pb-32">
          <div className="container-x">
            <h2 className="text-h2 font-semibold" data-reveal>
              Weitere Leistungen
            </h2>
            <div className="mt-12 grid gap-x-8 gap-y-14 sm:grid-cols-2 lg:grid-cols-3">
              {others.map((s, i) => (
                <ServiceCard key={s.slug} service={s} index={i} />
              ))}
            </div>
          </div>
        </section>
      )}

      <CtaBand title={`${service.title} geplant?`} />
      <JsonLd data={serviceLd(service)} />
    </>
  );
}

function List({ title, items }: { title: string; items: string[] }) {
  return (
    <div data-reveal>
      <h2 className="eyebrow">{title}</h2>
      <ul className="mt-5 space-y-3">
        {items.map((it) => (
          <li key={it} className="flex gap-3 border-t border-beton-100 pt-3">
            <CheckIcon className="mt-1 size-4 shrink-0 text-ziegel" />
            <span>{it}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
