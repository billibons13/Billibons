import Link from "next/link";
import { telHref, whatsappHref } from "@/config/site";
import { PhoneIcon, WhatsAppIcon } from "@/components/ui/Icons";

/**
 * Feste Kontaktleiste auf Mobilgeräten: Anrufen, WhatsApp oder Anfrage – jeweils ein Tipp.
 * Sitzt über der Safe-Area (iPhone Home-Indicator).
 */
export function MobileCtaBar() {
  return (
    <div className="fixed inset-x-0 bottom-0 z-40 border-t border-ink/10 bg-paper/95 pb-[env(safe-area-inset-bottom)] backdrop-blur-md sm:hidden">
      <div className="grid grid-cols-[1fr_1fr_1.4fr]">
        <a href={telHref} className="flex min-h-16 flex-col items-center justify-center gap-1 text-[0.72rem] font-medium">
          <PhoneIcon className="size-5" />
          Anrufen
        </a>
        <a
          href={whatsappHref}
          target="_blank"
          rel="noopener"
          className="flex min-h-16 flex-col items-center justify-center gap-1 border-l border-ink/10 text-[0.72rem] font-medium"
        >
          <WhatsAppIcon className="size-5" />
          WhatsApp
        </a>
        <Link
          href="/kontakt#anfrage"
          className="flex min-h-16 items-center justify-center bg-ziegel px-3 text-[0.95rem] font-semibold tracking-tight text-paper"
        >
          Projekt anfragen
        </Link>
      </div>
    </div>
  );
}
