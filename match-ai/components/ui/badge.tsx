import { cva, type VariantProps } from "class-variance-authority";
import type { ComponentProps } from "react";
import { cn } from "@/lib/utils";

export const badgeVariants = cva(
  "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium [&_svg]:size-3.5",
  {
    variants: {
      variant: {
        default: "border-border bg-white/[0.04] text-muted",
        accent: "border-accent/30 bg-accent/10 text-accent-strong",
        positive: "border-positive/25 bg-positive/10 text-positive",
        negative: "border-negative/25 bg-negative/10 text-negative",
        warning: "border-warning/30 bg-warning/10 text-warning",
      },
    },
    defaultVariants: { variant: "default" },
  },
);

export interface BadgeProps extends ComponentProps<"span">, VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return <span className={cn(badgeVariants({ variant }), className)} {...props} />;
}
