import type { ComponentProps } from "react";
import { cn } from "@/lib/utils";

export function Skeleton({ className, ...props }: ComponentProps<"div">) {
  return (
    <div
      aria-hidden="true"
      className={cn(
        "rounded-md bg-[linear-gradient(90deg,rgb(255_255_255/0.04)_0%,rgb(255_255_255/0.09)_50%,rgb(255_255_255/0.04)_100%)] bg-[length:200%_100%] animate-shimmer",
        className,
      )}
      {...props}
    />
  );
}
