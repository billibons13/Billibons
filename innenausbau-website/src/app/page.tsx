import { site } from "@/config/site";
import { faq } from "@/content/faq";
import { pageMetadata } from "@/lib/seo/metadata";
import { BeforeAfterShowcase } from "@/components/sections/BeforeAfterShowcase";
import { CtaBand } from "@/components/sections/CtaBand";
import { Faq } from "@/components/sections/Faq";
import { FeaturedProjects } from "@/components/sections/FeaturedProjects";
import { Hero } from "@/components/sections/Hero";
import { MaterialsQuality } from "@/components/sections/MaterialsQuality";
import { ProcessSteps } from "@/components/sections/ProcessSteps";
import { RegionBlock } from "@/components/sections/RegionBlock";
import { ServicesPreview } from "@/components/sections/ServicesPreview";
import { Testimonials } from "@/components/sections/Testimonials";
import { TrustBar } from "@/components/sections/TrustBar";
import { WhyUs } from "@/components/sections/WhyUs";

export const metadata = {
  ...pageMetadata({
    title: "Innenausbau, Renovierung & Sanierung in Schleswig-Holstein",
    description:
      "Innenausbau, Renovierung und Sanierung in Schleswig-Holstein und Hamburg: Trockenbau, Putz, Maler, Boden, Fliesen und Badsanierung – präzise geplant und sauber umgesetzt.",
    path: "/",
  }),
  title: { absolute: `Innenausbau, Renovierung & Sanierung in Schleswig-Holstein | ${site.name}` },
};

export default function HomePage() {
  return (
    <>
      <Hero />
      <TrustBar />
      <ServicesPreview />
      <BeforeAfterShowcase />
      <FeaturedProjects />
      <WhyUs />
      <ProcessSteps />
      <MaterialsQuality />
      <Testimonials />
      <Faq items={faq.slice(0, 6)} />
      <RegionBlock />
      <CtaBand />
    </>
  );
}
