import type { MetadataRoute } from "next";
import { site } from "@/config/site";
import { publishedLocations } from "@/content/locations";
import { projects } from "@/content/projects";
import { services } from "@/content/services";

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();
  const entry = (path: string, priority: number, changeFrequency: "monthly" | "yearly" = "monthly") => ({
    url: `${site.url}${path}`,
    lastModified: now,
    changeFrequency,
    priority,
  });
  return [
    entry("/", 1),
    entry("/leistungen", 0.9),
    ...services.map((s) => entry(`/leistungen/${s.slug}`, 0.8)),
    entry("/projekte", 0.8),
    ...projects.map((p) => entry(`/projekte/${p.slug}`, 0.6)),
    entry("/ablauf", 0.6),
    entry("/ueber-uns", 0.6),
    entry("/kontakt", 0.8),
    ...publishedLocations.map((l) => entry(`/innenausbau/${l.slug}`, 0.7)),
    entry("/impressum", 0.1, "yearly"),
    entry("/datenschutz", 0.1, "yearly"),
  ];
}
