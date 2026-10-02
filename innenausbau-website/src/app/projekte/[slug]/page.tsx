import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getProject, projects } from "@/content/projects";
import { pageMetadata } from "@/lib/seo/metadata";
import { BeforeAfterSlider } from "@/components/ui/BeforeAfterSlider";
import { ButtonLink } from "@/components/ui/Button";
import { SiteImage } from "@/components/ui/SiteImage";
import { CtaBand } from "@/components/sections/CtaBand";
import { PageHeader } from "@/components/sections/PageHeader";
import { ProjectCard } from "@/components/sections/ProjectCard";

type Props = { params: Promise<{ slug: string }> };

export const dynamicParams = false;

export function generateStaticParams() {
  return projects.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const p = getProject((await params).slug);
  if (!p) return {};
  return pageMetadata({ title: p.title, description: p.summary, path: `/projekte/${p.slug}`, image: p.after });
}

export default async function ProjectPage({ params }: Props) {
  const project = getProject((await params).slug);
  if (!project) notFound();
  const more = projects.filter((p) => p.slug !== project.slug).slice(0, 2);

  const facts = [
    { k: "Ort", v: project.location },
    { k: "Objekt", v: project.objectType },
    { k: "Leistung", v: project.services.join(", ") },
    { k: "Dauer", v: project.duration },
  ];

  return (
    <>
      <PageHeader
        trail={[
          { name: "Projekte", path: "/projekte" },
          { name: project.title, path: `/projekte/${project.slug}` },
        ]}
        eyebrow={project.isExample ? "Beispielprojekt" : "Referenzprojekt"}
        title={project.title}
        intro={project.summary}
      >
        <dl className="mt-12 grid grid-cols-2 border-t border-ink lg:grid-cols-4">
          {facts.map((f) => (
            <div key={f.k} className="border-b border-beton-100 py-5 pr-4 lg:border-b-0">
              <dt className="eyebrow">{f.k}</dt>
              <dd className="mt-2 font-medium">{f.v}</dd>
            </div>
          ))}
        </dl>
      </PageHeader>

      <div className="container-x" data-reveal>
        <BeforeAfterSlider before={project.before} after={project.after} sizes="(min-width: 1440px) 1360px, 100vw" ratio="16 / 10" priority />
        <p className="mt-3 text-sm text-beton-500">Regler ziehen, um Vorher und Nachher zu vergleichen.</p>
      </div>

      <section className="section">
        <div className="container-x grid gap-12 lg:grid-cols-12">
          <div className="lg:col-span-5" data-reveal>
            <h2 className="eyebrow">Ausgangslage</h2>
            <p className="mt-4 text-xl leading-relaxed text-pretty">{project.challenge}</p>
          </div>
          <div className="lg:col-span-6 lg:col-start-7" data-reveal>
            <h2 className="eyebrow">Unsere Lösung</h2>
            <p className="mt-4 text-xl leading-relaxed text-pretty">{project.solution}</p>
            <ButtonLink href="/kontakt#anfrage" className="mt-10">
              Ähnliches Projekt anfragen
            </ButtonLink>
          </div>
        </div>
      </section>

      <section className="pb-24 lg:pb-32" aria-label="Galerie">
        <div className="container-x grid gap-4 sm:grid-cols-2 lg:gap-6">
          {project.gallery.map((g, i) => (
            <SiteImage
              key={g + i}
              id={g}
              ratio={i === 0 ? "16 / 9" : "4 / 3"}
              className={i === 0 ? "sm:col-span-2" : ""}
              sizes={i === 0 ? "(min-width: 1440px) 1360px, 100vw" : "(min-width: 640px) 50vw, 100vw"}
            />
          ))}
        </div>
      </section>

      {more.length > 0 && (
        <section className="border-t border-beton-100 py-24 lg:py-32">
          <div className="container-x">
            <h2 className="text-h2 font-semibold">Weitere Projekte</h2>
            <div className="mt-12 grid gap-12 md:grid-cols-2">
              {more.map((p, i) => (
                <ProjectCard key={p.slug} project={p} index={i} />
              ))}
            </div>
          </div>
        </section>
      )}

      <CtaBand />
    </>
  );
}
