import type { Metadata } from "next";
import { LegalPage } from "@/components/legal/legal-page";
import { getMessages } from "@/lib/i18n";

const page = getMessages().legal.privacy;

export const metadata: Metadata = {
  title: page.metaTitle,
  alternates: { canonical: "/privacy" },
};

export default function PrivacyPage() {
  return <LegalPage title={page.title} sections={page.sections} />;
}
