"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { telHref, site } from "@/config/site";
import { mainNav } from "@/content/navigation";
import { ButtonLink } from "@/components/ui/Button";
import { PhoneIcon } from "@/components/ui/Icons";
import { Logo } from "./Logo";

export function Header() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => setOpen(false), [pathname]);

  useEffect(() => {
    document.documentElement.style.overflow = open ? "hidden" : "";
  }, [open]);

  return (
    <>
    <header
      className={`sticky top-0 z-50 transition-[background-color,box-shadow,backdrop-filter] duration-300 ${
        scrolled || open ? "bg-paper/90 shadow-[0_1px_0_rgba(18,19,20,0.08)] backdrop-blur-md" : "bg-paper"
      }`}
    >
      <div className="container-x flex h-16 items-center justify-between lg:h-20">
        <Logo />

        <nav aria-label="Hauptnavigation" className="hidden lg:block">
          <ul className="flex items-center gap-9">
            {mainNav.map((item) => {
              const active = pathname === item.href || pathname.startsWith(`${item.href}/`);
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    aria-current={active ? "page" : undefined}
                    className={`relative text-[0.95rem] tracking-tight transition-colors hover:text-ink ${
                      active ? "text-ink" : "text-anthrazit/70"
                    } after:absolute after:-bottom-1.5 after:left-0 after:h-px after:bg-ziegel after:transition-all after:duration-300 ${
                      active ? "after:w-full" : "after:w-0 hover:after:w-full"
                    }`}
                  >
                    {item.label}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        <div className="flex items-center gap-2">
          <a
            href={telHref}
            className="hidden items-center gap-2 px-3 text-[0.95rem] font-medium tracking-tight text-ink xl:flex"
          >
            <PhoneIcon className="size-4" />
            {site.contact.phone}
          </a>
          <div className="hidden sm:block">
            <ButtonLink href="/kontakt#anfrage">Projekt anfragen</ButtonLink>
          </div>
          <button
            type="button"
            onClick={() => setOpen((v) => !v)}
            aria-expanded={open}
            aria-controls="mobile-menu"
            className="flex size-12 items-center justify-center lg:hidden"
          >
            <span className="sr-only">{open ? "Menü schließen" : "Menü öffnen"}</span>
            <span className="relative block h-3 w-6" aria-hidden>
              <span className={`absolute left-0 h-[1.5px] w-6 bg-ink transition-all duration-300 ${open ? "top-1.5 rotate-45" : "top-0"}`} />
              <span className={`absolute left-0 h-[1.5px] w-6 bg-ink transition-all duration-300 ${open ? "top-1.5 -rotate-45" : "top-3"}`} />
            </span>
          </button>
        </div>
      </div>

    </header>
      {/* Mobiles Menü – außerhalb des <header>, da backdrop-filter dort position:fixed einschränkt */}
      <div
        id="mobile-menu"
        hidden={!open}
        className="fixed inset-x-0 top-16 bottom-0 z-40 overflow-y-auto bg-paper lg:hidden"
      >
        <nav aria-label="Mobile Navigation" className="container-x flex min-h-full flex-col pt-6 pb-28">
          <ul className="divide-y divide-beton-100 border-y border-beton-100">
            {mainNav.map((item) => (
              <li key={item.href}>
                <Link href={item.href} className="flex items-center justify-between py-5 text-2xl font-semibold tracking-tight">
                  {item.label}
                  <span className="text-beton-300" aria-hidden>
                    →
                  </span>
                </Link>
              </li>
            ))}
          </ul>
          <div className="mt-8 grid gap-3">
            <ButtonLink href="/kontakt#anfrage" size="lg">
              Kostenlose Anfrage
            </ButtonLink>
            <a href={telHref} className="flex min-h-14 items-center justify-center gap-3 border border-ink/20 font-medium">
              <PhoneIcon className="size-4" /> {site.contact.phone}
            </a>
          </div>
        </nav>
      </div>
    </>
  );
}
