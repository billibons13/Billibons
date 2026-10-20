import { format, getMessages, type Messages, type MessageVars } from "@/lib/i18n";

/** User-facing error codes. Messages live in lib/i18n/messages/en/common.ts → errors. */
export const ERROR_CODES = [
  "INVALID_IMAGE",
  "UNSUPPORTED_FORMAT",
  "IMAGE_TOO_LARGE",
  "MATCH_NOT_RECOGNIZED",
  "AI_UNAVAILABLE",
  "ANALYSIS_FAILED",
  "USAGE_LIMIT_REACHED",
  "PAYMENT_FAILED",
  "NOT_CONFIGURED",
] as const;

export type ErrorCode = (typeof ERROR_CODES)[number];

export function isErrorCode(value: unknown): value is ErrorCode {
  return typeof value === "string" && (ERROR_CODES as readonly string[]).includes(value);
}

/**
 * An error that is safe to show to the user. `cause` / internal details are
 * for logs only and must never be sent to the client.
 */
export class AppError extends Error {
  readonly code: ErrorCode;
  readonly vars?: MessageVars;

  constructor(code: ErrorCode, options?: { vars?: MessageVars; cause?: unknown }) {
    super(code, { cause: options?.cause });
    this.name = "AppError";
    this.code = code;
    this.vars = options?.vars;
  }
}

export function getErrorMessage(
  code: ErrorCode | "UNKNOWN",
  vars?: MessageVars,
  messages: Messages = getMessages(),
): string {
  return format(messages.errors[code], vars);
}

/** Serializable error payload for API responses / server actions. */
export interface PublicError {
  code: ErrorCode | "UNKNOWN";
  message: string;
}

export function toPublicError(error: unknown, messages: Messages = getMessages()): PublicError {
  if (error instanceof AppError) {
    return { code: error.code, message: getErrorMessage(error.code, error.vars, messages) };
  }
  return { code: "UNKNOWN", message: getErrorMessage("UNKNOWN", undefined, messages) };
}
