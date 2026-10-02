import Link from "next/link";
import type { ComponentProps, ReactNode } from "react";

type Variant = "primary" | "dark" | "outline" | "ghost" | "light";

const styles: Record<Variant, string> = {
  primary: "bg-ziegel text-paper hover:bg-ziegel-dark",
  dark: "bg-ink text-paper hover:bg-anthrazit",
  outline: "border border-ink/25 text-ink hover:border-ink hover:bg-ink hover:text-paper",
  ghost: "text-ink underline-offset-8 hover:underline px-0!",
  light: "border border-paper/40 text-paper hover:bg-paper hover:text-ink",
};

type Props = Omit<ComponentProps<typeof Link>, "className"> & {
  variant?: Variant;
  icon?: ReactNode;
  className?: string;
  size?: "md" | "lg";
};

export function ButtonLink({ variant = "primary", icon, className = "", size = "md", children, ...props }: Props) {
  return (
    <Link
      {...props}
      className={`group inline-flex min-h-12 whitespace-nowrap items-center justify-center gap-3 font-medium tracking-tight transition-colors duration-300 ${
        size === "lg" ? "px-7 text-base sm:min-h-14" : "px-6 text-[0.95rem]"
      } ${styles[variant]} ${className}`}
    >
      {children}
      {icon ?? <ArrowIcon className="size-4 transition-transform duration-300 group-hover:translate-x-1" />}
    </Link>
  );
}

export function ArrowIcon({ className = "size-4" }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" className={className} aria-hidden>
      <path d="M4 12h15M13 6l6 6-6 6" />
    </svg>
  );
}
