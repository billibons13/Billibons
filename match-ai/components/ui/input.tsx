import type { ComponentProps } from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends ComponentProps<"input"> {
  invalid?: boolean;
}

export function Input({ className, invalid, ...props }: InputProps) {
  return (
    <input
      aria-invalid={invalid || undefined}
      className={cn(
        "h-11 w-full rounded-xl border border-border bg-white/[0.03] px-3.5 text-[0.95rem] text-foreground placeholder:text-subtle transition-[border-color,box-shadow,background-color] duration-150",
        "hover:border-border-strong focus-visible:border-accent/60 focus-visible:bg-white/[0.05] focus-visible:shadow-[0_0_0_4px_rgb(139_147_255/0.15)] focus-visible:outline-none",
        "aria-invalid:border-negative/60 aria-invalid:focus-visible:shadow-[0_0_0_4px_rgb(248_113_113/0.15)]",
        "disabled:cursor-not-allowed disabled:opacity-60",
        className,
      )}
      {...props}
    />
  );
}
