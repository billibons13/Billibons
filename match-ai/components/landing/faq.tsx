import { Plus } from "lucide-react";
import { Container, Section, SectionHeader } from "@/components/ui/container";
import { DEFAULT_IMAGE_RETENTION_DAYS, DEFAULT_MAX_UPLOAD_MB } from "@/lib/config/upload";
import { PLAN_LIMITS } from "@/lib/config/plans";
import { format, getMessages } from "@/lib/i18n";

/** Accessible accordion built on native <details>/<summary>. */
export function Faq() {
  const faq = getMessages().landing.faq;
  const vars = {
    maxMb: DEFAULT_MAX_UPLOAD_MB,
    freeCount: PLAN_LIMITS.free,
    retentionDays: DEFAULT_IMAGE_RETENTION_DAYS,
  };

  return (
    <Section id="faq" aria-labelledby="faq-title">
      <Container className="max-w-3xl">
        <SectionHeader id="faq-title" eyebrow={faq.eyebrow} title={faq.title} />
        <div className="mt-14 divide-y divide-border rounded-2xl border border-border bg-surface/40">
          {faq.items.map((item) => (
            <details key={item.q} className="group px-5 sm:px-7">
              <summary className="flex cursor-pointer items-center justify-between gap-6 rounded-lg py-5 text-left text-[0.98rem] font-medium">
                {item.q}
                <Plus
                  className="size-4 shrink-0 text-muted transition-transform duration-200 group-open:rotate-45"
                  aria-hidden="true"
                />
              </summary>
              <p className="-mt-1 pb-6 text-sm leading-relaxed text-muted">{format(item.a, vars)}</p>
            </details>
          ))}
        </div>
      </Container>
    </Section>
  );
}
