import Link from "next/link";
import type { Project } from "@/content/projects";
import { SiteImage } from "@/components/ui/SiteImage";

export function ProjectCard({ project, index = 0, large }: { project: Project; index?: number; large?: boolean }) {
  return (
    <Link
      href={`/projekte/${project.slug}`}
      className="img-zoom group block"
      data-reveal
      style={{ "--reveal-delay": `${(index % 2) * 100}ms` } as React.CSSProperties}
    >
      <SiteImage
        id={project.after}
        ratio={large ? "16 / 10" : "4 / 3"}
        sizes={large ? "(min-width: 1024px) 66vw, 100vw" : "(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw"}
      />
      <div className="mt-5 flex flex-wrap items-baseline justify-between gap-x-6 gap-y-1">
        <h3 className="text-h3 font-semibold transition-colors group-hover:text-ziegel">{project.title}</h3>
        <p className="text-sm text-beton-500">{project.objectType}</p>
      </div>
      <p className="mt-2 text-sm text-anthrazit/65">{project.services.join(" · ")}</p>
      {project.isExample && (
        <p className="mt-2 text-xs tracking-wide text-beton-500 uppercase">Beispielprojekt</p>
      )}
    </Link>
  );
}
