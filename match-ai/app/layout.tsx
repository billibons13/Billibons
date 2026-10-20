import type { Metadata, Viewport } from "next";
import { Inter, Inter_Tight } from "next/font/google";
import { CookieConsent } from "@/components/layout/cookie-consent";
import { ToastProvider } from "@/components/ui/toast";
import { brand } from "@/lib/config/brand";
import { getAppUrl } from "@/lib/config/env";
import { DEFAULT_LOCALE } from "@/lib/i18n/config";
import { getMessages } from "@/lib/i18n";
import "./globals.css";

const inter = Inter({ variable: "--font-inter", subsets: ["latin"], display: "swap" });
const interTight = Inter_Tight({ variable: "--font-inter-tight", subsets: ["latin"], display: "swap" });

const m = getMessages();

export const metadata: Metadata = {
  metadataBase: new URL(getAppUrl()),
  title: { default: `${brand.name} — ${m.landing.meta.title}`, template: `%s · ${brand.name}` },
  description: m.landing.meta.description,
  applicationName: brand.name,
  alternates: { canonical: "/" },
  openGraph: {
    type: "website",
    siteName: brand.name,
    title: `${brand.name} — ${m.landing.meta.title}`,
    description: m.landing.meta.description,
    url: "/",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: `${brand.name} — ${m.landing.meta.title}`,
    description: m.landing.meta.description,
  },
  robots: { index: true, follow: true },
};

export const viewport: Viewport = {
  themeColor: "#07080c",
  colorScheme: "dark",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang={DEFAULT_LOCALE} className={`${inter.variable} ${interTight.variable} antialiased`}>
      <body className="min-h-dvh bg-background text-foreground">
        <a
          href="#main"
          className="sr-only rounded-full bg-foreground px-4 py-2 text-sm font-medium text-background focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[100]"
        >
          {m.common.skipToContent}
        </a>
        <ToastProvider>
          {children}
          <CookieConsent />
        </ToastProvider>
      </body>
    </html>
  );
}
