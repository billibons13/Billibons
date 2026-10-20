import type { Messages } from "@/lib/i18n";

export function getNavLinks(m: Messages) {
  return [
    { href: "/#how-it-works", label: m.nav.howItWorks },
    { href: "/#features", label: m.nav.features },
    { href: "/#pricing", label: m.nav.pricing },
    { href: "/#faq", label: m.nav.faq },
  ];
}
