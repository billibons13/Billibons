import type { ReactNode } from "react";
import { Breadcrumbs } from "@/components/ui/Breadcrumbs";

export function PageHeader({
  trail,
  eyebrow,
  title,
  intro,
  children,
}: {
  trail: { name: string; path: string }[];
  eyebrow?: string;
  title: ReactNode;
  intro?: ReactNode;
  children?: ReactNode;
}) {
  return (
    <section className="pt-8 pb-14 sm:pt-12 lg:pt-16 lg:pb-20">
      <div className="container-x">
        <Breadcrumbs trail={trail} />
        <div className="mt-12 grid gap-8 lg:grid-cols-12 lg:items-end">
          <div className="lg:col-span-8">
            {eyebrow && (
              <p className="eyebrow flex items-center gap-3" data-reveal>
                <span className="h-px w-8 bg-ziegel" aria-hidden />
                {eyebrow}
              </p>
            )}
            <h1 className="mt-5 text-[clamp(2.5rem,6vw,5.25rem)] leading-[0.98] font-semibold tracking-[-0.035em] text-balance" data-reveal>
              {title}
            </h1>
          </div>
          {intro && (
            <p className="text-lg leading-relaxed text-anthrazit/75 text-pretty lg:col-span-4 lg:pb-2" data-reveal>
              {intro}
            </p>
          )}
        </div>
        {children}
      </div>
    </section>
  );
}
