import { projects } from "@/content/projects";
import { site } from "@/config/site";
import { pageMetadata } from "@/lib/seo/metadata";
import { CtaBand } from "@/components/sections/CtaBand";
import { PageHeader } from "@/components/sections/PageHeader";
import { ProjectCard } from "@/components/sections/ProjectCard";

export const metadata = pageMetadata({
  title: "Projekte – Vorher & Nachher",
  description:
    "Renovierungs- und Sanierungsprojekte in Schleswig-Holstein: Badsanierung, Wohnungsrenovierung, Küchenrenovierung – mit Vorher-Nachher-Vergleich.",
  path: "/projekte",
  image: "wohnenNachher",
});

export default function ProjektePage() {
  const hasExamples = projects.some((p) => p.isExample);
  return (
    <>
      <PageHeader
        trail={[{ name: "Projekte", path: "/projekte" }]}
        eyebrow="Portfolio"
        title="Vorher. Nachher. Und alles dazwischen."
        intro="Ausgewählte Projekte mit Ausgangslage, Lösung und Ergebnis – inklusive interaktivem Vorher-Nachher-Vergleich."
      />
      <section className="pb-24 lg:pb-32">
        <div className="container-x">
          {hasExamples && site.labelVisualizations && (
            <p className="mb-12 max-w-3xl border-l-2 border-ziegel pl-4 text-sm text-anthrazit/70">
              Hinweis: Als „Beispielprojekt“ gekennzeichnete Einträge zeigen Visualisierungen typischer Projekte. Sie werden
              laufend durch dokumentierte Referenzprojekte ersetzt.
            </p>
          )}
          <div className="grid gap-x-8 gap-y-16 md:grid-cols-2">
            {projects.map((p, i) => (
              <ProjectCard key={p.slug} project={p} index={i} large={i === 0} />
            ))}
          </div>
        </div>
      </section>
      <CtaBand title="Ihr Raum als nächstes Projekt?" />
    </>
  );
}
