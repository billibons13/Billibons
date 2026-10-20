import { DemoAnalysis } from "@/components/landing/demo-analysis";
import { Faq } from "@/components/landing/faq";
import { Features } from "@/components/landing/features";
import { FinalCta } from "@/components/landing/final-cta";
import { Hero } from "@/components/landing/hero";
import { HowItWorks } from "@/components/landing/how-it-works";
import { Pricing } from "@/components/landing/pricing";
import { TrustStrip } from "@/components/landing/trust-strip";

export default function HomePage() {
  return (
    <>
      <Hero />
      <TrustStrip />
      <HowItWorks />
      <DemoAnalysis />
      <Features />
      <Pricing />
      <Faq />
      <FinalCta />
    </>
  );
}
