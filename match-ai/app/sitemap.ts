import type { MetadataRoute } from "next";
import { getAppUrl } from "@/lib/config/env";

const PUBLIC_ROUTES: { path: string; priority: number }[] = [
  { path: "/", priority: 1 },
  { path: "/register", priority: 0.8 },
  { path: "/login", priority: 0.5 },
  { path: "/privacy", priority: 0.3 },
  { path: "/terms", priority: 0.3 },
  { path: "/imprint", priority: 0.3 },
];

export default function sitemap(): MetadataRoute.Sitemap {
  const base = getAppUrl();
  return PUBLIC_ROUTES.map(({ path, priority }) => ({
    url: `${base}${path === "/" ? "" : path}`,
    changeFrequency: "monthly",
    priority,
  }));
}
