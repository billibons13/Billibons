import { projects } from "@/content/projects";
import { ButtonLink } from "@/components/ui/Button";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { ProjectCard } from "./ProjectCard";

export function FeaturedProjects() {
  const [first, ...others] = projects;
  if (!first) return null;
  return (
    <section className="section">
      <div className="container-x">
        <SectionHeading
          eyebrow="Projekte"
          title="Räume, die wir verwandelt haben."
          intro="Jedes Projekt beginnt mit einem Bestand und endet mit einer sauberen Übergabe. Ein Einblick in Umfang, Lösung und Ergebnis."
          align="split"
        />
        <div className="mt-16 grid gap-x-8 gap-y-14 lg:grid-cols-3">
          <div className="lg:col-span-2">
            <ProjectCard project={first} large />
          </div>
          <div className="grid gap-14">
            {others.slice(0, 2).map((p, i) => (
              <ProjectCard key={p.slug} project={p} index={i + 1} />
            ))}
          </div>
        </div>
        <div className="mt-16 flex justify-center">
          <ButtonLink href="/projekte" variant="outline">
            Alle Projekte
          </ButtonLink>
        </div>
      </div>
    </section>
  );
}
