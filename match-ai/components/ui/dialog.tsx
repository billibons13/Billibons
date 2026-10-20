"use client";

import { X } from "lucide-react";
import { useEffect, useId, useRef, type ReactNode } from "react";
import { useMessages } from "@/hooks/use-messages";
import { cn } from "@/lib/utils";

export interface DialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  description?: string;
  children?: ReactNode;
  className?: string;
}

/**
 * Accessible modal built on the native <dialog> element: showModal() gives
 * focus containment, inert background, Esc to close and focus restoration.
 */
export function Dialog({ open, onOpenChange, title, description, children, className }: DialogProps) {
  const ref = useRef<HTMLDialogElement>(null);
  const titleId = useId();
  const descriptionId = useId();
  const m = useMessages();

  useEffect(() => {
    const dialog = ref.current;
    if (!dialog) return;
    if (open && !dialog.open) dialog.showModal();
    if (!open && dialog.open) dialog.close();
  }, [open]);

  return (
    <dialog
      ref={ref}
      aria-labelledby={titleId}
      aria-describedby={description ? descriptionId : undefined}
      onClose={() => onOpenChange(false)}
      onClick={(event) => {
        // Click on the backdrop (the dialog element itself) closes it.
        if (event.target === event.currentTarget) onOpenChange(false);
      }}
      className={cn(
        "m-auto w-[calc(100%-2rem)] max-w-lg rounded-2xl border border-border-strong bg-surface-2 p-0 text-foreground shadow-glow-soft open:animate-fade-up",
        className,
      )}
    >
      <div className="p-6 sm:p-7">
        <div className="flex items-start justify-between gap-4">
          <h2 id={titleId} className="font-display text-lg font-semibold tracking-tight">
            {title}
          </h2>
          <button
            type="button"
            onClick={() => onOpenChange(false)}
            className="-m-1.5 rounded-full p-1.5 text-muted transition-colors hover:bg-white/5 hover:text-foreground"
            aria-label={m.common.close}
          >
            <X className="size-4" aria-hidden="true" />
          </button>
        </div>
        {description ? (
          <p id={descriptionId} className="mt-3 text-sm leading-relaxed text-muted">
            {description}
          </p>
        ) : null}
        {children ? <div className="mt-5">{children}</div> : null}
      </div>
    </dialog>
  );
}
