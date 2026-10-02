import type { Metadata } from "next";
import { site } from "@/config/site";
import { asset, type AssetKey } from "@/content/assets";

type PageMeta = {
  title: string;
  description: string;
  path: string;
  image?: AssetKey;
  noindex?: boolean;
};

/** Einheitliche Metadaten inkl. Canonical und Open Graph */
export function pageMetadata({ title, description, path, image = "hero", noindex }: PageMeta): Metadata {
  const img = asset(image);
  const url = `${site.url}${path}`;
  return {
    title,
    description,
    alternates: {
      canonical: url,
      // Vorbereitet für weitere Sprachen: { "de-DE": url, "en": `${site.url}/en${path}` }
      languages: { "de-DE": url },
    },
    openGraph: {
      type: "website",
      locale: site.locale,
      url,
      siteName: site.name,
      title,
      description,
      images: [{ url: img.src, width: img.width, height: img.height, alt: img.alt }],
    },
    twitter: { card: "summary_large_image", title, description, images: [img.src] },
    robots: noindex ? { index: false, follow: true } : undefined,
  };
}
