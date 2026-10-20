"use client";

import { Eye, EyeOff } from "lucide-react";
import { useState, type ComponentProps } from "react";
import { Input } from "@/components/ui/input";
import { FieldError, Label } from "@/components/ui/label";
import { useMessages } from "@/hooks/use-messages";
import { cn } from "@/lib/utils";

interface FieldProps extends Omit<ComponentProps<"input">, "id" | "name"> {
  name: string;
  label: string;
  error?: string;
}

export function TextField({ name, label, error, className, ...props }: FieldProps) {
  const id = `field-${name}`;
  const errorId = `${id}-error`;
  return (
    <div className={cn("space-y-2", className)}>
      <Label htmlFor={id}>{label}</Label>
      <Input id={id} name={name} invalid={Boolean(error)} aria-describedby={error ? errorId : undefined} {...props} />
      <FieldError id={errorId} message={error} />
    </div>
  );
}

export function PasswordField({ name, label, error, className, ...props }: FieldProps) {
  const [visible, setVisible] = useState(false);
  const m = useMessages();
  const id = `field-${name}`;
  const errorId = `${id}-error`;
  return (
    <div className={cn("space-y-2", className)}>
      <Label htmlFor={id}>{label}</Label>
      <div className="relative">
        <Input
          id={id}
          name={name}
          type={visible ? "text" : "password"}
          invalid={Boolean(error)}
          aria-describedby={error ? errorId : undefined}
          className="pr-11"
          {...props}
        />
        <button
          type="button"
          onClick={() => setVisible((value) => !value)}
          aria-label={visible ? m.auth.hidePassword : m.auth.showPassword}
          aria-pressed={visible}
          className="absolute right-1.5 top-1/2 inline-flex size-8 -translate-y-1/2 items-center justify-center rounded-lg text-muted transition-colors hover:bg-white/5 hover:text-foreground"
        >
          {visible ? <EyeOff className="size-4" aria-hidden="true" /> : <Eye className="size-4" aria-hidden="true" />}
        </button>
      </div>
      <FieldError id={errorId} message={error} />
    </div>
  );
}

/** Inline status message for the whole form (announced to screen readers). */
export function FormStatus({ status, message }: { status: "idle" | "error" | "success"; message?: string }) {
  if (status === "idle" || !message) return null;
  return (
    <p
      role={status === "error" ? "alert" : "status"}
      className={cn(
        "rounded-xl border px-4 py-3 text-sm leading-relaxed",
        status === "error" ? "border-negative/25 bg-negative/[0.07] text-negative" : "border-positive/25 bg-positive/[0.07] text-positive",
      )}
    >
      {message}
    </p>
  );
}
