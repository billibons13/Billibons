import Link from "next/link";
import { site } from "@/config/site";

/** Wortmarke – bis zum finalen Logo. Quadrat = Grundriss, Akzent = Ziegel. */
export function Logo({ tone = "dark" }: { tone?: "dark" | "light" }) {
  return (
    <Link href="/" className="group flex items-center gap-3" aria-label={`${site.name} – Startseite`}>
      <span className="relative block size-7" aria-hidden>
        <span className={`absolute inset-0 border-[1.5px] ${tone === "dark" ? "border-ink" : "border-paper"}`} />
        <span className="absolute right-0 bottom-0 size-3 bg-ziegel transition-transform duration-500 group-hover:-translate-x-1 group-hover:-translate-y-1" />
      </span>
      <span className="leading-none">
        <span className={`block text-[1.05rem] font-bold tracking-[0.18em] ${tone === "dark" ? "text-ink" : "text-paper"}`}>
          {site.name}
        </span>
        <span className={`mt-1 block text-[0.6rem] tracking-[0.24em] uppercase ${tone === "dark" ? "text-beton-500" : "text-paper/60"}`}>
          {site.tagline}
        </span>
      </span>
    </Link>
  );
}
