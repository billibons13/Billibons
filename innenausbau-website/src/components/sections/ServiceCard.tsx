import Link from "next/link";
import type { Service } from "@/content/services";
import { SiteImage } from "@/components/ui/SiteImage";
import { ArrowIcon } from "@/components/ui/Button";

export function ServiceCard({ service, index }: { service: Service; index: number }) {
  return (
    <Link
      href={`/leistungen/${service.slug}`}
      className="img-zoom group block"
      data-reveal
      style={{ "--reveal-delay": `${(index % 3) * 90}ms` } as React.CSSProperties}
    >
      <SiteImage id={service.image} ratio="4 / 3" sizes="(min-width: 1024px) 30vw, (min-width: 640px) 45vw, 100vw" label={false} />
      <div className="mt-5 flex items-start justify-between gap-6 border-t border-beton-100 pt-5">
        <div>
          <p className="text-xs tracking-[0.2em] text-beton-500 tabular-nums">{String(index + 1).padStart(2, "0")}</p>
          <h3 className="text-h3 mt-2 font-semibold">{service.title}</h3>
          <p className="mt-2 text-anthrazit/70">{service.short}</p>
        </div>
        <span className="mt-6 flex size-11 shrink-0 items-center justify-center border border-ink/15 transition-colors duration-300 group-hover:border-ziegel group-hover:bg-ziegel group-hover:text-paper">
          <ArrowIcon />
        </span>
      </div>
    </Link>
  );
}
