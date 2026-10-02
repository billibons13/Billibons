import Image from "next/image";
import { site } from "@/config/site";
import { asset, type AssetKey } from "@/content/assets";

type Props = {
  id: AssetKey;
  sizes: string;
  className?: string;
  imgClassName?: string;
  priority?: boolean;
  /** Seitenverhältnis-Box; ohne Angabe füllt das Bild den Elterncontainer (fill) */
  ratio?: string;
  label?: boolean;
};

/**
 * Responsive Bild (AVIF/WebP via next/image, lazy by default).
 * KI-Visualisierungen werden – solange `site.labelVisualizations` aktiv ist – dezent gekennzeichnet.
 */
export function SiteImage({ id, sizes, className = "", imgClassName = "", priority, ratio, label = true }: Props) {
  const a = asset(id);
  return (
    <div className={`relative overflow-hidden bg-beton-100 ${className}`} style={ratio ? { aspectRatio: ratio } : undefined}>
      <Image
        src={a.src}
        alt={a.alt}
        fill
        sizes={sizes}
        priority={priority}
        fetchPriority={priority ? "high" : undefined}
        className={`object-cover ${imgClassName}`}
      />
      {label && site.labelVisualizations && a.kind === "visualization" && <VisualizationBadge />}
    </div>
  );
}

export function VisualizationBadge({ className = "bottom-3 right-3" }: { className?: string }) {
  return (
    <span
      className={`pointer-events-none absolute z-10 bg-ink/55 px-2 py-1 text-[0.62rem] font-medium tracking-[0.14em] text-paper/90 uppercase backdrop-blur-sm ${className}`}
    >
      Visualisierung
    </span>
  );
}
