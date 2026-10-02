"use client";

import Image from "next/image";
import { useId, useState } from "react";
import { site } from "@/config/site";
import { asset, type AssetKey } from "@/content/assets";
import { VisualizationBadge } from "./SiteImage";

type Props = {
  before: AssetKey;
  after: AssetKey;
  sizes: string;
  ratio?: string;
  priority?: boolean;
  initial?: number;
};

/**
 * Vorher/Nachher-Vergleich.
 * Bedienung: Ziehen (Maus/Touch), Klick auf eine Position oder Pfeiltasten –
 * ein natives <input type="range"> sorgt für Barrierefreiheit ohne eigene Gestenlogik.
 */
export function BeforeAfterSlider({ before, after, sizes, ratio = "4 / 3", priority, initial = 50 }: Props) {
  const [pos, setPos] = useState(initial);
  const id = useId();
  const b = asset(before);
  const a = asset(after);
  const showBadge = site.labelVisualizations && (a.kind === "visualization" || b.kind === "visualization");

  return (
    <div className="relative w-full overflow-hidden bg-beton-100 select-none" style={{ aspectRatio: ratio }}>
      <Image src={a.src} alt={a.alt} fill sizes={sizes} priority={priority} className="object-cover" />
      <div className="absolute inset-0" style={{ clipPath: `inset(0 ${100 - pos}% 0 0)` }}>
        <Image src={b.src} alt={b.alt} fill sizes={sizes} priority={priority} className="object-cover" />
      </div>

      <span className="pointer-events-none absolute top-4 left-4 bg-ink/70 px-3 py-1.5 text-[0.68rem] font-semibold tracking-[0.2em] text-paper uppercase backdrop-blur-sm">
        Vorher
      </span>
      <span className="pointer-events-none absolute top-4 right-4 bg-paper/85 px-3 py-1.5 text-[0.68rem] font-semibold tracking-[0.2em] text-ink uppercase backdrop-blur-sm">
        Nachher
      </span>

      {/* Trennlinie + Griff */}
      <div className="pointer-events-none absolute inset-y-0 z-10 w-px bg-paper" style={{ left: `${pos}%` }} aria-hidden>
        <div className="absolute top-1/2 left-1/2 flex size-12 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full bg-paper text-ink shadow-[0_8px_30px_rgba(0,0,0,0.25)]">
          <svg viewBox="0 0 24 24" className="size-5" fill="none" stroke="currentColor" strokeWidth="1.8">
            <path d="m9 6-6 6 6 6M15 6l6 6-6 6" />
          </svg>
        </div>
      </div>

      <label htmlFor={id} className="sr-only">
        Vorher-Nachher-Vergleich: Regler nach links oder rechts bewegen
      </label>
      <input
        id={id}
        type="range"
        min={0}
        max={100}
        step={0.5}
        value={pos}
        onChange={(e) => setPos(Number(e.target.value))}
        className="ba-range absolute inset-0 z-20 h-full w-full cursor-ew-resize touch-pan-y opacity-0"
        aria-valuetext={`${Math.round(pos)} % Vorher sichtbar`}
      />

      {showBadge && <VisualizationBadge className="bottom-3 left-3" />}
    </div>
  );
}
