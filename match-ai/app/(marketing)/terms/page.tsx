import type { Metadata } from "next";
import { LegalPage } from "@/components/legal/legal-page";
import { getMessages } from "@/lib/i18n";

const page = getMessages().legal.terms;

export const metadata: Metadata = {
  title: page.metaTitle,
  alternates: { canonical: "/terms" },
};

export default function TermsPage() {
  return <LegalPage title={page.title} sections={page.sections} />;
}
