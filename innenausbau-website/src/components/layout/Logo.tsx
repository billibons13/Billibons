import Link from "next/link";
import { useId } from "react";
import { site } from "@/config/site";

type Tone = "dark" | "light";

/**
 * Logo nach der Skizze des Inhabers: Kuppel (Halbkreis auf Grundlinie),
 * „AKKERMAN“ im Bogen, „SK“ in der Mitte. Die Grundlinie trägt den Ziegel-Akzent.
 */
export function BrandMark({ tone = "dark", className = "w-56" }: { tone?: Tone; className?: string }) {
  const id = useId().replace(/:/g, "");
  const ink = tone === "dark" ? "var(--color-ink)" : "var(--color-paper)";
  return (
    <svg viewBox="0 0 240 140" className={className} role="img" aria-label={`${site.name} SK – Logo`}>
      <defs>
        <path id={`arc-${id}`} d="M38 128 A82 82 0 0 1 202 128" />
      </defs>
      <path d="M14 128 A106 106 0 0 1 226 128" fill="none" stroke={ink} strokeWidth="4" />
      <path d="M4 128 H236" stroke="var(--color-ziegel)" strokeWidth="5" />
      <text fill={ink} fontSize="25" fontWeight="700" letterSpacing="5" style={{ fontFamily: "var(--font-sans)" }}>
        <textPath href={`#arc-${id}`} startOffset="50%" textAnchor="middle">
          {site.name}
        </textPath>
      </text>
      <text
        x="120"
        y="116"
        textAnchor="middle"
        fill={ink}
        fontSize="42"
        fontWeight="800"
        letterSpacing="2"
        style={{ fontFamily: "var(--font-sans)" }}
      >
        SK
      </text>
    </svg>
  );
}

/** Kompaktes Zeichen (Kuppel + SK) – für Header und Favicon-Größen */
export function BrandIcon({ tone = "dark", className = "size-9" }: { tone?: Tone; className?: string }) {
  const ink = tone === "dark" ? "var(--color-ink)" : "var(--color-paper)";
  return (
    <svg viewBox="0 0 64 48" className={className} aria-hidden>
      <path d="M6 42 A26 26 0 0 1 58 42" fill="none" stroke={ink} strokeWidth="3" />
      <path d="M2 42 H62" stroke="var(--color-ziegel)" strokeWidth="3.5" />
      <text x="32" y="38" textAnchor="middle" fill={ink} fontSize="19" fontWeight="800" style={{ fontFamily: "var(--font-sans)" }}>
        SK
      </text>
    </svg>
  );
}

/** Header-Variante: Zeichen + Wortmarke (der Bogen-Schriftzug wäre in 40 px nicht lesbar) */
export function Logo({ tone = "dark" }: { tone?: Tone }) {
  return (
    <Link href="/" className="group flex items-center gap-3" aria-label={`${site.name} – Startseite`}>
      <BrandIcon tone={tone} className="h-8 w-11 transition-transform duration-500 group-hover:-translate-y-0.5" />
      <span className="leading-none">
        <span className={`block text-[1.05rem] font-bold tracking-[0.2em] ${tone === "dark" ? "text-ink" : "text-paper"}`}>
          {site.name}
        </span>
        <span className={`mt-1 block text-[0.6rem] tracking-[0.24em] uppercase ${tone === "dark" ? "text-beton-500" : "text-paper/60"}`}>
          {site.tagline}
        </span>
      </span>
    </Link>
  );
}
