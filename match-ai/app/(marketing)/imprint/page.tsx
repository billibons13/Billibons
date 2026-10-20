import type { Metadata } from "next";
import { LegalPage } from "@/components/legal/legal-page";
import { getMessages } from "@/lib/i18n";

const page = getMessages().legal.imprint;

export const metadata: Metadata = {
  title: page.metaTitle,
  alternates: { canonical: "/imprint" },
};

export default function ImprintPage() {
  return <LegalPage title={page.title} sections={page.sections} />;
}
