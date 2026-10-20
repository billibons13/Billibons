import { cn } from "@/lib/utils";

/** Circular gauge for a 0..1 value. Purely visual; the value is also rendered as text. */
export function ConfidenceRing({
  value,
  label,
  size = 96,
  gradientId,
  className,
}: {
  value: number;
  label: string;
  size?: number;
  /** Must be unique per page (SVG ids are global). */
  gradientId: string;
  className?: string;
}) {
  const clamped = Math.min(1, Math.max(0, value));
  const radius = 42;
  const circumference = 2 * Math.PI * radius;
  const percent = Math.round(clamped * 100);

  return (
    <div className={cn("relative inline-flex items-center justify-center", className)} style={{ width: size, height: size }}>
      <svg viewBox="0 0 100 100" className="size-full -rotate-90" aria-hidden="true">
        <defs>
          <linearGradient id={gradientId} x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#A5ABFF" />
            <stop offset="100%" stopColor="#5EEAD4" />
          </linearGradient>
        </defs>
        <circle cx="50" cy="50" r={radius} stroke="rgb(255 255 255 / 0.08)" strokeWidth="7" fill="none" />
        <circle
          cx="50"
          cy="50"
          r={radius}
          stroke={`url(#${gradientId})`}
          strokeWidth="7"
          strokeLinecap="round"
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={circumference * (1 - clamped)}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span
          className={cn("font-display font-semibold tabular-nums tracking-tight", size >= 110 ? "text-3xl" : "text-base")}
        >
          {percent}%
        </span>
        {size >= 110 ? <span className="mt-0.5 text-[0.65rem] uppercase tracking-[0.14em] text-subtle">{label}</span> : null}
        {size < 110 ? <span className="sr-only">{label}</span> : null}
      </div>
    </div>
  );
}
