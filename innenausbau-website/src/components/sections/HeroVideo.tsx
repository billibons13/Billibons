"use client";

import { useEffect, useRef } from "react";

/**
 * Lädt das Hero-Video erst nach dem ersten Rendern und nur, wenn sinnvoll:
 * Desktop/Tablet, keine reduzierte Bewegung, kein Datensparmodus.
 * Das Poster (next/image, priority) bleibt LCP-Element → gute Core Web Vitals.
 */
export function HeroVideo({ src }: { src: string }) {
  const ref = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const v = ref.current;
    if (!v) return;
    const conn = (navigator as Navigator & { connection?: { saveData?: boolean } }).connection;
    const ok =
      window.matchMedia("(min-width: 768px)").matches &&
      !window.matchMedia("(prefers-reduced-motion: reduce)").matches &&
      !conn?.saveData;
    if (!ok) return;
    const start = () => {
      v.src = src;
      v.play().then(() => v.classList.add("opacity-100")).catch(() => {});
    };
    if (document.readyState === "complete") setTimeout(start, 600);
    else window.addEventListener("load", () => setTimeout(start, 600), { once: true });
  }, [src]);

  return (
    <video
      ref={ref}
      muted
      loop
      playsInline
      preload="none"
      aria-hidden
      className="absolute inset-0 h-full w-full object-cover opacity-0 transition-opacity duration-1000"
    />
  );
}
