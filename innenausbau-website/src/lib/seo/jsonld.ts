import { isPlaceholder, site } from "@/config/site";
import { asset } from "@/content/assets";
import type { FaqItem } from "@/content/faq";
import type { Service } from "@/content/services";

const BUSINESS_ID = `${site.url}/#business`;

const clean = (v: string) => (isPlaceholder(v) ? undefined : v);

/** LocalBusiness – Platzhalter werden automatisch weggelassen, keine erfundenen Bewertungen */
export function localBusinessLd() {
  const a = site.address;
  const hasAddress = !isPlaceholder(a.street) && !isPlaceholder(a.city);
  return {
    "@context": "https://schema.org",
    "@type": ["HomeAndConstructionBusiness", "GeneralContractor"],
    "@id": BUSINESS_ID,
    name: site.name,
    legalName: clean(site.legalName),
    url: site.url,
    slogan: site.claim,
    telephone: clean(site.contact.phone),
    email: clean(site.contact.email),
    image: asset("hero").src,
    address: hasAddress
      ? {
          "@type": "PostalAddress",
          streetAddress: a.street,
          postalCode: clean(a.postalCode),
          addressLocality: a.city,
          addressRegion: a.region,
          addressCountry: a.country,
        }
      : undefined,
    geo: a.geo ? { "@type": "GeoCoordinates", latitude: a.geo.lat, longitude: a.geo.lng } : undefined,
    areaServed: [
      { "@type": "State", name: "Schleswig-Holstein" },
      { "@type": "City", name: "Hamburg" },
    ],
    foundingDate: site.facts.foundedYear ? String(site.facts.foundedYear) : undefined,
    openingHoursSpecification: site.openingHours.length
      ? site.openingHours.map((o) => ({
          "@type": "OpeningHoursSpecification",
          dayOfWeek: o.days,
          opens: o.opens,
          closes: o.closes,
        }))
      : undefined,
    sameAs: Object.values(site.social).filter(Boolean),
  };
}

export function serviceLd(service: Service) {
  return {
    "@context": "https://schema.org",
    "@type": "Service",
    name: service.title,
    serviceType: service.title,
    description: service.seo.description,
    url: `${site.url}/leistungen/${service.slug}`,
    provider: { "@id": BUSINESS_ID },
    areaServed: { "@type": "State", name: "Schleswig-Holstein" },
  };
}

export function faqLd(items: FaqItem[]) {
  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: items
      .filter((i) => !i.a.startsWith("["))
      .map((i) => ({ "@type": "Question", name: i.q, acceptedAnswer: { "@type": "Answer", text: i.a } })),
  };
}

export function breadcrumbLd(trail: { name: string; path: string }[]) {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [{ name: "Start", path: "/" }, ...trail].map((t, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: t.name,
      item: `${site.url}${t.path}`,
    })),
  };
}
