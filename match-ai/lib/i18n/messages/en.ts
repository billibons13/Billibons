import { auth } from "./en/auth";
import { common } from "./en/common";
import { landing } from "./en/landing";
import { legal } from "./en/legal";

/**
 * English dictionary — the source of truth for every user-facing string.
 * Other locales must provide the same shape (see `Messages` in lib/i18n/types.ts).
 */
export const en = {
  ...common,
  landing,
  ...auth,
  ...legal,
} as const;
