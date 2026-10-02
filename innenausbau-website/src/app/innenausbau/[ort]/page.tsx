import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { publishedLocations } from "@/content/locations";
import { projects } from "@/content/projects";
import { featuredServiceSlugs, services } from "@/content/services";
import { pageMetadata } from "@/lib/seo/metadata";
import { CtaBand } from "@/components/sections/CtaBand";
import { PageHeader } from "@/components/sections/PageHeader";
import { ProjectCard } from "@/components/sections/ProjectCard";
import { ServiceCard } from "@/components/sections/ServiceCard";

/**
 * Standortseiten – werden NUR für Orte mit `published: true` und eigenem Inhalt erzeugt
 * (siehe content/locations.ts). Alle anderen URLs liefern 404 → keine Doorway Pages.
 */
type Props = { params: Promise<{ ort: string }> };

export const dynamicParams = false;

export function generateStaticParams() {
  return publishedLocations.map((l) => ({ ort: l.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { ort } = await params;
  const loc = publishedLocations.find((l) => l.slug === ort);
  if (!loc) return {};
  return pageMetadata({
    title: `Innenausbau ${loc.city}`,
    description: loc.intro!.slice(0, 155),
    path: `/innenausbau/${loc.slug}`,
  });
}

export default async function LocationPage({ params }: Props) {
  const { ort } = await params;
  const loc = publishedLocations.find((l) => l.slug === ort);
  if (!loc) notFound();
  const localProjects = projects.filter((p) => loc.projectSlugs?.includes(p.slug));
  const featured = featuredServiceSlugs.slice(0, 3).map((s) => services.find((x) => x.slug === s)!);

  return (
    <>
      <PageHeader
        trail={[{ name: `Innenausbau ${loc.city}`, path: `/innenausbau/${loc.slug}` }]}
        eyebrow={`${loc.district} · Schleswig-Holstein`}
        title={`Innenausbau in ${loc.city}`}
        intro={loc.intro}
      />
      {loc.localNotes && (
        <section className="pb-20">
          <div className="container-x grid gap-6 md:grid-cols-3">
            {loc.localNotes.map((n) => (
              <p key={n} className="border-t border-ink pt-5 leading-relaxed">
                {n}
              </p>
            ))}
          </div>
        </section>
      )}
      {localProjects.length > 0 && (
        <section className="pb-24">
          <div className="container-x grid gap-12 md:grid-cols-2">
            {localProjects.map((p, i) => (
              <ProjectCard key={p.slug} project={p} index={i} />
            ))}
          </div>
        </section>
      )}
      <section className="pb-24">
        <div className="container-x grid gap-x-8 gap-y-14 sm:grid-cols-2 lg:grid-cols-3">
          {featured.map((s, i) => (
            <ServiceCard key={s.slug} service={s} index={i} />
          ))}
        </div>
      </section>
      <CtaBand title={`Projekt in ${loc.city} anfragen.`} />
    </>
  );
}
