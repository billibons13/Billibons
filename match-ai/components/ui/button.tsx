import { cva, type VariantProps } from "class-variance-authority";
import Link from "next/link";
import type { ComponentProps } from "react";
import { cn } from "@/lib/utils";
import { Spinner } from "./spinner";

export const buttonVariants = cva(
  "relative inline-flex select-none items-center justify-center gap-2 whitespace-nowrap rounded-full font-medium transition-[background-color,border-color,color,box-shadow,transform] duration-200 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring disabled:pointer-events-none disabled:opacity-60 active:translate-y-px [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        primary:
          "bg-foreground text-background shadow-[0_8px_30px_-12px_rgb(165_171_255/0.6)] hover:bg-white hover:shadow-glow",
        accent: "bg-accent text-accent-foreground hover:bg-accent-strong hover:shadow-glow",
        secondary: "glass text-foreground hover:border-border-strong hover:bg-white/[0.06]",
        ghost: "text-muted hover:bg-white/[0.05] hover:text-foreground",
        link: "rounded-md px-0 text-accent-strong underline-offset-4 hover:underline",
        danger: "bg-negative/15 text-negative hover:bg-negative/25",
      },
      size: {
        sm: "h-9 px-4 text-sm",
        md: "h-11 px-5 text-sm",
        lg: "h-12 px-6 text-[0.95rem]",
        icon: "size-10",
      },
    },
    defaultVariants: { variant: "primary", size: "md" },
  },
);

type ButtonVariantProps = VariantProps<typeof buttonVariants>;

export interface ButtonProps extends ComponentProps<"button">, ButtonVariantProps {
  loading?: boolean;
  loadingText?: string;
}

export function Button({
  className,
  variant,
  size,
  loading = false,
  loadingText,
  disabled,
  children,
  type = "button",
  ...props
}: ButtonProps) {
  return (
    <button
      type={type}
      className={cn(buttonVariants({ variant, size }), className)}
      disabled={disabled || loading}
      aria-busy={loading || undefined}
      {...props}
    >
      {loading ? (
        <>
          <Spinner className="size-4" label={loadingText ?? "Loading"} />
          <span>{loadingText ?? children}</span>
        </>
      ) : (
        children
      )}
    </button>
  );
}

export interface ButtonLinkProps extends ComponentProps<typeof Link>, ButtonVariantProps {}

/** A link that looks like a button (navigation should use <a>, not <button>). */
export function ButtonLink({ className, variant, size, ...props }: ButtonLinkProps) {
  return <Link className={cn(buttonVariants({ variant, size }), className)} {...props} />;
}
