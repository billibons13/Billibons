import Link from "next/link";
import { brand } from "@/lib/config/brand";
import { format, getMessages } from "@/lib/i18n";
import { cn } from "@/lib/utils";

export function LogoMark({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" className={cn("size-7", className)} aria-hidden="true" fill="none">
      <defs>
        <linearGradient id="logo-g" x1="4" y1="4" x2="28" y2="28" gradientUnits="userSpaceOnUse">
          <stop stopColor="#A5ABFF" />
          <stop offset="1" stopColor="#5EEAD4" />
        </linearGradient>
      </defs>
      <rect x="1" y="1" width="30" height="30" rx="9" fill="#0D0F15" stroke="url(#logo-g)" strokeOpacity="0.55" />
      <path d="M8 21.5 12.5 11l3.5 7 3.5-7L24 21.5" stroke="url(#logo-g)" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
      <circle cx="16" cy="24.5" r="1.4" fill="#5EEAD4" />
    </svg>
  );
}

export function Logo({ className }: { className?: string }) {
  const m = getMessages();
  return (
    <Link
      href="/"
      aria-label={format(m.nav.homeLabel, { brand: brand.name })}
      className={cn("inline-flex items-center gap-2.5 rounded-lg", className)}
    >
      <LogoMark />
      <span className="font-display text-[0.95rem] font-semibold tracking-[0.06em]">{brand.name}</span>
    </Link>
  );
}
