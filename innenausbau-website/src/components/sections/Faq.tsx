import type { FaqItem } from "@/content/faq";
import { faqLd } from "@/lib/seo/jsonld";
import { JsonLd } from "@/components/ui/JsonLd";
import { PlusIcon } from "@/components/ui/Icons";
import { SectionHeading } from "@/components/ui/SectionHeading";

/** Native <details> – zugänglich, ohne JavaScript. */
export function Faq({ items, title = "Häufige Fragen" }: { items: FaqItem[]; title?: string }) {
  return (
    <section className="section">
      <div className="container-x grid gap-12 lg:grid-cols-12">
        <div className="lg:col-span-4">
          <SectionHeading eyebrow="FAQ" title={title} />
        </div>
        <div className="divide-y divide-beton-100 border-y border-beton-100 lg:col-span-7 lg:col-start-6">
          {items.map((f) => (
            <details key={f.q} className="group" data-reveal>
              <summary className="flex min-h-16 cursor-pointer list-none items-center justify-between gap-6 py-6 text-lg font-medium tracking-tight">
                {f.q}
                <PlusIcon className="size-5 shrink-0 text-beton-500 transition-transform duration-300 group-open:rotate-45 group-open:text-ziegel" />
              </summary>
              <p className="max-w-2xl pb-7 leading-relaxed text-anthrazit/75">{f.a}</p>
            </details>
          ))}
        </div>
      </div>
      <JsonLd data={faqLd(items)} />
    </section>
  );
}
