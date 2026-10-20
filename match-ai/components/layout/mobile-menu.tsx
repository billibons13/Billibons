"use client";

import { Menu, X } from "lucide-react";
import { useEffect, useId, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { ButtonLink } from "@/components/ui/button";
import { useMessages } from "@/hooks/use-messages";

interface MobileMenuProps {
  links: { href: string; label: string }[];
}

export function MobileMenu({ links }: MobileMenuProps) {
  const [open, setOpen] = useState(false);
  const panelId = useId();
  const buttonRef = useRef<HTMLButtonElement>(null);
  const m = useMessages();

  useEffect(() => {
    if (!open) return;
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setOpen(false);
        buttonRef.current?.focus();
      }
    };
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [open]);

  const close = () => setOpen(false);

  return (
    <div className="md:hidden">
      <button
        ref={buttonRef}
        type="button"
        aria-expanded={open}
        aria-controls={open ? panelId : undefined}
        aria-label={open ? m.nav.closeMenu : m.nav.openMenu}
        onClick={() => setOpen((value) => !value)}
        className="inline-flex size-10 items-center justify-center rounded-full text-foreground transition-colors hover:bg-white/5"
      >
        {open ? <X className="size-5" aria-hidden="true" /> : <Menu className="size-5" aria-hidden="true" />}
      </button>
      {/* Portal: the header uses backdrop-filter, which would trap a fixed child. */}
      {open
        ? createPortal(
              <div
                id={panelId}
                className="fixed inset-x-0 top-16 bottom-0 z-40 overflow-y-auto border-t border-border bg-background px-4 pb-10 pt-4 md:hidden"
              >
                <nav aria-label={m.nav.primaryLabel}>
                  <ul className="flex flex-col">
                    {links.map((link) => (
                      <li key={link.href}>
                        <a
                          href={link.href}
                          onClick={close}
                          className="block border-b border-border py-4 font-display text-lg text-foreground/90"
                        >
                          {link.label}
                        </a>
                      </li>
                    ))}
                  </ul>
                </nav>
                <div className="mt-8 flex flex-col gap-3">
                  <ButtonLink href="/register" size="lg" onClick={close}>
                    {m.nav.tryFree}
                  </ButtonLink>
                  <ButtonLink href="/login" variant="secondary" size="lg" onClick={close}>
                    {m.nav.login}
                  </ButtonLink>
                </div>
              </div>,
            document.body,
          )
        : null}
    </div>
  );
}
