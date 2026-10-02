import type { ReactNode } from "react";

type Props = {
  eyebrow?: string;
  title: ReactNode;
  intro?: ReactNode;
  as?: "h1" | "h2";
  align?: "left" | "split";
  tone?: "light" | "dark";
};

export function SectionHeading({ eyebrow, title, intro, as: Tag = "h2", align = "left", tone = "light" }: Props) {
  const muted = tone === "dark" ? "text-paper/65" : "text-anthrazit/75";
  return (
    <div className={align === "split" ? "grid gap-6 lg:grid-cols-12 lg:items-end" : "max-w-3xl"}>
      <div className={align === "split" ? "lg:col-span-7" : ""}>
        {eyebrow && (
          <p className={`eyebrow mb-5 flex items-center gap-3 ${tone === "dark" ? "text-paper/50" : ""}`} data-reveal>
            <span className="h-px w-8 bg-ziegel" aria-hidden />
            {eyebrow}
          </p>
        )}
        <Tag className={`${Tag === "h1" ? "text-display" : "text-h2"} font-semibold text-balance`} data-reveal>
          {title}
        </Tag>
      </div>
      {intro && (
        <p
          className={`text-lg leading-relaxed text-pretty ${muted} ${align === "split" ? "lg:col-span-5 lg:pb-2" : "mt-6"}`}
          data-reveal
          style={{ "--reveal-delay": "120ms" } as React.CSSProperties}
        >
          {intro}
        </p>
      )}
    </div>
  );
}
