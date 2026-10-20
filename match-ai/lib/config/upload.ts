import { parsePositiveNumber } from "./env";

export const DEFAULT_MAX_UPLOAD_MB = 8;
export const DEFAULT_IMAGE_RETENTION_DAYS = 30;

export const ALLOWED_IMAGE_TYPES = ["image/png", "image/jpeg", "image/webp"] as const;
export type AllowedImageType = (typeof ALLOWED_IMAGE_TYPES)[number];

export const ALLOWED_EXTENSIONS: Record<AllowedImageType, readonly string[]> = {
  "image/png": ["png"],
  "image/jpeg": ["jpg", "jpeg"],
  "image/webp": ["webp"],
};

/** Upload limit in bytes. Server code passes `serverEnv.maxUploadMb`. */
export function getMaxUploadBytes(maxUploadMb?: string): number {
  return Math.round(parsePositiveNumber(maxUploadMb, DEFAULT_MAX_UPLOAD_MB) * 1024 * 1024);
}

/** Days after which uploaded images are deleted (configurable, see IMAGE_RETENTION_DAYS). */
export function getImageRetentionDays(raw?: string): number {
  return Math.floor(parsePositiveNumber(raw, DEFAULT_IMAGE_RETENTION_DAYS));
}
