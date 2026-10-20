import { CheckCircle2, ImageIcon, ScanLine, Sparkles, TrendingDown, TrendingUp } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { getMessages } from "@/lib/i18n";
import { ConfidenceRing } from "./confidence-ring";

/** Decorative mock of the analysis dashboard. Labeled as demo — no real data. */
export function AnalysisMock() {
  const m = getMessages();
  const mock = m.landing.mock;
  const demo = m.landing.demo;

  return (
    <figure aria-label={mock.label} className="relative mx-auto w-full max-w-5xl">
      <div aria-hidden="true" className="absolute -inset-x-10 -top-16 bottom-0 -z-10 rounded-[3rem] bg-[radial-gradient(60%_60%_at_50%_30%,rgb(139_147_255/0.22),transparent_70%)] blur-2xl" />
      <div className="glass overflow-hidden rounded-[1.6rem] bg-surface/70 shadow-glow-soft">
        <div className="flex items-center justify-between border-b border-border px-4 py-3 sm:px-5">
          <div className="flex items-center gap-1.5" aria-hidden="true">
            <span className="size-2.5 rounded-full bg-white/15" />
            <span className="size-2.5 rounded-full bg-white/10" />
            <span className="size-2.5 rounded-full bg-white/10" />
          </div>
          <Badge variant="warning">{m.common.demoBadge}</Badge>
        </div>

        <div className="grid gap-4 p-4 sm:p-5 md:grid-cols-[0.9fr_1.1fr_0.9fr]">
          {/* Uploaded screenshot (abstract) */}
          <div className="rounded-xl border border-border bg-surface-2/70 p-4">
            <div className="flex items-center gap-2 text-xs text-muted">
              <ImageIcon className="size-3.5" aria-hidden="true" />
              {mock.upload}
            </div>
            <div className="mt-4 space-y-3 rounded-lg border border-border bg-background/60 p-4" aria-hidden="true">
              <div className="flex items-center justify-between">
                <span className="h-2 w-16 rounded-full bg-white/15" />
                <span className="h-2 w-8 rounded-full bg-accent-2/40" />
              </div>
              <div className="flex items-center justify-between gap-3 pt-2">
                <div className="flex items-center gap-2">
                  <span className="size-7 rounded-full bg-gradient-to-br from-accent/60 to-accent/20" />
                  <span className="text-sm font-medium">{demo.teamA}</span>
                </div>
                <span className="font-display text-sm text-subtle">vs</span>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium">{demo.teamB}</span>
                  <span className="size-7 rounded-full bg-gradient-to-br from-accent-2/60 to-accent-2/20" />
                </div>
              </div>
              <div className="grid grid-cols-3 gap-2 pt-2">
                <span className="h-7 rounded-md bg-white/[0.06]" />
                <span className="h-7 rounded-md bg-white/[0.06]" />
                <span className="h-7 rounded-md bg-white/[0.06]" />
              </div>
            </div>
            <div className="mt-4 flex items-center gap-2 text-xs text-positive">
              <CheckCircle2 className="size-3.5" aria-hidden="true" />
              {mock.recognized}
            </div>
          </div>

          {/* Summary */}
          <div className="rounded-xl border border-border bg-surface-2/70 p-4">
            <div className="flex items-center gap-2 text-xs text-muted">
              <ScanLine className="size-3.5" aria-hidden="true" />
              {mock.analyzing}
            </div>
            <div className="mt-4 flex items-center gap-4">
              <ConfidenceRing value={0.78} label={mock.confidence} size={92} gradientId="ring-hero" />
              <div className="min-w-0">
                <p className="text-xs uppercase tracking-[0.14em] text-subtle">{mock.summary}</p>
                <p className="mt-1.5 text-sm leading-relaxed text-foreground/90">{mock.summaryText}</p>
              </div>
            </div>
            <div className="mt-5 space-y-2.5" aria-hidden="true">
              {[82, 64, 48].map((w) => (
                <div key={w} className="h-1.5 rounded-full bg-white/[0.06]">
                  <div className="h-full rounded-full bg-gradient-to-r from-accent to-accent-2" style={{ width: `${w}%` }} />
                </div>
              ))}
            </div>
          </div>

          {/* Signals */}
          <div className="rounded-xl border border-border bg-surface-2/70 p-4">
            <div className="flex items-center gap-2 text-xs text-muted">
              <Sparkles className="size-3.5" aria-hidden="true" />
              {mock.signals}
            </div>
            <ul className="mt-4 space-y-2.5 text-sm">
              <li className="flex items-center justify-between gap-2 rounded-lg bg-positive/[0.07] px-3 py-2">
                <span className="flex items-center gap-2">
                  <TrendingUp className="size-3.5 text-positive" aria-hidden="true" />
                  {demo.factors.form.title}
                </span>
                <span className="text-xs text-positive">{mock.positive}</span>
              </li>
              <li className="flex items-center justify-between gap-2 rounded-lg bg-positive/[0.07] px-3 py-2">
                <span className="flex items-center gap-2">
                  <TrendingUp className="size-3.5 text-positive" aria-hidden="true" />
                  {demo.factors.home.title}
                </span>
                <span className="text-xs text-positive">{mock.positive}</span>
              </li>
              <li className="flex items-center justify-between gap-2 rounded-lg bg-negative/[0.07] px-3 py-2">
                <span className="flex items-center gap-2">
                  <TrendingDown className="size-3.5 text-negative" aria-hidden="true" />
                  {mock.risks}
                </span>
                <span className="text-xs text-negative">{mock.negative}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <figcaption className="mt-4 text-center text-xs text-subtle">{m.common.illustrativeNote}</figcaption>
    </figure>
  );
}
