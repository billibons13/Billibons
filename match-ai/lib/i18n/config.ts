/**
 * Supported locales. To add a language:
 * 1. Create lib/i18n/messages/<locale>.ts exporting an object typed as `Messages`.
 * 2. Add the locale code here and register the dictionary in lib/i18n/index.ts.
 * See docs/ARCHITECTURE.md → "Adding a language".
 */
export const LOCALES = ["en"] as const;
export type Locale = (typeof LOCALES)[number];

/** Planned next: "de", "ru", "uk". */
export const PLANNED_LOCALES = ["de", "ru", "uk"] as const;

export const DEFAULT_LOCALE: Locale = "en";

export function isLocale(value: string | undefined | null): value is Locale {
  return typeof value === "string" && (LOCALES as readonly string[]).includes(value);
}
