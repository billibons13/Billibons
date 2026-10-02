import type { Metadata, Viewport } from "next";
import { Inter_Tight } from "next/font/google";
import { site } from "@/config/site";
import { localBusinessLd } from "@/lib/seo/jsonld";
import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import { MobileCtaBar } from "@/components/layout/MobileCtaBar";
import { JsonLd } from "@/components/ui/JsonLd";
import { RevealObserver } from "@/components/ui/RevealObserver";
import "./globals.css";

const font = Inter_Tight({ subsets: ["latin", "latin-ext"], variable: "--font-inter-tight", display: "swap" });

export const metadata: Metadata = {
  metadataBase: new URL(site.url),
  title: {
    default: `Innenausbau, Renovierung & Sanierung in Schleswig-Holstein | ${site.name}`,
    template: `%s | ${site.name}`,
  },
  description:
    "Innenausbau, Renovierung und Sanierung in Schleswig-Holstein und Hamburg: Trockenbau, Putz, Maler, Boden, Fliesen und Badsanierung – präzise geplant und sauber umgesetzt.",
  applicationName: site.name,
  formatDetection: { telephone: false },
};

export const viewport: Viewport = {
  themeColor: "#f5f3ef",
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="de" className={font.variable} suppressHydrationWarning>
      <head>
        {/* Reveal-Animationen nur mit aktivem JS – ohne JS bleibt alles sichtbar */}
        <script dangerouslySetInnerHTML={{ __html: "document.documentElement.classList.add('js')" }} />
      </head>
      <body>
        <a href="#inhalt" className="sr-only z-[60] bg-ink px-4 py-3 text-paper focus:not-sr-only focus:fixed focus:top-2 focus:left-2">
          Zum Inhalt springen
        </a>
        <Header />
        <main id="inhalt">{children}</main>
        <Footer />
        <MobileCtaBar />
        <RevealObserver />
        <JsonLd data={localBusinessLd()} />
      </body>
    </html>
  );
}
