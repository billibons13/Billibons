import type { ComponentProps } from "react";
import { cn } from "@/lib/utils";

export function Container({ className, ...props }: ComponentProps<"div">) {
  return <div className={cn("mx-auto w-full max-w-6xl px-4 sm:px-6 lg:px-8", className)} {...props} />;
}

export function Section({ className, ...props }: ComponentProps<"section">) {
  return <section className={cn("relative py-16 sm:py-28", className)} {...props} />;
}

export function SectionHeader({
  eyebrow,
  title,
  subtitle,
  id,
  className,
}: {
  eyebrow?: string;
  title: string;
  subtitle?: string;
  id?: string;
  className?: string;
}) {
  return (
    <div className={cn("mx-auto max-w-2xl text-center", className)}>
      {eyebrow ? (
        <p className="mb-4 text-xs font-semibold uppercase tracking-[0.2em] text-accent-strong">{eyebrow}</p>
      ) : null}
      <h2 id={id} className="font-display text-3xl font-semibold tracking-tight text-balance sm:text-[2.6rem] sm:leading-[1.1]">
        {title}
      </h2>
      {subtitle ? <p className="mt-4 text-base leading-relaxed text-muted text-pretty sm:text-lg">{subtitle}</p> : null}
    </div>
  );
}
