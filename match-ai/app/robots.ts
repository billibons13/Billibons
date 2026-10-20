import type { MetadataRoute } from "next";
import { getAppUrl } from "@/lib/config/env";

export default function robots(): MetadataRoute.Robots {
  const base = getAppUrl();
  return {
    rules: [{ userAgent: "*", allow: "/", disallow: ["/dashboard", "/auth/", "/reset-password"] }],
    sitemap: `${base}/sitemap.xml`,
    host: base,
  };
}
