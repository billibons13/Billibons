import {
  ALLOWED_EXTENSIONS,
  ALLOWED_IMAGE_TYPES,
  type AllowedImageType,
} from "@/lib/config/upload";
import type { ErrorCode } from "@/lib/errors";

export interface UploadCandidate {
  /** First bytes of the file are enough (>= 12), the whole file is fine too. */
  bytes: Uint8Array;
  /** MIME type as declared by the client (untrusted). */
  declaredType: string;
  fileName: string;
  /** Total size in bytes. */
  size: number;
}

export type UploadValidationResult =
  | { ok: true; type: AllowedImageType; extension: string }
  | { ok: false; code: Extract<ErrorCode, "INVALID_IMAGE" | "UNSUPPORTED_FORMAT" | "IMAGE_TOO_LARGE"> };

const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

function startsWith(bytes: Uint8Array, signature: number[], offset = 0): boolean {
  if (bytes.length < offset + signature.length) return false;
  return signature.every((b, i) => bytes[offset + i] === b);
}

/** Detects the real image type from magic bytes. Returns null for anything else. */
export function sniffImageType(bytes: Uint8Array): AllowedImageType | null {
  if (startsWith(bytes, PNG_SIGNATURE)) return "image/png";
  if (startsWith(bytes, [0xff, 0xd8, 0xff])) return "image/jpeg";
  // RIFF....WEBP
  if (startsWith(bytes, [0x52, 0x49, 0x46, 0x46]) && startsWith(bytes, [0x57, 0x45, 0x42, 0x50], 8)) {
    return "image/webp";
  }
  return null;
}

export function getExtension(fileName: string): string {
  const base = fileName.split(/[\\/]/).pop() ?? "";
  const dot = base.lastIndexOf(".");
  return dot > 0 ? base.slice(dot + 1).toLowerCase() : "";
}

function normalizeMime(mime: string): string {
  const value = mime.split(";")[0]?.trim().toLowerCase() ?? "";
  return value === "image/jpg" ? "image/jpeg" : value;
}

function isAllowedType(value: string): value is AllowedImageType {
  return (ALLOWED_IMAGE_TYPES as readonly string[]).includes(value);
}

/**
 * Validates an uploaded image. Order: size → declared MIME → extension →
 * magic bytes (the only check that is not trivially spoofable) → consistency.
 */
export function validateUpload(file: UploadCandidate, maxBytes: number): UploadValidationResult {
  if (file.size <= 0 || file.bytes.length === 0) return { ok: false, code: "INVALID_IMAGE" };
  if (file.size > maxBytes) return { ok: false, code: "IMAGE_TOO_LARGE" };

  const declared = normalizeMime(file.declaredType);
  if (!isAllowedType(declared)) return { ok: false, code: "UNSUPPORTED_FORMAT" };

  const extension = getExtension(file.fileName);
  const allowedExtensions = Object.values(ALLOWED_EXTENSIONS).flat();
  if (!allowedExtensions.includes(extension)) return { ok: false, code: "UNSUPPORTED_FORMAT" };

  const sniffed = sniffImageType(file.bytes);
  if (!sniffed) return { ok: false, code: "INVALID_IMAGE" };

  // Content must match both the declared MIME type and the extension.
  if (sniffed !== declared || !ALLOWED_EXTENSIONS[sniffed].includes(extension)) {
    return { ok: false, code: "INVALID_IMAGE" };
  }

  return { ok: true, type: sniffed, extension };
}
