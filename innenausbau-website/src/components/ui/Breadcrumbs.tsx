import Link from "next/link";
import { breadcrumbLd } from "@/lib/seo/jsonld";
import { JsonLd } from "./JsonLd";

export function Breadcrumbs({ trail }: { trail: { name: string; path: string }[] }) {
  return (
    <>
      <nav aria-label="Brotkrumen" className="eyebrow flex flex-wrap items-center gap-2 text-beton-500">
        <Link href="/" className="hover:text-ink">
          Start
        </Link>
        {trail.map((t, i) => (
          <span key={t.path} className="flex items-center gap-2">
            <span aria-hidden>/</span>
            {i === trail.length - 1 ? (
              <span aria-current="page" className="text-ink">
                {t.name}
              </span>
            ) : (
              <Link href={t.path} className="hover:text-ink">
                {t.name}
              </Link>
            )}
          </span>
        ))}
      </nav>
      <JsonLd data={breadcrumbLd(trail)} />
    </>
  );
}
